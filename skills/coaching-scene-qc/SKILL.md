---
name: coaching-scene-qc
description: Audit and improve gameplay coaching scenes and videos for timing, clarity, HyperFrames teaching value, narration alignment, annotation lifetime, dead-space removal, action-first order, and strict audiovisual QC. Use after composing or rendering any interactive gameplay coaching review.
---

# Coaching Scene QC

## Purpose

Make every coaching scene earn its time and make sense to a real player. Check that the fight plays before the explanation, the review begins immediately after the fight, the voice-over explains the visible decision, and HyperFrames annotations appear only for the sentence that needs them. Use `human-context-coaching-audit` when the scene may be technically valid but semantically generic, mistimed, or missing context. Use this skill before rendering and again after rendering.

Read `references/coaching_scene_qc_guide.md` and copy `templates/coaching_scene_qc_checklist.md` for every revision. Before scene review, run `context-aware-fight-detector` on the candidate inventory; do not create a fight review card from a raw vision-model fight list.

## Pre-render audit

Run the human-context questions before accepting a scene as technically ready. Ask what the player knew, what changed the fight, why the review happens at this point, whether the advice is specific to the visible evidence, and whether the player can use it next game. A passing codec, motion score, or readable card does not override a semantic failure.

1. **Check the event type before the fight order.** Confirm that the scene is a promoted fight supported by combat interaction plus consequence. A loot screen, death crate, inventory page, peek, angle clear, movement segment, body view, or recovery scene is not a fight unless independent combat evidence is present. Then confirm that each meaningful fight has a start, first contact, turning point, outcome, and aftermath. Insert the review after that fight, not after extraction.
2. **Check the teaching contract.** Confirm that every fight review says what happened, what worked, what hurt us, and what to do next time when evidence supports those claims.
3. **Check the interactive sequence.** Use normal-speed action, visible consequence, short pause, simple question, 2–4 second thinking window, rewind, explanation, likely alternative, trade-off, and next-game cue.
4. **Check the voice-over map.** Record visual start/end and narration start/end for every scene. Add speech for setup, contact, turning point, outcome, lesson, and next step. Do not add narration merely to fill time.
5. **Check annotation lifetime.** Bring in one arrow, highlight, freeze label, or board shortly before its sentence. Remove it within 0.3–0.5 seconds after that sentence. Split long explanations into several short scenes.
6. **Check language.** Run `plain-language-game-coach` over narration, questions, annotations, and drills. Replace complex terms with concrete game actions.
7. **Check dead space.** Trim silent gaps, stale cards, repeated text, unexplained highlights, and looting or travel that does not teach anything. Preserve natural gameplay breathing only when it has a clear purpose.

## HyperFrames design rules

Use HyperFrames as an active teaching tool rather than a background card. Prefer a freeze frame of the exact decision, a short rewind of the turning point, a single highlighted corner or cover point, an arrow for the proposed route, a `YOU SEE → YOU DO → RESULT` strip, and a before/after comparison. Keep one major visual idea on screen at a time.

Use a fight progress strip that names the current fight and lesson. Keep it small and meaningful. Do not use it as decorative motion. Label inferred enemy-view panels exactly: `ENEMY VIEW — INFERRED FROM VISIBLE GEOMETRY`. Do not draw hidden enemies or unsupported telemetry.

## Voice-over timing rules

Use 8–15 seconds for a routine fight review, 20–35 seconds for a teachable decision, and 45–75 seconds for a major turning point. Let action audio play before the explanation and leave a short breath after the outcome. Duck gameplay audio under narration, but do not erase the sound that proves the decision. End the visual card when its narration ends; never leave a highlight or board hanging while the narrator is silent.

## Post-render inspection

Inspect a contact sheet at the cold open, every fight outcome, every fight card, at least one question and rewind per match, every tactical board, the pattern bridge, the scorecard, and the drills. Listen or inspect waveform timing at the start and end of each narration block. Verify that the first visible frame is not black, that cards do not overlap, and that source footage resumes after each review.

Run strict machine checks on the final output. Require video integrity, accepted brightness, accepted contrast, accepted saturation, balanced color, intelligible loudness, true peak below the delivery target, and adequate motion. If a full-length scan is expensive, use representative samples during iteration but run the authoritative check on the complete final before delivery.

## Acceptance standard

Do not pass a revision if any non-fight event is promoted from a raw candidate list, if any meaningful fight is reviewed only at extraction, if a question appears after its answer, if an annotation is longer than its teaching sentence, if dead space exists solely because of fixed scene duration, if jargon prevents a general player from understanding the advice, if voice-over omits the turning point or consequence, if the insight could be pasted onto any unrelated clip, if the edit removes context needed to understand the choice, or if any claim lacks an evidence class. Technical QC and human-context QC must both pass.

## Handoff

Return a QC report with each failed item, timestamp or scene ID, cause, correction, and recheck result. Separate semantic failures from technical failures. Pass the corrected script to `session-coaching-explainer` for HyperFrames/Kinocut production. Use `context-aware-fight-detector` for candidate promotion and tactical memory, `human-context-coaching-audit` for context and causality, `fight-by-fight-review` for coverage, and `plain-language-game-coach` for wording before the final render.
