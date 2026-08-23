---
name: pure-gaming-highlights
description: Create, analyze, and refine pure gaming highlight videos from livestreams or gameplay files. Use when the user wants game-focused highlight reels, complete fights, tactical sequences, ranked clips, or long-form gaming edits with no meme videos, reaction stickers, or decorative overlays.
---

# Pure Gaming Highlights

## Overview

Use this skill to turn a livestream or gameplay recording into a focused highlight edit built around complete fights, tactical decisions, strong outcomes, and concise connective gameplay. Use **Kinocut** for source inspection, timeline assembly, audio handling, export, and quality checks; use optional local or game-specific analyzers only to propose candidates.

This is a **pure gameplay** workflow. Do not add meme cutaways, reaction stickers, downloaded meme footage, copyrighted characters, or decorative reaction graphics unless the user explicitly opts back in. Minimal editorial typography is allowed when it clarifies a round, location, tactical beat, or outcome.

## Workflow

1. **Confirm inputs and rights.** Obtain a local video file or an authorized download. Record the source path, title/creator, duration, resolution, frame rate, audio tracks, and usage permission. Do not bypass authentication, paywalls, DRM, or platform restrictions. If reuse rights are unclear, state that the edit is for review and require permission before publishing.
2. **Inspect the source.** Run `scripts/inspect_source.py` or Kinocut metadata commands. Identify gameplay, combat, traversal, inventory/loot, menus, sponsor material, deaths, extractions, and dead air. Use transcript, audio peaks, motion, scene changes, and visual/game-specific signals as candidate evidence, not as final editorial decisions.
3. **Build a contiguous highlight map.** Use `references/highlight_map_schema.md`. Each fight must be represented as one or more contiguous source ranges covering approach or setup, first contact, escalation, decisive moment, and immediate result. Do not cut away during an unresolved firefight. If a fight is too long, remove only clearly redundant pauses while retaining the causal chain and outcome.
4. **Choose the format.** Default to a **3–5 minute proper highlight** for a full session. Use a shorter cut only when the user asks for a teaser or short. Keep loot and inventory footage as short reward/context beats; target no more than 20–25% of total runtime unless the user specifically wants a loot-focused video.
5. **Plan the visual system.** Prefer the source’s native aspect ratio unless the target platform requires another format. Use a bold condensed or heavy sans-serif font, high contrast, safe margins, restrained all-caps labels, and consistent placement. Use text only for useful context such as `ROUND 2`, `FIRST CONTACT`, `LOW HP`, `EXTRACTION`, or `FIGHT WON`. Do not place text over the weapon sightline, minimap, kill feed, subtitles, or face/hand camera.
6. **Assemble in Kinocut.** Encode the selected ranges into a Kinocut timeline. Preserve streamer commentary, game audio, and meaningful reactions. Use hard cuts or restrained transitions; do not use effects to hide missing continuity. Add only subtle, original audio accents when they support a confirmed impact, transition, or outcome. Keep dialogue intelligible and avoid clipping.
7. **Review before polishing.** Run Kinocut’s video quality and design checks, inspect representative frames at the hook, each fight’s first contact and outcome, loot bridges, and final extraction/death, and measure duration, codecs, frame rate, dimensions, and loudness. Use `scripts/generate_review_template.py` to create the review record.
8. **Self-critique brutally.** Score the ten-point checklist in the generated report. Timestamp every issue. Pay special attention to whether a fight starts too late, ends too early, or is interrupted by loot, labels, or transitions. If the score is below the user’s threshold, revise the map and rerender rather than merely describing the problem. Keep an iteration counter and stop at the agreed maximum.
9. **Deliver transparently.** Provide the final MP4, editable Kinocut timeline, highlight map, review report, source/rights notes, and any project-specific assets. Never claim publish-ready if rights are uncertain or a required QC gate failed.

## Highlight selection rules

- Rank **complete engagements** above isolated kills. A clean kill without its setup may be a short insert, but it should not replace a stronger complete fight.
- Preserve causality: show why the player entered, what changed, how the player adapted, and what happened immediately afterward.
- Alternate intensity and recovery. Use a short loot, reload, extraction, or traversal beat as connective tissue, then return to gameplay.
- Remove sponsor segments, long menu navigation, repeated item sorting, loading screens, and dead air unless they contain essential context or a deliberate emotional payoff.
- Prefer distinct encounters and locations. Avoid reusing the same source shot, angle, or identical reaction unless repetition is itself the story.
- Use the hook quickly, but do not spoil every outcome in the first seconds. A strong opening can begin with contact, danger, or a tactical decision and then return to the setup.
- Preserve original dialogue when it explains the moment. Do not fabricate quotes or describe an event that is not visible or audible in the source.

## Quality gate

Use the following ten checks, each scored 0–10 for a total out of 100:

1. **Pacing:** cuts and sequences move with purpose without rushing complete fights.
2. **Hook strength:** the first 5–10 seconds establish danger, skill, or a clear objective.
3. **Fight continuity:** every featured engagement reaches a visible kill, escape, death, extraction, or other outcome.
4. **Visual cohesion:** exposure, color, aspect ratio, and source quality feel consistent.
5. **Typography:** labels are distinctive, readable, safe, and useful rather than decorative.
6. **Audio clarity:** commentary, game audio, and music are balanced without clipping.
7. **Energy curve:** the edit builds, releases, and finishes with a meaningful payoff.
8. **Dead-air control:** menus, repeated looting, and filler are compressed without removing context.
9. **Platform readiness:** requested duration, resolution, frame rate, codec, aspect ratio, and loudness are satisfied.
10. **Retention test:** an honest viewer would continue watching the next encounter.

A score of **90/100 or higher** is the default publish threshold when the user requests one. If the edit does not reach the threshold within the maximum iterations, deliver the strongest version and state the exact shortfall.

## Optional repository integrations

Read `references/repository_guide.md` before adding external detectors. Prefer optional integrations over hard dependencies:

- **VideoHighlighter** can propose candidates from local scene, motion, audio, object, action, and transcript signals.
- **Crispy** can provide game-specific visual highlight detection where its supported models apply.
- **Clipception** can provide engagement-ranking ideas using audio, laughter, excitement, and transcription, but adds external-model dependencies.
- **Twitch Stream Highlights Detection** is a research reference for multimodal audio, movement, and chat scoring rather than a drop-in editor.

Never let an automated score override continuity review. A detector may find a kill while missing the setup or aftermath that makes the fight meaningful.

## Bundled resources

- `scripts/inspect_source.py`: extract source metadata through `ffprobe`.
- `scripts/validate_edit_map.py`: validate contiguous clip ranges, complete-fight flags, excluded ranges, and loot-ratio warnings.
- `scripts/generate_review_template.py`: create a timestamped ten-point review report.
- `references/highlight_map_schema.md`: reusable edit-map format and examples.
- `references/repository_guide.md`: researched repository comparison and integration guidance.
- `references/kinocut_workflow.md`: command patterns and operational cautions for Kinocut.
