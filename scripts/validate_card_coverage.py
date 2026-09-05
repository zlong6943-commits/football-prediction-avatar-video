#!/usr/bin/env python3
"""Validate presenter-first material-card timing from card-coverage.json."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


DEFAULT_LIMITS = {
    "max_coverage_ratio": 0.35,
    "max_card_seconds": 5.0,
    "min_presenter_only_gap_seconds": 3.0,
    "protected_opening_seconds": 4.0,
    "protected_ending_seconds": 5.0,
}


def read_report(value: str) -> dict[str, Any]:
    if value == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(value).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("report root must be an object")
    return data


def number(record: dict[str, Any], key: str, errors: list[str]) -> float:
    value = record.get(key)
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        errors.append(f"missing finite numeric {key}")
        return 0.0
    return float(value)


def merge_intervals(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    merged: list[tuple[float, float]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def validate(data: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    duration = number(data, "duration_seconds", errors)
    if duration <= 0:
        errors.append("duration_seconds must be positive")

    limits = dict(DEFAULT_LIMITS)
    supplied_limits = data.get("limits", {})
    if supplied_limits is not None and not isinstance(supplied_limits, dict):
        errors.append("limits must be an object")
        supplied_limits = {}
    for key in limits:
        if key in supplied_limits:
            value = supplied_limits[key]
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                errors.append(f"limits.{key} must be finite numeric")
            else:
                limits[key] = float(value)

    if limits["max_coverage_ratio"] > DEFAULT_LIMITS["max_coverage_ratio"]:
        errors.append("max_coverage_ratio cannot exceed 0.35 without a dense-cut exception")
    if limits["max_card_seconds"] > DEFAULT_LIMITS["max_card_seconds"]:
        errors.append("max_card_seconds cannot exceed 5.0 without a dense-cut exception")
    if limits["min_presenter_only_gap_seconds"] < DEFAULT_LIMITS["min_presenter_only_gap_seconds"]:
        errors.append("min_presenter_only_gap_seconds cannot be below 3.0")
    if limits["protected_opening_seconds"] < DEFAULT_LIMITS["protected_opening_seconds"]:
        errors.append("protected_opening_seconds cannot be below 4.0")
    if limits["protected_ending_seconds"] < DEFAULT_LIMITS["protected_ending_seconds"]:
        errors.append("protected_ending_seconds cannot be below 5.0")

    cards = data.get("cards")
    if not isinstance(cards, list):
        errors.append("cards must be an array")
        cards = []

    intervals: list[tuple[float, float]] = []
    seen_ids: set[str] = set()
    for position, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            errors.append(f"card {position} must be an object")
            continue
        card_id = card.get("id")
        if not isinstance(card_id, str) or not card_id.strip():
            errors.append(f"card {position} needs a non-empty id")
        elif card_id in seen_ids:
            errors.append(f"duplicate card id {card_id!r}")
        else:
            seen_ids.add(card_id)
        start = number(card, "start", errors)
        end = number(card, "end", errors)
        if start < 0 or end <= start or end > duration + 0.001:
            errors.append(f"card {card_id or position}: invalid interval {start:.3f}–{end:.3f}s")
            continue
        hold = end - start
        if hold > limits["max_card_seconds"] + 0.001:
            errors.append(
                f"card {card_id or position}: {hold:.3f}s exceeds "
                f"{limits['max_card_seconds']:.3f}s"
            )
        intervals.append((start, end))

    merged = merge_intervals(intervals)
    total_visible = sum(end - start for start, end in merged)
    coverage = total_visible / duration if duration > 0 else 1.0
    if coverage > limits["max_coverage_ratio"] + 0.0005:
        errors.append(
            f"material-card coverage {coverage:.3f} exceeds "
            f"{limits['max_coverage_ratio']:.3f}"
        )

    if intervals:
        if min(start for start, _ in intervals) < limits["protected_opening_seconds"] - 0.001:
            errors.append("a material card enters inside the protected opening interval")
        if max(end for _, end in intervals) > duration - limits["protected_ending_seconds"] + 0.001:
            errors.append("a material card enters inside the protected ending interval")

    gaps = [merged[index + 1][0] - merged[index][1] for index in range(len(merged) - 1)]
    for index, gap in enumerate(gaps, start=1):
        if gap < limits["min_presenter_only_gap_seconds"] - 0.001:
            errors.append(
                f"presenter-only gap {index} is {gap:.3f}s, below "
                f"{limits['min_presenter_only_gap_seconds']:.3f}s"
            )

    default_max_cards = max(1, math.ceil(duration / 30.0) + 1)
    if 60.0 <= duration <= 90.0:
        default_max_cards = 4
    configured_max = data.get("max_large_card_count", default_max_cards)
    if not isinstance(configured_max, int) or configured_max < 0:
        errors.append("max_large_card_count must be a non-negative integer")
        configured_max = default_max_cards
    if configured_max > default_max_cards:
        errors.append(
            f"max_large_card_count {configured_max} exceeds default {default_max_cards} "
            "without a dense-cut exception"
        )
    if len(cards) > configured_max:
        errors.append(f"large material-card count {len(cards)} exceeds {configured_max}")

    metrics = {
        "duration_seconds": round(duration, 3),
        "large_material_card_count": len(cards),
        "material_card_total_visible_seconds": round(total_visible, 3),
        "material_card_coverage_ratio": round(coverage, 4),
        "presenter_only_coverage_ratio": round(max(0.0, 1.0 - coverage), 4),
        "longest_material_card_seconds": round(
            max((end - start for start, end in intervals), default=0.0), 3
        ),
        "shortest_presenter_only_gap_seconds": round(min(gaps), 3) if gaps else None,
        "protected_opening_seconds": limits["protected_opening_seconds"],
        "protected_ending_seconds": limits["protected_ending_seconds"],
    }
    return errors, metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="card-coverage.json path, or - for stdin")
    args = parser.parse_args()
    try:
        data = read_report(args.report)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"card coverage validation failed: {exc}", file=sys.stderr)
        return 2
    errors, metrics = validate(data)
    if errors:
        print(f"card coverage validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        return 1
    print("card coverage validation passed")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
