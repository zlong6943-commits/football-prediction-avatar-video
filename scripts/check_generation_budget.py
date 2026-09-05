#!/usr/bin/env python3
"""Block a HeyGen submit or retry that could exceed installed spending caps."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_MAX_USD = 2.0
EXPLICIT_JOB_OVERRIDE_MAX_USD = 4.0
INSTALLATION_MAX_CREDITS = 40.0
PREFERRED_CREDITS = 29.0
ALLOWED_CONFIDENCE = {"guaranteed", "conservative_upper_bound"}
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def fail(message: str) -> None:
    raise SystemExit(f"generation budget check failed: {message}")


def finite_number(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        fail(f"{label} must be a finite number")
    value = float(value)
    if value < 0:
        fail(f"{label} must not be negative")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_job_usd_override(
    approvals: dict[str, Any], job: Path, usd_cap: float, transport: str
) -> None:
    """Allow a narrowly scoped user-authorized API cap above the default ceiling."""

    if usd_cap <= DEFAULT_MAX_USD + 1e-9:
        return
    if usd_cap > EXPLICIT_JOB_OVERRIDE_MAX_USD + 1e-9:
        fail(
            f"USD cap {usd_cap:.2f} exceeds explicit job-override maximum "
            f"{EXPLICIT_JOB_OVERRIDE_MAX_USD:.2f}"
        )

    override = approvals.get("api_budget_override") or {}
    if not isinstance(override, dict) or override.get("approved") is not True:
        fail(
            f"USD cap {usd_cap:.2f} exceeds default maximum {DEFAULT_MAX_USD:.2f} "
            "without an explicit per-job API budget authorization"
        )
    if override.get("scope") != job.name:
        fail("api_budget_override.scope must exactly match the current job directory name")
    if override.get("provider") != "HeyGen official API" or transport != "api":
        fail("the per-job USD override is valid only for the HeyGen official API route")
    override_cap = finite_number(override.get("usd_hard_cap"), "api_budget_override.usd_hard_cap")
    if abs(override_cap - usd_cap) > 1e-9:
        fail("api_budget_override.usd_hard_cap must match hard_caps.usd")
    authorization_text = str(override.get("authorization_text", "")).strip()
    if "4美元" not in authorization_text or "用api" not in authorization_text.lower():
        fail("api_budget_override must preserve the user's API and 4-dollar authorization text")
    if not str(override.get("authorized_at", "")).strip():
        fail("api_budget_override.authorized_at is required")
    if override.get("paid_retries_allowed") is not False:
        fail("api_budget_override.paid_retries_allowed must be false")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path, help="Job directory containing generation-budget.json")
    parser.add_argument("--stage", choices=("preflight", "postflight"), required=True)
    args = parser.parse_args()

    budget_path = args.job / "generation-budget.json"
    approvals_path = args.job / "approvals.json"
    if not budget_path.is_file():
        fail(f"missing {budget_path}")
    if not approvals_path.is_file():
        fail(f"missing {approvals_path}")

    budget = json.loads(budget_path.read_text(encoding="utf-8"))
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
    if not isinstance(budget, dict):
        fail("generation-budget.json root must be an object")

    caps = budget.get("hard_caps") or {}
    usd_cap = finite_number(caps.get("usd"), "hard_caps.usd")
    credit_cap = finite_number(caps.get("credits"), "hard_caps.credits")
    if credit_cap > INSTALLATION_MAX_CREDITS + 1e-9:
        fail(
            f"credit cap {credit_cap:.2f} exceeds installed maximum "
            f"{INSTALLATION_MAX_CREDITS:.0f}"
        )

    if budget.get("paid_retries_allowed") is not False:
        fail("paid_retries_allowed must be false")

    script = approvals.get("script") or {}
    script_file = args.job / str(script.get("file", ""))
    approved_hash = str(script.get("sha256", "")).lower()
    budget_hash = str(budget.get("approved_script_sha256", "")).lower()
    if script.get("approved") is not True or not script_file.is_file():
        fail("approved script record is missing or invalid")
    if not SHA256_RE.fullmatch(approved_hash) or sha256_file(script_file) != approved_hash:
        fail("approved script file/hash mismatch")
    if budget_hash != approved_hash:
        fail("budget quote is not tied to the currently approved script hash")

    route = budget.get("planned_route") or {}
    if route.get("provider") != "HeyGen":
        fail("planned_route.provider must be HeyGen")
    if route.get("transport") not in {"web", "api"}:
        fail("planned_route.transport must be web or api")
    validate_job_usd_override(approvals, args.job, usd_cap, str(route.get("transport")))
    if not str(route.get("model", "")).strip():
        fail("planned_route.model is required")
    if route.get("selection_basis") != "lowest_compatible_model":
        fail("planned_route.selection_basis must be lowest_compatible_model")
    if route.get("quote_confidence") not in ALLOWED_CONFIDENCE:
        fail("quote_confidence must be guaranteed or conservative_upper_bound")
    if not str(route.get("pricing_source", "")).strip():
        fail("planned_route.pricing_source is required")
    duration = finite_number(
        route.get("duration_upper_bound_seconds"),
        "planned_route.duration_upper_bound_seconds",
    )
    if duration <= 0:
        fail("duration_upper_bound_seconds must be positive")

    ledger = budget.get("ledger")
    if not isinstance(ledger, list) or not ledger:
        fail("ledger must contain charged and/or planned billable line items")

    actual_usd = 0.0
    actual_credits = 0.0
    planned_usd = 0.0
    planned_credits = 0.0
    planned_count = 0
    for index, item in enumerate(ledger):
        if not isinstance(item, dict):
            fail(f"ledger[{index}] must be an object")
        status = item.get("status")
        if status not in {"charged", "planned", "free", "cancelled"}:
            fail(f"ledger[{index}].status is invalid")
        usd = finite_number(item.get("usd", 0), f"ledger[{index}].usd")
        credits = finite_number(item.get("credits", 0), f"ledger[{index}].credits")
        if status == "charged":
            actual_usd += usd
            actual_credits += credits
        elif status == "planned":
            planned_count += 1
            planned_usd += usd
            planned_credits += credits

    cumulative_usd = actual_usd + planned_usd
    cumulative_credits = actual_credits + planned_credits
    if cumulative_usd > usd_cap + 1e-9:
        fail(f"cumulative worst-case USD {cumulative_usd:.2f} exceeds cap {usd_cap:.2f}")
    if cumulative_credits > credit_cap + 1e-9:
        fail(
            f"cumulative worst-case credits {cumulative_credits:.2f} exceeds cap "
            f"{credit_cap:.0f}"
        )

    if args.stage == "preflight" and planned_count != 1:
        fail("preflight must contain exactly one planned paid submission and no paid retry")
    if args.stage == "postflight":
        if planned_count:
            fail("postflight must replace every planned line item with charged/free/cancelled status")
        actual = budget.get("actual_total") or {}
        if abs(finite_number(actual.get("usd"), "actual_total.usd") - actual_usd) > 0.005:
            fail("actual_total.usd does not match the charged ledger")
        if abs(
            finite_number(actual.get("credits"), "actual_total.credits") - actual_credits
        ) > 0.005:
            fail("actual_total.credits does not match the charged ledger")

    preferred_note = (
        "within preferred 29-credit target"
        if cumulative_credits <= PREFERRED_CREDITS + 1e-9
        else "above preferred 29-credit target but within hard cap"
    )
    print(
        f"generation budget check passed ({args.stage}): "
        f"USD {cumulative_usd:.2f}/{usd_cap:.2f}, "
        f"credits {cumulative_credits:.2f}/{credit_cap:.0f}; {preferred_note}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"generation budget check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
