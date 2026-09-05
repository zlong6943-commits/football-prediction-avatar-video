#!/usr/bin/env python3
"""Final no-regression gate for a football avatar-video delivery folder."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


FINAL_RE = re.compile(r"final-v(\d+)\.mp4$")


def load(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing {path.name}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name} root must be an object")
        return {}
    return value


def run_gate(script: Path, arguments: list[str], errors: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(script), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if result.returncode:
        errors.append(f"{script.name} failed: {result.stdout.strip()}")


def require_zero(record: dict[str, Any], key: str, errors: list[str]) -> None:
    if record.get(key) != 0:
        errors.append(f"captions.{key} must be 0")


def number(record: dict[str, Any], key: str, errors: list[str]) -> float | None:
    value = record.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append(f"visual.{key} must be numeric")
        return None
    return float(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path)
    args = parser.parse_args()
    job = args.job.resolve()
    scripts = Path(__file__).resolve().parent
    errors: list[str] = []

    brief = load(job / "brief.json", errors)
    presenter = load(job / "presenter.json", errors)
    delivery = load(job / "delivery.json", errors)
    qa = load(job / "qa-report.json", errors)
    av = load(job / "av-sync-report.json", errors)

    video = brief.get("video") or {}
    if video.get("aspect_ratio") != "9:16" or video.get("resolution") != "1080x1920":
        errors.append("brief.video must specify 9:16 at 1080x1920")
    if abs(float(video.get("cover_seconds", -1))) > 0.01:
        errors.append("brief.video.cover_seconds must be 0.0 for the standalone-cover default")
    if video.get("burned_source_captions") is not False:
        errors.append("brief must confirm burned_source_captions=false")
    if video.get("caption_mask") is not False:
        errors.append("brief must confirm caption_mask=false")

    caps = brief.get("hard_caps") or {}
    approvals = load(job / "approvals.json", errors)
    budget_override = approvals.get("api_budget_override") or {}
    allowed_usd = 2.0
    if (
        budget_override.get("approved") is True
        and budget_override.get("scope") == job.name
        and budget_override.get("provider") == "HeyGen official API"
        and budget_override.get("paid_retries_allowed") is False
    ):
        allowed_usd = min(4.0, float(budget_override.get("usd_hard_cap", 0)))
    if float(caps.get("usd", 999)) > allowed_usd or float(caps.get("credits", 999)) > 40:
        errors.append(f"brief hard caps must not exceed US${allowed_usd:g} and 40 credits")

    if presenter.get("authorized") is not True:
        errors.append("presenter.json must record authorization")
    if not presenter.get("profile") or not presenter.get("voice_name"):
        errors.append("presenter profile and voice name are required")
    if presenter.get("profile") == "七姐" and presenter.get("brand_search_text") != "7姐聊球":
        errors.append("七姐 profile must use brand_search_text=7姐聊球")

    final_rel = str(delivery.get("final_video", ""))
    source_rel = str(delivery.get("clean_avatar_source", ""))
    sync_rel = str(delivery.get("sync_source", source_rel))
    final_match = FINAL_RE.fullmatch(Path(final_rel).name)
    if not final_match:
        errors.append("delivery.final_video must use final-vNN.mp4")
    if Path(source_rel).name != "avatar-clean.mp4":
        errors.append("delivery.clean_avatar_source must point to avatar-clean.mp4")
    final_path = job / final_rel
    source_path = job / source_rel
    if not final_path.is_file():
        errors.append("delivery final video does not exist")
    if not source_path.is_file():
        errors.append("delivery clean avatar source does not exist")
    if sync_rel and not (job / sync_rel).is_file():
        errors.append("delivery sync source does not exist")
    if final_path.resolve() == source_path.resolve():
        errors.append("final video and clean source must be different files")
    versions = [int(match.group(1)) for path in job.glob("final-v*.mp4") if (match := FINAL_RE.fullmatch(path.name))]
    if final_match and versions and int(final_match.group(1)) != max(versions):
        errors.append("delivery.final_video is not the newest rendered version")

    if av.get("status") != "pass":
        errors.append("av-sync-report.json must pass")
    if len(av.get("audio_anchors") or []) < 6 or len(av.get("picture_anchors") or []) < 6:
        errors.append("A/V report must contain at least six audio and six picture anchors")
    av_final_name = Path(str((av.get("final") or {}).get("path", ""))).name
    av_source_name = Path(str((av.get("source") or {}).get("path", ""))).name
    if final_rel and av_final_name != Path(final_rel).name:
        errors.append("A/V report does not describe the delivered final video")
    if sync_rel and av_source_name != Path(sync_rel).name:
        errors.append("A/V report does not describe the declared sync source")

    qa_video = qa.get("video") or {}
    if qa_video.get("width") != 1080 or qa_video.get("height") != 1920:
        errors.append("qa video resolution must be 1080x1920")
    if qa_video.get("video_codec") != "h264":
        errors.append("qa video codec must be h264")
    if qa_video.get("audio_codec") != "aac" or qa_video.get("audio_sample_rate") != 48000:
        errors.append("qa audio must be AAC 48 kHz")

    captions = qa.get("captions") or {}
    for key in (
        "multiline_cues",
        "punctuation_cues",
        "overlapping_cues",
        "out_of_bounds_cues",
        "duplicate_caption_layers",
        "character_by_character_cues",
        "underlined_cues",
    ):
        require_zero(captions, key, errors)
    if captions.get("status") != "pass":
        errors.append("caption QA status must pass")

    visual = qa.get("visual") or {}
    required_true = (
        "fixture_bar_covers_head",
        "search_box_covers_face",
        "burned_source_captions",
        "bottom_mask_used",
        "betting_brand_detected",
    )
    for key in required_true:
        if visual.get(key) is not False:
            errors.append(f"visual.{key} must be false")
    if visual.get("search_box_label") != "查看更多":
        errors.append("search box label must be 查看更多")
    if presenter.get("brand_search_text") and visual.get("search_box_text") != presenter.get(
        "brand_search_text"
    ):
        errors.append("search box text does not match presenter profile")
    if visual.get("search_box_retype_interval_seconds") != 10:
        errors.append("search box must clear and retype every 10 seconds")
    cover_fixture_bottom = number(visual, "cover_fixture_bottom_y", errors)
    fixture_top = number(visual, "fixture_bar_top_y", errors)
    fixture_bottom = number(visual, "fixture_bar_bottom_y", errors)
    hair_top = number(visual, "presenter_hair_top_y", errors)
    search_left = number(visual, "search_box_left_x", errors)
    card_opacity = number(visual, "material_card_shell_opacity", errors)
    card_blur = number(visual, "material_card_backdrop_blur_px", errors)
    if cover_fixture_bottom is not None and cover_fixture_bottom > 1780:
        errors.append("cover fixture panel must not extend below y=1780")
    if fixture_top is not None and fixture_top < 110:
        errors.append("in-video fixture bar must not enter the y<110 phone-top exclusion zone")
    if fixture_bottom is not None and hair_top is not None and fixture_bottom > hair_top - 24:
        errors.append("in-video fixture bar must keep at least 24px above presenter hair/head")
    if search_left is not None and search_left < 56:
        errors.append("search widget must keep at least 56px left phone-edge clearance")
    if card_opacity is not None and not 0.50 <= card_opacity <= 0.65:
        errors.append("material card shell opacity must be between 0.50 and 0.65")
    if card_blur is not None and not 8 <= card_blur <= 12:
        errors.append("material card backdrop blur must be between 8px and 12px")
    if visual.get("cards_are_intermittent") is not True:
        errors.append("material cards must be intermittent with presenter-only gaps")
    if visual.get("hyperframes_check") != "pass" or visual.get("status") != "pass":
        errors.append("HyperFrames/visual QA must pass")

    run_gate(scripts / "check_approvals.py", [str(job), "--stage", "render"], errors)
    run_gate(scripts / "check_generation_budget.py", [str(job), "--stage", "postflight"], errors)
    run_gate(scripts / "verify_logo_manifest.py", [str(job)], errors)
    run_gate(scripts / "validate_captions.py", [str(job / "captions.srt")], errors)
    sync_arguments = [str(job / "caption-sync.json")]
    if isinstance(video.get("fps"), (int, float)) and float(video["fps"]) > 0:
        sync_arguments.extend(["--fps", str(video["fps"])])
    run_gate(scripts / "validate_caption_sync.py", sync_arguments, errors)

    if errors:
        print(f"delivery contract failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"delivery contract passed: final={final_rel}, raw={source_rel}, "
        "budget/sync/captions/logos/visual gates passed"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"delivery contract failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
