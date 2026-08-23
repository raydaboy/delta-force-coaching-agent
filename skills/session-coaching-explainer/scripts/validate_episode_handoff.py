#!/usr/bin/env python3
"""Validate a session-coaching-explainer scene recipe or episode handoff."""
from __future__ import annotations
import json
import sys
from pathlib import Path

KINDS = {"live_action", "consequence", "rewind", "question", "evidence_panel", "causal_timeline", "tactical_board", "alternative_compare", "pattern_bridge", "scorecard", "drill"}
CLAIMS = {"observed", "inference", "unknown", "production"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_episode_handoff.py SCENE_RECIPE.json", file=sys.stderr)
        return 2
    try:
        path = Path(sys.argv[1])
        data = json.loads(path.read_text())
        scenes = data.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            raise ValueError("scenes must be a non-empty list")
        ids = set()
        last_end = 0.0
        kinds = []
        for i, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                raise ValueError(f"scenes[{i}] must be an object")
            sid = scene.get("scene_id")
            if not sid or sid in ids:
                raise ValueError(f"scenes[{i}] has missing or duplicate scene_id")
            ids.add(sid)
            kind = scene.get("kind")
            if kind not in KINDS:
                raise ValueError(f"{sid} has unsupported scene kind")
            kinds.append(kind)
            start, duration = scene.get("start"), scene.get("duration")
            if not isinstance(start, (int, float)) or not isinstance(duration, (int, float)) or start < 0 or duration <= 0:
                raise ValueError(f"{sid} has invalid start/duration")
            if start + duration < last_end - 0.01:
                raise ValueError(f"{sid} overlaps a prior scene in the linear recipe")
            last_end = start + duration
            if scene.get("claim_class") not in CLAIMS:
                raise ValueError(f"{sid} has unsupported claim_class")
            if not isinstance(scene.get("evidence_refs", []), list):
                raise ValueError(f"{sid}.evidence_refs must be a list")
            if kind in {"live_action", "consequence", "rewind"} and not scene.get("source_times"):
                raise ValueError(f"{sid} requires source_times")
            if kind == "question":
                if not scene.get("question"):
                    raise ValueError(f"{sid} requires question")
                if scene.get("thinking_window_seconds", 0) <= 0:
                    raise ValueError(f"{sid} requires thinking_window_seconds")
            if kind == "evidence_panel":
                for key in ("observed_text", "inferred_text", "unknown_text"):
                    if not scene.get(key):
                        raise ValueError(f"{sid} requires {key}")
            if kind == "alternative_compare":
                for key in ("original_action", "alternative_action", "tradeoff", "unknowns"):
                    if key != "unknowns" and not scene.get(key):
                        raise ValueError(f"{sid} requires {key}")
                if scene.get("claim_class") != "inference":
                    raise ValueError(f"{sid} alternative must be inference")
            if kind == "tactical_board" and not scene.get("model_disclaimer"):
                raise ValueError(f"{sid} tactical board needs model_disclaimer")
            if kind == "drill" and not scene.get("success_condition"):
                raise ValueError(f"{sid} drill requires success_condition")
        if "question" in kinds and "evidence_panel" not in kinds:
            raise ValueError("a question scene requires a later evidence_panel reveal")
        if "alternative_compare" not in kinds:
            raise ValueError("episode requires at least one alternative_compare scene")
        if "drill" not in kinds:
            raise ValueError("episode requires at least one drill scene")
        print(f"VALID episode handoff: {path}")
        print(f"scenes={len(scenes)} duration={last_end:.2f}s kinds={','.join(dict.fromkeys(kinds))}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
