#!/usr/bin/env python3
"""Extract spoken narration from an interactive episode script."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_narration.py EPISODE_SCRIPT.json NARRATION.txt", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text())
    lines = []
    opening = data.get("opening", {}).get("spoken_text")
    if opening:
        lines.append(opening.strip())
    for beat in data.get("beats", []):
        text = beat.get("spoken_text")
        if text:
            lines.append(text.strip())
        if beat.get("kind") == "question" and beat.get("question"):
            lines.append(beat["question"].strip())
    Path(sys.argv[2]).write_text("\n\n".join(lines).strip() + "\n")
    print(f"WROTE {sys.argv[2]} paragraphs={len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
