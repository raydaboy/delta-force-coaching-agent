#!/usr/bin/env python3
"""Fail-closed validation for a source-specific session workbook/playbook input."""
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_LESSON_FIELDS = ("lesson_id", "title", "source_window", "snapshot_id", "observed", "inferred", "unknown", "decision_point", "alternative", "cue", "drill", "reflection_prompt")
REQUIRED_DRILL_FIELDS = ("trigger", "action", "success_condition", "scope")
GENERIC_ALTERNATIVE = re.compile(r"^(use|take|find) (the )?(cover|hard cover)[.!]?$", re.I)


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc


def validate(workbook: dict, snapshots: dict, require_files: bool = False) -> list[str]:
    errors: list[str] = []
    for field in ("title", "player_goal", "session_summary", "strengths", "priorities", "lessons", "next_session_rules", "practice_plan", "evidence_limits"):
        if not workbook.get(field):
            errors.append(f"missing workbook field: {field}")
    if len(workbook.get("priorities", [])) > 3:
        errors.append("workbook may contain at most three priorities")
    if not 1 <= len(workbook.get("lessons", [])) <= 6:
        errors.append("workbook needs one to six selected lessons")
    snapshot_map = {item.get("id"): item for item in snapshots.get("snapshots", []) if item.get("id")}
    seen_ids: set[str] = set()
    for index, lesson in enumerate(workbook.get("lessons", []), start=1):
        prefix = f"lesson {index}"
        for field in REQUIRED_LESSON_FIELDS:
            if field not in lesson or lesson.get(field) in (None, ""):
                errors.append(f"{prefix}: missing {field}")
        lesson_id = lesson.get("lesson_id")
        if lesson_id in seen_ids:
            errors.append(f"duplicate lesson_id: {lesson_id}")
        seen_ids.add(lesson_id)
        window = lesson.get("source_window", {})
        try:
            start, decision, outcome, end = (float(window[key]) for key in ("start", "decision", "outcome", "end"))
            if not start <= decision <= outcome <= end:
                errors.append(f"{prefix}: source_window must be ordered start <= decision <= outcome <= end")
        except (KeyError, TypeError, ValueError):
            errors.append(f"{prefix}: invalid source_window")
        for evidence in ("observed", "inferred", "unknown"):
            if not isinstance(lesson.get(evidence), list):
                errors.append(f"{prefix}: {evidence} must be a list")
        alternative = lesson.get("alternative", {})
        action = str(alternative.get("action", "")).strip()
        for field in ("action", "tradeoff", "likely_benefit"):
            if not alternative.get(field):
                errors.append(f"{prefix}: alternative missing {field}")
        if GENERIC_ALTERNATIVE.match(action) or len(action.split()) < 4:
            errors.append(f"{prefix}: local alternative is too generic")
        if not lesson.get("cue") or len(str(lesson.get("cue")).split()) > 9:
            errors.append(f"{prefix}: cue must contain one to nine words")
        drill = lesson.get("drill", {})
        for field in REQUIRED_DRILL_FIELDS:
            if not drill.get(field):
                errors.append(f"{prefix}: drill missing {field}")
        snapshot = snapshot_map.get(lesson.get("snapshot_id"))
        if not snapshot:
            errors.append(f"{prefix}: snapshot_id is not present in snapshot manifest")
        elif require_files:
            path = snapshot.get("path")
            if not path or not Path(path).exists():
                errors.append(f"{prefix}: snapshot file unavailable")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--snapshot-manifest", type=Path, required=True)
    parser.add_argument("--require-snapshot-files", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(read_json(args.workbook), read_json(args.snapshot_manifest), args.require_snapshot_files)
    except ValueError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
    result = {"valid": not errors, "errors": errors}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
