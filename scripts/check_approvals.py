#!/usr/bin/env python3
"""Validate the recorded approval gates for a football avatar-video job."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"approval check failed: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path, help="Job directory")
    parser.add_argument("--stage", choices=("generate", "render"), required=True)
    args = parser.parse_args()

    approval_path = args.job / "approvals.json"
    if not approval_path.is_file():
        fail(f"missing {approval_path}")
    data = json.loads(approval_path.read_text(encoding="utf-8"))

    script = data.get("script") or {}
    if script.get("approved") is not True:
        fail("script is not explicitly approved")
    script_file = args.job / str(script.get("file", ""))
    expected_hash = str(script.get("sha256", "")).lower()
    if not script_file.is_file() or len(expected_hash) != 64:
        fail("approved script file or hash is invalid")
    actual_hash = sha256_file(script_file)
    if actual_hash != expected_hash:
        fail("approved script changed after approval")

    if args.stage == "render":
        visual = data.get("visual") or {}
        if visual.get("approved") is not True:
            fail("visual sample is not explicitly approved")
        revision_file = args.job / str(visual.get("file", ""))
        expected_visual_hash = str(visual.get("sha256", "")).lower()
        if not revision_file.is_file() or len(expected_visual_hash) != 64:
            fail("approved visual revision file or hash is invalid")
        if sha256_file(revision_file) != expected_visual_hash:
            fail("visual revision changed after approval")

    print(f"approval check passed for stage={args.stage}")


if __name__ == "__main__":
    main()
