# Full-Session Coaching Explainer Workflow

## Contents

1. Episode architecture
2. Deep lessons and pattern bridges
3. HyperFrames scene types
4. Audio and narration
5. Kinocut finishing
6. QC

## 1. Episode architecture

Use the validated episode script as the source of truth. The recommended structure is:

`cold open → consequence → session promise → strengths → agenda → question → rewind → causal explanation → tactical board → alternative → pattern bridge → resumed source → scorecard → drills`

The action must happen before its interpretation. The viewer should see what the decision caused before the coach explains the decision.

## 2. Deep lessons and pattern bridges

Choose two or three deep lessons. For the remaining fights, use short pattern bridges that show recurrence or improvement. Do not create a full tactical-board scene for every minor contact; the whole-session episode should have a clear hierarchy.

A deep lesson should normally contain live action, consequence, rewind, question, evidence frame, causal UI, alternative, outcome replay, and drill. A pattern bridge can contain a short clip, one annotation, a claim class, and a link to the main lesson.

## 3. HyperFrames scene types

Supported scene recipes include:

- `live_action`: source clip at natural speed with source audio;
- `consequence`: source clip or still showing the immediate result;
- `rewind`: actual reverse-motion clip with restrained scanline or color treatment;
- `question`: freeze frame plus question and thinking timer;
- `evidence_panel`: observed, inferred, and unknown claims;
- `causal_timeline`: animated `SEES → CHOOSES → EFFECT → CONSEQUENCE` strip;
- `tactical_board`: dark screen with cover, route, sightline, and resource geometry;
- `alternative_compare`: original versus likely better action with trade-off;
- `pattern_bridge`: short linked evidence clip;
- `scorecard`: strengths, priorities, and confidence notes;
- `drill`: measurable next-session practice card.

Keep overlays semantic. Never draw an enemy or telemetry that the source does not support.

## 4. Audio and narration

Use source gameplay audio for action and consequence. Duck it below narration in explanation sections. Keep questions short and leave a thinking window before the reveal. Measure narration duration before setting scene durations. Use local TTS where appropriate and preserve a text source for revision.

## 5. Kinocut finishing

Build an editable finishing timeline listing source clips, narration, ducking, fades, volumes, normalization target, peak safety, and export settings. Normalize near −16 LUFS; if true peak exceeds the project safety target, use a conservative additional trim or limiter pass. Record the measured loudness and peak in the QC report.

## 6. QC

Inspect contact sheets at every major scene type. Confirm the source outcome is visible or explicitly unresolved; questions precede reveals; the agenda is readable; causal UI does not contradict the report; enemy-view panels remain inference-labeled; alternative scenes state trade-offs; drills are measurable; and the video remains pure gameplay coaching without memes or decorative reaction graphics.
