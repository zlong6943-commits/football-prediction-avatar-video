#!/usr/bin/env python3
"""Validate caption/audio anchors and motion/SFX timing in caption-sync.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def number(record: dict[str, Any], key: str, label: str, errors: list[str]) -> float:
    value = record.get(key)
    if not isinstance(value, (int, float)):
        errors.append(f"{label}: missing numeric {key}")
        return 0.0
    return float(value)


def distributed_anchor_indices(count: int) -> list[int]:
    return sorted({0, count // 4, count // 2, 3 * count // 4, count - 1})


def validate(
    data: dict[str, Any],
    max_caption_lead: float,
    max_caption_lag: float,
    fps: float,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    cover_shift = number(data, "cover_shift_seconds", "root", errors)
    cues = data.get("cues")
    if not isinstance(cues, list) or len(cues) < 5:
        return errors + ["root: at least five aligned caption cues are required"], notes

    previous_end = 0.0
    for position, cue in enumerate(cues, start=1):
        if not isinstance(cue, dict):
            errors.append(f"cue {position}: record must be an object")
            continue
        if cue.get("index") != position:
            errors.append(f"cue {position}: index must be sequential")
        caption_start = number(cue, "caption_start", f"cue {position}", errors)
        caption_end = number(cue, "caption_end", f"cue {position}", errors)
        speech_start = number(cue, "speech_start", f"cue {position}", errors)
        speech_end = number(cue, "speech_end", f"cue {position}", errors)
        if caption_end <= caption_start:
            errors.append(f"cue {position}: caption end must follow caption start")
        if speech_end < speech_start:
            errors.append(f"cue {position}: speech end must not precede speech start")
        if caption_start < previous_end - 0.001:
            errors.append(f"cue {position}: caption overlaps the previous cue")
        previous_end = max(previous_end, caption_end)
        lead = speech_start - caption_start
        if lead > max_caption_lead + 0.001:
            errors.append(
                f"cue {position}: caption leads speech by {lead:.3f}s, over {max_caption_lead:.3f}s"
            )
        if lead < -max_caption_lag - 0.001:
            errors.append(
                f"cue {position}: caption lags speech by {-lead:.3f}s, over {max_caption_lag:.3f}s"
            )

    first_speech = float(cues[0].get("speech_start", 0.0))
    if first_speech < cover_shift - 0.001:
        errors.append("root: narration begins before the opening cover has ended")

    expected_anchors = distributed_anchor_indices(len(cues))
    supplied = data.get("anchor_indices")
    if not isinstance(supplied, list) or len(set(supplied)) < 5:
        errors.append("root: anchor_indices must record five distributed caption anchors")
    else:
        zero_based = sorted({int(index) - 1 for index in supplied})
        if zero_based != expected_anchors:
            errors.append(
                f"root: anchor_indices must cover opening/25%/50%/75%/ending; expected "
                f"{[index + 1 for index in expected_anchors]}"
            )
        else:
            for index in zero_based:
                cue = cues[index]
                notes.append(
                    f"anchor {cue['index']}: {cue.get('text', '')!r} "
                    f"caption={float(cue['caption_start']):.3f}s "
                    f"speech={float(cue['speech_start']):.3f}s"
                )

    beats = data.get("visual_beats")
    if not isinstance(beats, list) or not beats:
        errors.append("root: add visual_beats for fixture/cards and their SFX before render")
    else:
        two_frames = 2 / fps
        for position, beat in enumerate(beats, start=1):
            if not isinstance(beat, dict):
                errors.append(f"visual beat {position}: record must be an object")
                continue
            label = f"visual beat {beat.get('id', position)!r}"
            speech_anchor = number(beat, "speech_anchor", label, errors)
            motion_start = number(beat, "motion_start", label, errors)
            sfx_start = number(beat, "sfx_start", label, errors)
            motion_delta = motion_start - speech_anchor
            if not -0.25 <= motion_delta <= 0.10:
                errors.append(
                    f"{label}: motion is {motion_delta:+.3f}s from its spoken claim; "
                    "retime the card or choose the correct anchor"
                )
            if abs(sfx_start - motion_start) > two_frames + 0.001:
                errors.append(
                    f"{label}: SFX is {abs(sfx_start - motion_start):.3f}s from motion, "
                    f"over two frames ({two_frames:.3f}s)"
                )

    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path, help="caption-sync.json")
    parser.add_argument("--max-caption-lead", type=float, default=0.22)
    parser.add_argument("--max-caption-lag", type=float, default=0.05)
    parser.add_argument("--fps", type=float, default=25.0)
    args = parser.parse_args()
    if not args.report.is_file():
        parser.error(f"file not found: {args.report}")
    if args.fps <= 0:
        parser.error("fps must be positive")

    data = json.loads(args.report.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        parser.error("report root must be an object")
    errors, notes = validate(data, args.max_caption_lead, args.max_caption_lag, args.fps)
    if errors:
        print(f"caption sync validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("caption sync validation passed")
    for note in notes:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
