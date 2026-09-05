#!/usr/bin/env python3
"""Align semantic display captions to Whisper-compatible token timestamps."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


SPECIAL_TOKEN_RE = re.compile(r"^\[_")
DIGIT_DASH_RE = re.compile(r"(\d)\s*[-–—]\s*(\d)")


def canonical(text: str) -> list[str]:
    text = DIGIT_DASH_RE.sub(r"\1比\2", unicodedata.normalize("NFKC", text).lower())
    return [
        char
        for char in text
        if unicodedata.category(char)[0] in {"L", "N"} or "\u3400" <= char <= "\u9fff"
    ]


def format_time(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def parse_spoken_srt(path: Path) -> list[str]:
    blocks = re.split(r"\r?\n\s*\r?\n", path.read_text(encoding="utf-8-sig").strip())
    text: list[str] = []
    for number, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3:
            raise ValueError(f"spoken SRT cue {number} is incomplete")
        text.extend(canonical("".join(lines[2:])))
    if not text:
        raise ValueError("spoken SRT contains no alignable text")
    return text


def flatten_plan(value: Any) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    if isinstance(value, list):
        for item in value:
            output.extend(flatten_plan(item))
        return output
    if isinstance(value, str):
        return [{"display": value, "spoken": value}]
    if not isinstance(value, dict):
        raise ValueError(f"unsupported caption-plan item: {value!r}")

    display = value.get("display", value.get("text"))
    spoken = value.get("spoken", display)
    if not isinstance(display, str) or not display.strip():
        raise ValueError(f"caption-plan item has no display text: {value!r}")
    if not isinstance(spoken, str) or not spoken.strip():
        raise ValueError(f"caption-plan item has no spoken anchor: {value!r}")
    if "spoken" not in value and any(unicodedata.category(char).startswith("S") for char in display):
        raise ValueError(
            f"icon display {display!r} requires an explicit spoken phrase for alignment"
        )
    return [{"display": display.strip(), "spoken": spoken.strip()}]


def align(left: list[str], right: list[str]) -> tuple[int, list[int | None]]:
    rows = len(left) + 1
    columns = len(right) + 1
    matrix = [[0] * columns for _ in range(rows)]
    for row in range(rows):
        matrix[row][0] = row
    for column in range(columns):
        matrix[0][column] = column

    for row in range(1, rows):
        for column in range(1, columns):
            substitution = matrix[row - 1][column - 1] + (
                0 if left[row - 1] == right[column - 1] else 1
            )
            matrix[row][column] = min(
                substitution,
                matrix[row - 1][column] + 1,
                matrix[row][column - 1] + 1,
            )

    mapping: list[int | None] = [None] * len(left)
    row = len(left)
    column = len(right)
    while row or column:
        if row and column:
            cost = 0 if left[row - 1] == right[column - 1] else 1
            if matrix[row][column] == matrix[row - 1][column - 1] + cost:
                mapping[row - 1] = column - 1
                row -= 1
                column -= 1
                continue
        if row and matrix[row][column] == matrix[row - 1][column] + 1:
            row -= 1
            continue
        column -= 1
    return matrix[-1][-1], mapping


def recognized_tokens(path: Path) -> tuple[list[str], list[dict[str, float]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    transcription = data.get("transcription")
    if not isinstance(transcription, list):
        raise ValueError("Whisper JSON has no transcription list")

    chars: list[str] = []
    times: list[dict[str, float]] = []
    for segment in transcription:
        for token in segment.get("tokens", []):
            token_text = str(token.get("text", ""))
            if SPECIAL_TOKEN_RE.match(token_text):
                continue
            token_chars = canonical(token_text)
            if not token_chars:
                continue
            offsets = token.get("offsets") or {}
            start = float(offsets.get("from", 0)) / 1000
            end = float(offsets.get("to", offsets.get("from", 0))) / 1000
            duration = max(0.0, end - start)
            for index, char in enumerate(token_chars):
                chars.append(char)
                times.append(
                    {
                        "start": start + duration * index / len(token_chars),
                        "end": start + duration * (index + 1) / len(token_chars),
                    }
                )
    if not chars:
        raise ValueError("Whisper JSON contains no timed speech tokens")
    return chars, times


def fill_missing_times(values: list[dict[str, float] | None]) -> list[dict[str, float]]:
    filled = values[:]
    for index, value in enumerate(filled):
        if value is not None:
            continue
        left = index - 1
        right = index + 1
        while left >= 0 and filled[left] is None:
            left -= 1
        while right < len(filled) and filled[right] is None:
            right += 1
        if left >= 0 and right < len(filled):
            assert filled[left] is not None and filled[right] is not None
            ratio = (index - left) / (right - left)
            point = filled[left]["end"] + (filled[right]["start"] - filled[left]["end"]) * ratio
        elif left >= 0:
            assert filled[left] is not None
            point = filled[left]["end"]
        elif right < len(filled):
            assert filled[right] is not None
            point = filled[right]["start"]
        else:
            raise ValueError("alignment produced no usable timestamps")
        filled[index] = {"start": point, "end": point}
    return [value for value in filled if value is not None]


def write_outputs(
    plan: list[dict[str, str]],
    expected: list[str],
    recognized: list[str],
    recognized_times: list[dict[str, float]],
    output_srt: Path,
    output_report: Path,
    cover_shift: float,
    visual_lead: float,
    max_visual_lead: float,
    min_duration: float,
    min_similarity: float,
) -> None:
    recognition_distance, expected_mapping = align(expected, recognized)
    recognition_similarity = 1 - recognition_distance / max(len(expected), len(recognized))
    if recognition_similarity < min_similarity:
        raise ValueError(f"speech alignment similarity too low: {recognition_similarity:.3f}")

    expected_times = fill_missing_times(
        [recognized_times[index] if index is not None else None for index in expected_mapping]
    )
    hint_groups = [canonical(item["spoken"]) for item in plan]
    if any(not group for group in hint_groups):
        raise ValueError("every caption-plan item needs alignable spoken text")
    hinted = [char for group in hint_groups for char in group]
    plan_distance, plan_mapping = align(hinted, expected)
    plan_similarity = 1 - plan_distance / max(len(hinted), len(expected))
    if plan_similarity < 0.90:
        raise ValueError(f"caption plan does not partition the approved speech: {plan_similarity:.3f}")

    ranges: list[tuple[int, int]] = []
    cursor = 0
    for group in hint_groups:
        mapped = [index for index in plan_mapping[cursor : cursor + len(group)] if index is not None]
        if not mapped:
            raise ValueError(f"caption {len(ranges) + 1} has no spoken alignment")
        ranges.append((min(mapped), max(mapped)))
        cursor += len(group)

    speech_starts = [expected_times[first]["start"] + cover_shift for first, _ in ranges]
    speech_ends = [expected_times[last]["end"] + cover_shift for _, last in ranges]
    starts = [max(cover_shift if index == 0 else 0.0, value - visual_lead) for index, value in enumerate(speech_starts)]
    for index in range(len(starts) - 2, -1, -1):
        earliest = speech_starts[index] - max_visual_lead
        starts[index] = max(earliest, min(starts[index], starts[index + 1] - min_duration - 0.03))

    cues: list[dict[str, Any]] = []
    for index, item in enumerate(plan):
        end = (
            starts[index + 1] - 0.03
            if index + 1 < len(starts)
            else max(speech_ends[index] + 0.22, starts[index] + min_duration)
        )
        if end - starts[index] < min_duration - 0.001:
            raise ValueError(
                f"caption {index + 1} is too short after alignment; merge or re-segment nearby cues"
            )
        cues.append(
            {
                "index": index + 1,
                "text": item["display"],
                "spoken": item["spoken"],
                "caption_start": round(starts[index], 3),
                "caption_end": round(end, 3),
                "speech_start": round(speech_starts[index], 3),
                "speech_end": round(speech_ends[index], 3),
            }
        )

    srt = "\n\n".join(
        f"{cue['index']}\n{format_time(cue['caption_start'])} --> {format_time(cue['caption_end'])}\n{cue['text']}"
        for cue in cues
    ) + "\n"
    anchors = sorted({0, len(cues) // 4, len(cues) // 2, 3 * len(cues) // 4, len(cues) - 1})
    report = {
        "method": "word_token_alignment",
        "cover_shift_seconds": cover_shift,
        "visual_lead_seconds": visual_lead,
        "recognition_similarity": round(recognition_similarity, 4),
        "caption_plan_similarity": round(plan_similarity, 4),
        "anchor_indices": [index + 1 for index in anchors],
        "cues": cues,
        "visual_beats": [],
    }
    output_srt.write_text(srt, encoding="utf-8")
    output_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spoken-srt", type=Path, required=True, help="exact approved spoken text in SRT form")
    parser.add_argument("--whisper-json", type=Path, required=True, help="Whisper full JSON with token offsets")
    parser.add_argument("--plan", type=Path, required=True, help="semantic caption plan JSON")
    parser.add_argument("--output-srt", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    parser.add_argument("--cover-shift", type=float, default=0.0)
    parser.add_argument("--visual-lead", type=float, default=0.16)
    parser.add_argument("--max-visual-lead", type=float, default=0.22)
    parser.add_argument("--min-duration", type=float, default=0.20)
    parser.add_argument("--min-similarity", type=float, default=0.80)
    args = parser.parse_args()

    for path in (args.spoken_srt, args.whisper_json, args.plan):
        if not path.is_file():
            parser.error(f"file not found: {path}")
    if args.visual_lead < 0 or args.max_visual_lead < args.visual_lead:
        parser.error("visual lead values are invalid")

    plan = flatten_plan(json.loads(args.plan.read_text(encoding="utf-8")))
    recognized, times = recognized_tokens(args.whisper_json)
    write_outputs(
        plan,
        parse_spoken_srt(args.spoken_srt),
        recognized,
        times,
        args.output_srt,
        args.output_report,
        args.cover_shift,
        args.visual_lead,
        args.max_visual_lead,
        args.min_duration,
        args.min_similarity,
    )
    print(f"wrote {args.output_srt} and {args.output_report} with {len(plan)} aligned cues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
