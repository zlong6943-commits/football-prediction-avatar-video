#!/usr/bin/env python3
"""Validate the football avatar video's display-caption contract."""

from __future__ import annotations

import argparse
import re
import string
import sys
import unicodedata
from pathlib import Path


TIMECODE_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+"
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
)
DEFAULT_FORBIDDEN_TERMS = ("sky bet", "skybet")


def is_punctuation(char: str) -> bool:
    return char in string.punctuation or unicodedata.category(char).startswith("P")


def parse_timecode(value: str) -> tuple[float, float] | None:
    match = TIMECODE_RE.fullmatch(value)
    if not match:
        return None
    numbers = [int(part) for part in match.groups()]
    start = numbers[0] * 3600 + numbers[1] * 60 + numbers[2] + numbers[3] / 1000
    end = numbers[4] * 3600 + numbers[5] * 60 + numbers[6] + numbers[7] / 1000
    return start, end


def validate(path: Path, forbidden_terms: tuple[str, ...]) -> list[str]:
    content = path.read_text(encoding="utf-8-sig").strip()
    if not content:
        return ["caption file is empty"]

    errors: list[str] = []
    blocks = re.split(r"\r?\n\s*\r?\n", content)
    previous_end = 0.0
    for block_number, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3:
            errors.append(f"cue {block_number}: expected index, timecode, and text")
            continue

        if lines[0].strip() != str(block_number):
            errors.append(
                f"cue {block_number}: expected sequential index {block_number}, got {lines[0]!r}"
            )

        timing = parse_timecode(lines[1].strip())
        if timing is None:
            errors.append(f"cue {block_number}: invalid SRT timecode {lines[1]!r}")
        else:
            start, end = timing
            if end <= start:
                errors.append(f"cue {block_number}: end must be after start")
            if start < previous_end - 0.001:
                errors.append(f"cue {block_number}: overlaps the previous cue")
            previous_end = max(previous_end, end)

        text_lines = lines[2:]
        if len(text_lines) != 1:
            errors.append(f"cue {block_number}: caption must use exactly one text line")
        caption = "".join(text_lines).strip()
        if not caption:
            errors.append(f"cue {block_number}: caption text is empty")
            continue

        if any(mark in caption.lower() for mark in ("<br", "\\n", "\u2028", "\u2029")):
            errors.append(f"cue {block_number}: explicit line-break markup is forbidden")

        marks = "".join(char for char in caption if is_punctuation(char))
        if marks:
            errors.append(f"cue {block_number}: punctuation is forbidden: {marks!r}")

        folded = " ".join(caption.casefold().split())
        for term in forbidden_terms:
            if term.casefold() in folded:
                errors.append(f"cue {block_number}: forbidden visible term {term!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reject punctuation, multi-line or empty cues, invalid timing, overlaps, "
            "and forbidden visible terms. Screen fit remains a rendered-pixel QA gate."
        )
    )
    parser.add_argument("srt", type=Path, help="SRT file to validate")
    parser.add_argument(
        "--forbidden-term",
        action="append",
        default=[],
        help="additional case-insensitive visible term to reject; repeat as needed",
    )
    args = parser.parse_args()

    if not args.srt.is_file():
        parser.error(f"file not found: {args.srt}")

    forbidden = DEFAULT_FORBIDDEN_TERMS + tuple(args.forbidden_term)
    errors = validate(args.srt, forbidden)
    if errors:
        print(f"caption validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "caption validation passed: one line per cue, no punctuation, "
        "valid non-overlapping timing, forbidden terms absent"
    )
    print("note: verify semantic segmentation and horizontal fit on rendered pixels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
