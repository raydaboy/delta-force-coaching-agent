---
name: session-coaching-explainer
description: Produce full-session gameplay coaching videos from a validated session map and interactive episode script. Use when the user wants the entire recording turned into an agenda-led, pause-and-explain lesson with action-first replays, rewinds, tactical UI, questions, alternatives, drills, HyperFrames composition, local narration, and Kinocut finishing.
---

# Session Coaching Explainer

## Purpose

Turn a validated `gameplay-session-coach` map and `interactive-coaching-script` episode into one coherent coaching video covering the whole session. The result should feel like an interactive performance review: show the action, let the consequence land, ask a question, rewind to the decision, explain what was known, show the causal result, compare a realistic alternative, bridge to the session pattern, and finish with drills.

Use HyperFrames for composition, deterministic stills, annotations, tactical boards, timelines, questions, alternatives, and drill cards. Use local speech synthesis or prepared narration audio for voice. Use Kinocut for source extraction, audio mix, loudness normalization, peak safety, export, and QC.

## Inputs and outputs

Required inputs:

- `session_map.json` or `session_summary.json`.
- `episode_script.json`.
- Source gameplay video and audio.
- Evidence frames or the ability to extract them.

Outputs:

- `session_coaching_explainer.mp4`.
- `hyperframes/` project and composition HTML.
- `scene_manifest.json`.
- `narration.wav` and the spoken-text source.
- `kinocut_finishing_timeline.json`.
- `final_qc_report.md` and machine-readable QC receipts.

## Production workflow

### 1. Verify the script contract

Confirm that every episode beat has source times, a claim class, evidence references, spoken text or a scene-only instruction, visual plan, pause duration when needed, and uncertainty. Refuse to render a claim that lacks evidence references unless it is clearly labelled as an analogy or production direction.

### 2. Build the full-session story arc

Use this default visual order:

`cold open action → consequence → session promise → strengths → agenda → question → rewind → causal UI → tactical board → alternative → pattern bridge → resumed evidence → progress check → scorecard → drills`

Do not make every fight a full explainer. Use a few deep lessons and short pattern bridges for the rest. Preserve the natural action and audio before switching to analysis.

### 3. Use the action-first rewind pattern

For each major lesson:

1. Show the gameplay action at normal speed.
2. Show the immediate result: damage, displacement, retreat, kill, escape, death, or unresolved cutoff.
3. Add a restrained rewind effect using a real reverse-motion clip and a clear `REWIND / FIND THE DECISION` label.
4. Freeze the decision frame.
5. Animate the question and allow thinking time.
6. Reveal observed facts, then inference, then unknowns.
7. Animate the causal timeline and relevant geometry.
8. Compare the original choice with the likely alternative and its trade-off.
9. Resume the source outcome or disclose that it remains unresolved.

Never use a rewind to hide the consequence. The viewer should understand what happened before being told what it meant.

### 4. Build semantic UI, not decoration

Prefer:

- `OBSERVED`, `INFERRED`, and `UNKNOWN` evidence chips;
- causal timelines such as `SEES → CHOOSES → EFFECT → CONSEQUENCE`;
- resource or risk meters for utility, health, ammo, time, and exposure;
- line-of-sight cones, cover zones, route arrows, and tactical boards;
- before/after comparison screens;
- question cards and reveal cards;
- measurable drill cards.

Avoid memes, stickers, reaction graphics, decorative HUD clutter, fake enemy positions, fake telemetry, and UI that obscures the source evidence.

### 5. Handle enemy-perspective explanations safely

If showing what the enemy could plausibly see, label the scene `ENEMY VIEW — INFERRED FROM VISIBLE GEOMETRY`. Use only angles, cover gaps, stationary windows, and routes supported by the source. Do not draw an unseen enemy or claim hidden intent. State the exact unknowns in narration or on screen.

### 6. Mix and finish with Kinocut

Keep gameplay audio during action and consequence. Duck or lower it under narration. Normalize the final mix near −16 LUFS, then apply a conservative true-peak safety pass below −1.5 dBTP when required by QC. Export H.264/AAC MP4 at the source’s intended aspect ratio and frame rate.

Record the finishing timeline with source clips, narration, volumes, fades, normalization target, peak safety, and export settings.

### 7. Run QC

Run composition checks before expensive renders. After rendering, inspect contact sheets at the cold open, consequence, rewind, question, tactical board, alternative, resumed outcome, scorecard, and drill. Verify:

- action precedes explanation;
- questions appear before reveals;
- every overlay matches visible evidence;
- the session agenda is readable;
- the story does not over-focus on one fight;
- unresolved fights remain unresolved;
- strengths and weaknesses match the written report;
- audio is intelligible and peak-safe;
- no memes or unrelated decorative elements slipped in.

## Handoff commands

Use the project-specific HyperFrames CLI or Kinocut wrapper available in the environment. A typical sequence is:

```bash
kino hyperframes-init session-coaching --video SOURCE --resolution landscape --skip-transcribe
npx --no-install hyperframes check
npx --no-install hyperframes render -o session_coaching_hyperframes.mp4 --fps 30 --quality high
kino normalize-audio session_coaching_hyperframes.mp4 -l -17 -o session_coaching_safe.mp4
kino video-quality-check session_coaching_safe.mp4 --format json > quality_check.json
```

The exact commands may vary by installed version. Never skip validation to save time.

## Bundled resources

Read `references/full_session_explainer_workflow.md` for the complete production pattern. Read `references/hyperframes_ui_patterns.md` for tactical UI recipes. Read `references/episode_scene_schema.md` before converting scripts into scenes. Copy `templates/session_scene_recipe.json` and `templates/kinocut_finishing_timeline.json` for new projects. Use `scripts/validate_episode_handoff.py` before rendering.
