#!/usr/bin/env python3
"""Build a compact handoff summary from a gameplay-session-coach session map."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: build_session_summary.py SESSION_MAP.json OUTPUT.json", file=sys.stderr)
        return 2
    source_path, output_path = map(Path, sys.argv[1:])
    data = json.loads(source_path.read_text())
    priorities = sorted(data.get("priorities", []), key=lambda p: p.get("rank", 999))
    strengths = data.get("strengths", [])
    weaknesses = data.get("weaknesses", [])
    objectives = data.get("learning_objectives", [])
    if not objectives:
        objectives = []
        for p in priorities[:3]:
            objectives.append({
                "objective_id": f"objective_from_{p.get('priority_id', 'priority')}",
                "rank": p.get("rank", len(objectives) + 1),
                "title": p.get("title", "Priority correction"),
                "opening_line": f"Today we will work on {p.get('title', 'this priority').lower()}.",
                "question_for_player": "What would you choose before seeing the replay?",
                "reveal": p.get("alternative", "Review the evidence and compare the likely alternative."),
                "supporting_fights": p.get("supporting_fights", []),
                "visual_plan": ["action_first", "rewind", "causal_timeline", "alternative"],
                "drill": p.get("drill", {})
            })
    output = {
        "session_summary": data.get("session_summary", ""),
        "source": data.get("source", {}),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "priorities": priorities[:3],
        "learning_objectives": objectives[:3],
        "fight_count": len(data.get("fights", [])),
        "fights": data.get("fights", []),
        "unknowns": data.get("unknowns", []),
        "evidence_ledger": data.get("evidence_ledger", [])
    }
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"WROTE {output_path}")
    print(f"objectives={len(output['learning_objectives'])} priorities={len(output['priorities'])} fights={output['fight_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
