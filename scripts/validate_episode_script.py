#!/usr/bin/env python3
"""Validate an interactive-coaching-script episode_script.json."""
from __future__ import annotations
import json
import sys
from pathlib import Path

KINDS = {"cold_open", "session_promise", "strength", "agenda", "question", "reveal", "analogy", "alternative", "pattern_bridge", "progress_check", "scorecard", "drill"}
CLAIMS = {"observed", "inference", "unknown", "production"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_episode_script.py EPISODE_SCRIPT.json", file=sys.stderr)
        return 2
    try:
        path = Path(sys.argv[1])
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            raise ValueError("top-level JSON must be an object")
        beats = data.get("beats")
        if not isinstance(beats, list) or not beats:
            raise ValueError("beats must be a non-empty list")
        ids = set()
        saw_question = False
        saw_reveal = False
        for i, beat in enumerate(beats):
            if not isinstance(beat, dict):
                raise ValueError(f"beats[{i}] must be an object")
            bid = beat.get("beat_id")
            if not bid or bid in ids:
                raise ValueError(f"beats[{i}] has missing or duplicate beat_id")
            ids.add(bid)
            if beat.get("kind") not in KINDS:
                raise ValueError(f"{bid} has unsupported kind")
            if beat.get("claim_class") not in CLAIMS:
                raise ValueError(f"{bid} has unsupported claim_class")
            if not isinstance(beat.get("source_times", []), list):
                raise ValueError(f"{bid}.source_times must be a list")
            if not isinstance(beat.get("evidence_refs", []), list):
                raise ValueError(f"{bid}.evidence_refs must be a list")
            if beat.get("kind") == "question":
                saw_question = True
                if not beat.get("question"):
                    raise ValueError(f"{bid} question is required")
                if not isinstance(beat.get("answerable_from_visible_evidence"), bool):
                    raise ValueError(f"{bid}.answerable_from_visible_evidence is required")
                if beat.get("thinking_window_seconds", 0) <= 0:
                    raise ValueError(f"{bid} needs a positive thinking window")
            if beat.get("kind") == "reveal":
                saw_reveal = True
                for key in ("observed_claims", "inference_claims", "unknowns"):
                    if key not in beat or not isinstance(beat[key], list):
                        raise ValueError(f"{bid} reveal requires list field {key}")
            if beat.get("kind") == "alternative":
                for key in ("original_action", "better_action", "tradeoff", "likely_benefit", "unknowns"):
                    if not beat.get(key) and key != "unknowns":
                        raise ValueError(f"{bid} alternative requires {key}")
                if beat.get("claim_class") != "inference":
                    raise ValueError(f"{bid} alternative must have claim_class inference")
                confidence = beat.get("confidence")
                if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                    raise ValueError(f"{bid} alternative confidence must be between 0 and 1")
            if beat.get("kind") == "drill" and not beat.get("success_condition"):
                raise ValueError(f"{bid} drill requires success_condition")
        if not saw_question or not saw_reveal:
            raise ValueError("episode must contain at least one question beat and one reveal beat")
        print(f"VALID episode script: {path}")
        print(f"beats={len(beats)} questions={sum(b.get('kind') == 'question' for b in beats)} reveals={sum(b.get('kind') == 'reveal' for b in beats)}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
