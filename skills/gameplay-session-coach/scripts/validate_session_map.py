#!/usr/bin/env python3
"""Validate a gameplay-session-coach session_map.json."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ALLOWED_STATUS = {"won", "lost", "escaped", "injured_retreat", "unresolved", "unknown"}
ALLOWED_CLASS = {"observed", "inference", "unknown"}
ALLOWED_EVIDENCE = {"frame", "frames", "audio", "transcript", "hud", "ocr", "telemetry", "metadata", "inference", "replay_test"}


def fail(message: str) -> None:
    raise ValueError(message)


def confidence(value, label: str) -> None:
    if not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
        fail(f"{label} confidence must be between 0 and 1")


def evidence_list(items, label: str) -> None:
    if items is None:
        return
    if not isinstance(items, list):
        fail(f"{label} must be a list")
    for i, entry in enumerate(items):
        if not isinstance(entry, dict):
            fail(f"{label}[{i}] must be an object")
        etype = entry.get("type")
        if etype not in ALLOWED_EVIDENCE:
            fail(f"{label}[{i}] has unsupported evidence type {etype!r}")
        if "claim" not in entry:
            fail(f"{label}[{i}] must include claim")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_session_map.py SESSION_MAP.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            fail("top-level JSON must be an object")
        source = data.get("source")
        if not isinstance(source, dict):
            fail("source object is required")
        if not source.get("path"):
            fail("source.path is required")
        if not isinstance(source.get("duration"), (int, float)) or source["duration"] <= 0:
            fail("source.duration must be positive")
        fights = data.get("fights", [])
        if not isinstance(fights, list):
            fail("fights must be a list")
        fight_ids = set()
        for index, fight in enumerate(fights):
            if not isinstance(fight, dict):
                fail(f"fights[{index}] must be an object")
            fid = fight.get("fight_id")
            if not fid or fid in fight_ids:
                fail(f"fights[{index}] has missing or duplicate fight_id")
            fight_ids.add(fid)
            start, end = fight.get("start"), fight.get("end")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or not 0 <= start < end <= source["duration"] + 0.01:
                fail(f"{fid} has invalid boundaries")
            if fight.get("status") not in ALLOWED_STATUS:
                fail(f"{fid} has unsupported status")
            if not fight.get("evidence"):
                fail(f"{fid} requires evidence")
            evidence_list(fight.get("evidence"), f"{fid}.evidence")
            for decision in fight.get("key_decisions", []):
                if not isinstance(decision, dict):
                    fail(f"{fid}.key_decisions entries must be objects")
                if not decision.get("decision_id"):
                    fail(f"{fid} decision missing decision_id")
                if decision.get("context_before") is None or decision.get("action_taken") is None or decision.get("consequence") is None:
                    fail(f"{fid} decision requires context_before, action_taken, and consequence")
        for section in ("strengths", "weaknesses"):
            patterns = data.get(section, [])
            if not isinstance(patterns, list):
                fail(f"{section} must be a list")
            for i, pattern in enumerate(patterns):
                if not isinstance(pattern, dict):
                    fail(f"{section}[{i}] must be an object")
                if not pattern.get("claim"):
                    fail(f"{section}[{i}] claim is required")
                if pattern.get("class") not in ALLOWED_CLASS:
                    fail(f"{section}[{i}] class must be observed, inference, or unknown")
                confidence(pattern.get("confidence"), f"{section}[{i}]")
                for fid in pattern.get("supporting_fights", []):
                    if fid not in fight_ids:
                        fail(f"{section}[{i}] references unknown fight {fid}")
        priorities = data.get("priorities", [])
        if not isinstance(priorities, list) or len(priorities) > 3:
            fail("priorities must be a list with no more than three entries")
        for i, priority in enumerate(priorities):
            if not isinstance(priority, dict):
                fail(f"priorities[{i}] must be an object")
            required = ("priority_id", "rank", "title", "behavior_to_change", "supporting_fights", "observed_consequence", "alternative", "counterfactual", "drill")
            for key in required:
                if key not in priority:
                    fail(f"priorities[{i}] missing {key}")
            for fid in priority.get("supporting_fights", []):
                if fid not in fight_ids:
                    fail(f"priorities[{i}] references unknown fight {fid}")
            cf = priority["counterfactual"]
            if cf.get("class") != "inference":
                fail(f"priorities[{i}] counterfactual must be inference")
            confidence(cf.get("confidence"), f"priorities[{i}].counterfactual")
            if not isinstance(cf.get("unknowns"), list):
                fail(f"priorities[{i}] counterfactual.unknowns must be a list")
            drill = priority["drill"]
            if not drill.get("name") or not drill.get("success_condition"):
                fail(f"priorities[{i}] requires a measurable drill")
        objectives = data.get("learning_objectives", [])
        if not isinstance(objectives, list) or len(objectives) > 3:
            fail("learning_objectives must contain no more than three entries")
        for i, objective in enumerate(objectives):
            for key in ("objective_id", "rank", "title", "opening_line", "question_for_player", "reveal", "supporting_fights", "drill"):
                if key not in objective:
                    fail(f"learning_objectives[{i}] missing {key}")
            for fid in objective.get("supporting_fights", []):
                if fid not in fight_ids:
                    fail(f"learning_objectives[{i}] references unknown fight {fid}")
        evidence_list(data.get("evidence_ledger", []), "evidence_ledger")
        print(f"VALID session map: {path}")
        print(f"fights={len(fights)} strengths={len(data.get('strengths', []))} weaknesses={len(data.get('weaknesses', []))} priorities={len(priorities)} objectives={len(objectives)}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
