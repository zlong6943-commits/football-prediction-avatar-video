#!/usr/bin/env python3
"""Validate official logo provenance and file integrity in sources.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_EVIDENCE = {
    "club-brand-page",
    "club-site-current-asset",
    "competition-official-page",
}
DENIED_HOST_PARTS = {
    "wikipedia.org",
    "wikimedia.org",
    "worldvectorlogo.com",
    "seeklogo.com",
    "brandsoftheworld.com",
    "logoeps.com",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def host(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("URL must be an absolute HTTPS URL")
    return parsed.hostname.lower()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path, help="Job directory containing sources.json")
    args = parser.parse_args()

    manifest_path = args.job / "sources.json"
    if not manifest_path.is_file():
        raise SystemExit(f"missing {manifest_path}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    logos = data.get("logos")
    if not isinstance(logos, list) or len(logos) < 2:
        raise SystemExit("sources.json must contain at least two logo records")

    errors: list[str] = []
    for index, record in enumerate(logos):
        label = f"logos[{index}]"
        try:
            page_host = host(str(record.get("official_page_url", "")))
            asset_host = host(str(record.get("asset_url", "")))
            if any(part in page_host or part in asset_host for part in DENIED_HOST_PARTS):
                errors.append(f"{label}: denied third-party logo host")
        except ValueError as exc:
            errors.append(f"{label}: {exc}")

        if record.get("evidence_class") not in ALLOWED_EVIDENCE:
            errors.append(f"{label}: invalid evidence_class")
        relative = Path(str(record.get("file", "")))
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"{label}: file must be a safe job-relative path")
            continue
        logo_file = args.job / relative
        if not logo_file.is_file():
            errors.append(f"{label}: logo file does not exist")
            continue
        expected = str(record.get("sha256", "")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"{label}: invalid sha256")
        elif sha256_file(logo_file) != expected:
            errors.append(f"{label}: sha256 mismatch")
        if not record.get("retrieved_at"):
            errors.append(f"{label}: missing retrieved_at")
        if not record.get("team"):
            errors.append(f"{label}: missing team")

    if errors:
        raise SystemExit("logo manifest check failed:\n- " + "\n- ".join(errors))
    print(f"logo manifest check passed for {len(logos)} logos")


if __name__ == "__main__":
    main()
