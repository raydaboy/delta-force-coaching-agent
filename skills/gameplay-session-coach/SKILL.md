---
name: gameplay-session-coach
description: Analyze an entire gameplay recording as a coaching session. Use when the user wants a full-video review, a strengths-and-weaknesses assessment, repeated mistakes across fights, a learning agenda, priority corrections, or an opening explanation of what the session will teach.
---

# Gameplay Session Coach

## Purpose

Use this skill after or alongside `gameplay-coach` when the user wants the **whole recording** understood as one performance session. Do not narrate every second equally. Build a session-level model of what the player was trying to do, what repeatedly worked, what repeatedly failed, which moments changed the session, and what should be taught first.

Treat the recording as the source of truth. Import fight-level evidence from `gameplay-coach`; do not replace its before/decision/after discipline. Aggregate only claims that are supported by multiple timestamped observations or one exceptionally clear high-leverage event.

## What this skill produces

The core outputs are:

- `session_map.json`: source boundary, fight index, patterns, strengths, weaknesses, priorities, learning objectives, evidence ledger, and uncertainty.
- `learning_objectives.json`: the short agenda that can open an interactive coaching episode.
- `session_coaching_report.md`: a human-readable whole-session review.
- `evidence/`: contact sheets, extracted clips, frame notes, transcript excerpts, and source analyses when available.

Use `interactive-coaching-script` after this skill when the user wants a narrated, question-and-reveal episode. Use `session-coaching-explainer` after the script skill when the user wants a rendered full-video coaching lesson.

## Operating modes

| Mode | Use when | Required result |
|---|---|---|
| `session_review` | The user wants an inventory of the whole recording | Session map, fight index, evidence gaps |
| `session_coach` | The user wants strengths, weaknesses, and a training plan | Full report, ranked priorities, measurable drills |
| `session_agenda` | The user wants to know what the episode should teach | Learning objectives with evidence and confidence |
| `session_all` | The user wants the complete foundation for an interactive episode | All outputs and validated handoff files |

## Required workflow

### 1. Establish the session boundary

Inspect the source with `gameplay-coach/scripts/inspect_source.py` or `ffprobe`. Record duration, frame rate, resolution, audio availability, game, map or mode if visible, and the player’s stated goal. Note limitations before conclusions: missing audio, cropped HUD, soft frames, off-screen enemies, hard cuts, or unresolved outcomes.

### 2. Build an event inventory

Divide the recording into meaningful segments such as movement, looting, rotation, preparation, contact, fight, recovery, extraction, death, or menu time. Candidate events may come from motion, gunfire, reloads, damage indicators, healing, kill feed, HUD changes, audio peaks, commentary, and scene changes. Candidates are proposals until visually inspected.

Do not let dead air dominate the review. Preserve enough lead-in and aftermath to explain decisions, but prioritize moments that reveal a skill pattern or a turning point.

### 3. Reuse complete fight analyses

For each candidate fight, call or reproduce the `gameplay-coach` contract:

`setup → first contact → initial trade → escalation → turning point → outcome → aftermath`

Every fight must be marked `won`, `lost`, `escaped`, `injured_retreat`, `unresolved`, or another evidence-supported status. Do not treat every death as a mistake and do not treat every kill as proof of correct play.

### 4. Build the session pattern matrix

Compare fights using the same dimensions:

| Dimension | Ask |
|---|---|
| Information | What did the player know before the decision? |
| Advantage | How was an advantage created or lost? |
| Position | Was cover, angle, height, or movement useful? |
| Resources | Was utility, ammo, armor, health, or time used well? |
| Timing | Did the player convert, disengage, or re-peek at the right time? |
| Execution | Did mechanics express a sound decision or rescue a poor one? |
| Outcome | What actually happened and what remained unknown? |

A pattern requires recurrence, a high-leverage exemplar, or a clearly supported session-level principle. Label confidence and list the supporting fight IDs.

### 5. Identify strengths before weaknesses

Strengths should describe repeatable controllable behaviors, not compliments. Examples include first-contact target selection, recoil control after a down, disciplined reload timing, use of hard cover, threat confirmation, or converting an isolated enemy into a safe reset.

A win can still contain a correctable mistake. A loss can still contain a correct decision. Keep those distinctions explicit.

### 6. Rank weaknesses and priorities

Rank candidate corrections by:

`impact × frequency × controllability × transferability × evidence_confidence`

Use no more than three top priorities for the episode. Every priority must include a behavior, at least one supporting fight, the observed consequence, a realistic alternative, uncertainty, and a measurable drill.

### 7. Write the learning agenda

The opening agenda must be supported by the entire session. It should answer:

> “After reviewing this gameplay, what are you already doing well, what is holding you back, and what will we cover today?”

Use this order:

1. Session result and scope.
2. Two or three repeatable strengths.
3. Two or three priority weaknesses.
4. Today’s learning objectives in ranked order.
5. A brief promise of how each objective will be demonstrated.

Avoid vague claims such as “your positioning needs work.” Prefer “you created first advantages in three fights, but twice re-engaged while injured before resetting behind hard cover.”

### 8. Preserve evidence classes

Every session claim is `observed`, `inference`, or `unknown`. A transcript proves what the player said, not what the player saw. A kill feed proves a recorded event, not the player’s intention. A repeated pattern can be inferred only from the listed examples.

Use cautious wording for counterfactuals: “would likely reduce exposure,” “would preserve more options,” or “may have prevented the damage.” Never promise survival or a win without a controlled replay.

### 9. Validate and hand off

Validate with:

```bash
python scripts/validate_session_map.py session_map.json
python scripts/build_session_summary.py session_map.json session_summary.json
```

Then pass `session_map.json`, `learning_objectives.json`, and `session_coaching_report.md` to `interactive-coaching-script`.

## Quality gates

Before delivery, confirm that the session boundary is explicit; fights have complete or unresolved outcomes; strengths and weaknesses cite fights; priorities are limited and measurable; the opening agenda is evidence-backed; repeated patterns do not overstate sample size; and unknowns remain visible.

## Bundled resources

Read `references/session_analysis_workflow.md` for the full event-to-pattern workflow. Read `references/session_map_schema.md` before authoring JSON. Copy `templates/session_map_template.json` for a new session. Use `templates/session_report_template.md` for the report structure. Run the scripts only after timestamps and evidence references are present.
