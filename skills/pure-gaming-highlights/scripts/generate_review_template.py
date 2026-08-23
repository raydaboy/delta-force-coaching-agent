#!/usr/bin/env python3
"""Generate a timestamped review template for a gaming highlight."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

CHECKS = [
    ("Pacing", "Do cuts and sequence lengths move with purpose without rushing fights?"),
    ("Hook Strength", "Does the first 5–10 seconds establish danger, skill, or an objective?"),
    ("Fight Continuity", "Does every featured fight reach a visible outcome?"),
    ("Visual Cohesion", "Are exposure, color, framing, and source quality consistent?"),
    ("Typography", "Are labels distinctive, readable, safe, and useful?"),
    ("Audio Clarity", "Are commentary and game audio intelligible without clipping?"),
    ("Energy Curve", "Does the edit build, release, and finish with a meaningful payoff?"),
    ("Dead-Air Control", "Are menus, repeated loot actions, and filler compressed?"),
    ("Platform Readiness", "Does the export satisfy requested duration, codec, frame rate, dimensions, aspect ratio, and loudness?"),
    ("Retention Test", "Would a viewer continue into the next encounter?"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--video", default="[path to rendered video]")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"# Pure Gaming Highlight Review — Attempt #{args.attempt}",
        "",
        f"- Render: `{args.video}`",
        f"- Review generated: {stamp}",
        "- Scope: no meme videos, reaction stickers, or decorative graphics; gameplay and useful editorial typography only.",
        "",
        "## Scores",
        "",
        "| Check | Score (0–10) | Timestamped evidence | Fix or keep |",
        "|---|---:|---|---|",
    ]
    for name, question in CHECKS:
        lines.append(f"| **{name}** |  | {question} |  |")
    lines += [
        "",
        "**Overall score:** /100",
        "",
        "**Grade:**",
        "",
        "## Issues Found",
        "",
        "1. `[00:00]` ",
        "2. `[00:00]` ",
        "3. `[00:00]` ",
        "",
        "## What Worked",
        "",
        "Record the strongest complete fight, best tactical decision, clearest outcome, and most effective typography or audio choice.",
        "",
        "## Recommended Fixes",
        "",
        "1. ",
        "2. ",
        "3. ",
        "",
        "## Publish Decision",
        "",
        "- [ ] Ready to publish",
        "- [ ] Revise and rerender",
        "- [ ] Deliver best available version with caveats",
        "",
        "Do not call the video publish-ready when source rights are unclear or a required technical gate fails.",
    ]
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
