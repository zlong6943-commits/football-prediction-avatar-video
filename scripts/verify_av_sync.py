#!/usr/bin/env python3
"""Measure source-to-final audio and picture delay at distributed anchors."""

from __future__ import annotations

import argparse
import array
import json
import math
import shutil
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(command: list[str]) -> bytes:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(error or f"command failed: {' '.join(command)}")
    return result.stdout


def parse_rate(value: str) -> float:
    if "/" in value:
        left, right = value.split("/", 1)
        denominator = float(right)
        return float(left) / denominator if denominator else 0.0
    return float(value)


def probe(path: Path) -> dict[str, Any]:
    payload = json.loads(
        run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(path),
            ]
        )
    )
    streams = payload.get("streams") or []
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    audio = next((item for item in streams if item.get("codec_type") == "audio"), None)
    if not video or not audio:
        raise ValueError(f"{path} must contain video and audio streams")
    duration = float(payload.get("format", {}).get("duration") or video.get("duration") or 0)
    fps = parse_rate(str(video.get("avg_frame_rate") or video.get("r_frame_rate") or "0"))
    return {
        "duration": duration,
        "width": int(video.get("width", 0)),
        "height": int(video.get("height", 0)),
        "fps": fps,
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name"),
        "audio_sample_rate": int(audio.get("sample_rate") or 0),
        "audio_channels": int(audio.get("channels") or 0),
    }


def extract_audio(path: Path, sample_rate: int) -> array.array[int]:
    raw = run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "s16le",
            "pipe:1",
        ]
    )
    samples = array.array("h")
    samples.frombytes(raw)
    if sys.byteorder != "little":
        samples.byteswap()
    if not samples:
        raise ValueError(f"no audio samples extracted from {path}")
    return samples


def envelope(samples: array.array[int], bin_size: int) -> list[float]:
    values: list[float] = []
    for start in range(0, len(samples) - bin_size + 1, bin_size):
        total = 0
        for value in samples[start : start + bin_size]:
            total += abs(value)
        values.append(total / bin_size)
    return values


def correlation(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return -1.0
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = 0.0
    left_energy = 0.0
    right_energy = 0.0
    for a, b in zip(left, right):
        da = a - left_mean
        db = b - right_mean
        numerator += da * db
        left_energy += da * da
        right_energy += db * db
    denominator = math.sqrt(left_energy * right_energy)
    return numerator / denominator if denominator > 1e-9 else -1.0


def distributed_starts(duration: float, window: float, count: int) -> list[float]:
    usable = duration - window
    if usable <= 0:
        raise ValueError("source is too short for synchronization windows")
    fractions = (0.05, 0.20, 0.38, 0.58, 0.76, 0.91)
    if count != 6:
        fractions = tuple((index + 1) / (count + 1) for index in range(count))
    return [min(usable, max(0.0, usable * value)) for value in fractions]


def measure_audio_offsets(
    source: list[float],
    final: list[float],
    bins_per_second: int,
    source_duration: float,
    expected_delay: float,
    search_radius: float,
    window: float,
    count: int,
) -> list[dict[str, float]]:
    measurements: list[dict[str, float]] = []
    window_bins = round(window * bins_per_second)
    radius_bins = round(search_radius * bins_per_second)
    expected_bins = round(expected_delay * bins_per_second)
    for source_start in distributed_starts(source_duration, window, count):
        source_index = round(source_start * bins_per_second)
        template = source[source_index : source_index + window_bins]
        best_corr = -2.0
        best_final_index = -1
        center = source_index + expected_bins
        for final_index in range(center - radius_bins, center + radius_bins + 1):
            if final_index < 0 or final_index + window_bins > len(final):
                continue
            score = correlation(template, final[final_index : final_index + window_bins])
            if score > best_corr:
                best_corr = score
                best_final_index = final_index
        if best_final_index < 0:
            raise ValueError(f"could not search final audio near source {source_start:.3f}s")
        final_start = best_final_index / bins_per_second
        measurements.append(
            {
                "source_seconds": round(source_start, 3),
                "final_seconds": round(final_start, 3),
                "delay_seconds": round(final_start - source_start, 4),
                "correlation": round(best_corr, 6),
            }
        )
    return measurements


def parse_roi(value: str, width: int, height: int) -> tuple[int, int, int, int]:
    try:
        x, y, w, h = (int(part) for part in value.split(":"))
    except (TypeError, ValueError):
        raise ValueError("face ROI must use X:Y:W:H integers") from None
    if min(x, y, w, h) < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
        raise ValueError("face ROI is outside the source frame")
    return x, y, w, h


def extract_gray_frame(path: Path, timestamp: float, roi: tuple[int, int, int, int]) -> bytes:
    x, y, w, h = roi
    return run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            f"{timestamp:.6f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-vf",
            f"crop={w}:{h}:{x}:{y},scale=64:64:flags=area,format=gray",
            "-f",
            "rawvideo",
            "pipe:1",
        ]
    )


def byte_correlation(left: bytes, right: bytes) -> float:
    if len(left) != 4096 or len(right) != 4096:
        return -1.0
    return correlation(list(left), list(right))


def measure_picture_offsets(
    source_path: Path,
    final_path: Path,
    roi: tuple[int, int, int, int],
    anchors: list[float],
    expected_delay: float,
    fps: float,
    search_frames: float,
) -> list[dict[str, float]]:
    measurements: list[dict[str, float]] = []
    half_frame = 0.5 / fps
    steps = round(search_frames * 2)
    for source_time in anchors:
        source_frame = extract_gray_frame(source_path, source_time, roi)
        best_corr = -2.0
        best_time = 0.0
        for step in range(-steps, steps + 1):
            final_time = source_time + expected_delay + step * half_frame
            if final_time < 0:
                continue
            score = byte_correlation(
                source_frame,
                extract_gray_frame(final_path, final_time, roi),
            )
            if score > best_corr:
                best_corr = score
                best_time = final_time
        measurements.append(
            {
                "source_seconds": round(source_time, 3),
                "final_seconds": round(best_time, 3),
                "delay_seconds": round(best_time - source_time, 4),
                "correlation": round(best_corr, 6),
            }
        )
    return measurements


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--expected-delay", type=float, default=0.0)
    parser.add_argument("--face-roi", required=True, help="overlay-free source ROI as X:Y:W:H")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--anchors", type=int, default=6)
    parser.add_argument("--audio-correlation", type=float, default=0.80)
    parser.add_argument("--picture-correlation", type=float, default=0.70)
    parser.add_argument("--audio-search-radius", type=float, default=0.30)
    parser.add_argument("--picture-search-frames", type=float, default=2.0)
    args = parser.parse_args()

    if args.anchors < 6:
        parser.error("at least six distributed anchors are required")
    if not args.source.is_file() or not args.final.is_file():
        parser.error("source and final files must exist")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("ffmpeg and ffprobe are required")

    source_meta = probe(args.source)
    final_meta = probe(args.final)
    errors: list[str] = []
    if final_meta["width"] != 1080 or final_meta["height"] != 1920:
        errors.append("final resolution must be 1080x1920")
    if final_meta["video_codec"] != "h264":
        errors.append("final video codec must be H.264")
    if final_meta["audio_codec"] != "aac" or final_meta["audio_sample_rate"] != 48000:
        errors.append("final audio must be AAC 48 kHz")
    if abs(final_meta["fps"] - source_meta["fps"]) > 0.01:
        errors.append("final fps must preserve the clean source fps")
    if final_meta["duration"] + 0.05 < source_meta["duration"] + args.expected_delay:
        errors.append("final duration is shorter than the delayed clean source")

    roi = parse_roi(args.face_roi, source_meta["width"], source_meta["height"])
    sample_rate = 8000
    bin_ms = 10
    bin_size = sample_rate * bin_ms // 1000
    bins_per_second = 1000 // bin_ms
    source_audio = envelope(extract_audio(args.source, sample_rate), bin_size)
    final_audio = envelope(extract_audio(args.final, sample_rate), bin_size)
    audio = measure_audio_offsets(
        source_audio,
        final_audio,
        bins_per_second,
        source_meta["duration"],
        args.expected_delay,
        args.audio_search_radius,
        3.0,
        args.anchors,
    )
    picture_anchor_times = [item["source_seconds"] + 1.5 for item in audio]
    picture = measure_picture_offsets(
        args.source,
        args.final,
        roi,
        picture_anchor_times,
        args.expected_delay,
        final_meta["fps"],
        args.picture_search_frames,
    )

    frame_seconds = 1 / final_meta["fps"]
    audio_delays = [item["delay_seconds"] for item in audio]
    picture_delays = [item["delay_seconds"] for item in picture]
    min_audio_corr = min(item["correlation"] for item in audio)
    min_picture_corr = min(item["correlation"] for item in picture)
    audio_drift = max(audio_delays) - min(audio_delays)
    picture_drift = max(picture_delays) - min(picture_delays)
    median_audio = statistics.median(audio_delays)
    median_picture = statistics.median(picture_delays)
    post_delta = median_audio - median_picture

    if min_audio_corr < args.audio_correlation:
        errors.append(
            f"minimum audio correlation {min_audio_corr:.3f} is below "
            f"{args.audio_correlation:.3f}"
        )
    if min_picture_corr < args.picture_correlation:
        errors.append(
            f"minimum picture correlation {min_picture_corr:.3f} is below "
            f"{args.picture_correlation:.3f}; choose a cleaner face ROI or fix timing"
        )
    if max(abs(value - args.expected_delay) for value in audio_delays) > frame_seconds + 0.001:
        errors.append("one or more audio anchors differ from expected delay by over one frame")
    if max(abs(value - args.expected_delay) for value in picture_delays) > frame_seconds + 0.001:
        errors.append("one or more picture anchors differ from expected delay by over one frame")
    if audio_drift > frame_seconds + 0.001:
        errors.append("audio delay drifts by over one frame")
    if picture_drift > frame_seconds + 0.001:
        errors.append("picture delay drifts by over one frame")
    if abs(post_delta) > frame_seconds + 0.001:
        errors.append("postproduction audio-to-picture offset exceeds one frame")

    report = {
        "status": "pass" if not errors else "fail",
        "source": {"path": str(args.source), **source_meta},
        "final": {"path": str(args.final), **final_meta},
        "expected_delay_seconds": args.expected_delay,
        "frame_tolerance_seconds": round(frame_seconds, 6),
        "face_roi": {"x": roi[0], "y": roi[1], "width": roi[2], "height": roi[3]},
        "audio_anchors": audio,
        "picture_anchors": picture,
        "summary": {
            "median_audio_delay_seconds": round(median_audio, 4),
            "median_picture_delay_seconds": round(median_picture, 4),
            "audio_to_picture_offset_seconds": round(post_delta, 4),
            "audio_drift_seconds": round(audio_drift, 4),
            "picture_drift_seconds": round(picture_drift, 4),
            "minimum_audio_correlation": round(min_audio_corr, 6),
            "minimum_picture_correlation": round(min_picture_corr, 6),
        },
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print(f"A/V synchronization validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(f"report written to {args.output}", file=sys.stderr)
        return 1
    print(
        f"A/V synchronization passed at {len(audio)} audio and {len(picture)} picture anchors; "
        f"median audio={median_audio:.3f}s, picture={median_picture:.3f}s, "
        f"delta={post_delta * 1000:.1f}ms"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"A/V synchronization validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
