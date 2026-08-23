#!/usr/bin/env python3
"""Validate a pure-gaming-highlight edit map.

Expected JSON shape:
{
  "source_file": "...",
  "target_duration_seconds": 240,
  "clips": [
    {"label": "Round 1", "kind": "combat", "source_start": 10,
     "source_end": 42, "keep_complete": true}
  ],
  "excluded_ranges": [{"start": 100, "end": 130, "reason": "sponsor"}]
}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_KINDS = {"combat", "loot", "traverse", "extraction", "transition", "context"}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate(payload: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    clips = payload.get("clips")
    if not isinstance(clips, list) or not clips:
        fail("clips must be a non-empty list", errors)
        return errors, warnings

    target = payload.get("target_duration_seconds")
    if not isinstance(target, (int, float)) or target <= 0:
        fail("target_duration_seconds must be positive", errors)

    exclusions = payload.get("excluded_ranges", [])
    for index, exclusion in enumerate(exclusions):
        if not isinstance(exclusion, dict):
            fail(f"excluded_ranges[{index}] must be an object", errors)
            continue
        if exclusion.get("start", 0) >= exclusion.get("end", 0):
            fail(f"excluded_ranges[{index}] must have start < end", errors)

    total = 0.0
    loot_total = 0.0
    previous_end = None
    for index, clip in enumerate(clips):
        prefix = f"clips[{index}]"
        if not isinstance(clip, dict):
            fail(f"{prefix} must be an object", errors)
            continue
        start = clip.get("source_start")
        end = clip.get("source_end")
        kind = clip.get("kind")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            fail(f"{prefix} requires numeric source_start and source_end", errors)
            continue
        if start < 0 or end <= start:
            fail(f"{prefix} must have 0 <= source_start < source_end", errors)
        if previous_end is not None and start < previous_end:
            warnings.append(f"{prefix} overlaps or backtracks from the previous source range")
        previous_end = end
        if kind not in ALLOWED_KINDS:
            fail(f"{prefix}.kind must be one of {sorted(ALLOWED_KINDS)}", errors)
        duration = max(0.0, end - start)
        total += duration
        if kind == "loot":
            loot_total += duration
        if kind == "combat" and clip.get("keep_complete") is not True:
            fail(f"{prefix} is combat but keep_complete is not true", errors)
        if kind == "combat" and not clip.get("outcome"):
            warnings.append(f"{prefix} has no explicit outcome; record kill, escape, death, extraction, or other result")
        label = clip.get("label")
        if not isinstance(label, str) or not label.strip():
            fail(f"{prefix}.label must be a non-empty string", errors)

    if isinstance(target, (int, float)) and total:
        difference = abs(total - target)
        if difference > 1.0:
            warnings.append(f"clip duration sum is {total:.2f}s versus target {target:.2f}s")
    if total and loot_total / total > 0.25:
        warnings.append(f"loot footage is {loot_total / total:.1%} of the map; keep it under roughly 20–25% unless explicitly requested")
    if not any(clip.get("kind") == "combat" for clip in clips if isinstance(clip, dict)):
        fail("the map must contain at least one combat segment", errors)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.map.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read edit map: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(payload)
    result = {"valid": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2) + "\n")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
