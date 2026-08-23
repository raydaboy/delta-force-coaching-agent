# AGENTS.md — Gameplay Coaching Agent Contract

## Mission

Build a useful coaching session from a user-authorized gameplay recording. Optimize for the user’s stated goal, not for raw combat count, model excitement, or video length. The default pure-gameplay mode removes filler and keeps complete meaningful engagements with enough setup and consequence to understand the decision.

## Mandatory startup

Read this file first. If no player profile exists, offer the optional profile questionnaire before the match-goal questionnaire. Then read the skill file matching the requested operation. For a full coaching video, read these in order: `skills/context-aware-fight-detector/SKILL.md`, `skills/gameplay-session-coach/SKILL.md`, `skills/interactive-coaching-script/SKILL.md`, `skills/session-coaching-explainer/SKILL.md`, `skills/coaching-scene-qc/SKILL.md`, and `skills/pure-gaming-highlights/SKILL.md`. Inspect the applicable schema before writing each JSON artifact. Never rely on previous chat context as the only specification.

## Pipeline invariants

1. The player profile and match goal are separate data objects. The profile calibrates teaching; the goal judges decisions.
2. The player goal is data. Capture it before analysis and keep it unchanged in `goal_record.json`.
3. A raw candidate is not a fight. Preserve every candidate, including negative candidates, then run the deterministic resolver.
4. A promoted fight needs both an interaction and a consequence. A sighting, ADS frame, body, death crate, loot page, doorway peek, angle clear, heal, explosion, or generic audio peak is not enough by itself.
5. Maintain tactical memory. Merge uninterrupted exchanges into one cluster; split only after a meaningful reset, substantial relocation, objective change, or sustained loss of contact.
6. Every selected fight must show setup, real first combat, turning point, visible outcome, and short useful aftermath. A review begins only after the outcome.
7. Every spoken claim is labelled `observed`, `inferred`, or `unknown`. Do not invent enemy locations, intent, teammate presence, loot value, or guaranteed counterfactual results.
8. Questions appear before reveals. Use a 2–4 second thinking window when the player could answer from the paused frame.
9. Keep coaching specific. Each lesson must identify what happened, what helped, what hurt, a realistic alternative, the trade-off, and one next-game cue. Do not repeat “use cover” without naming the visible cover or explaining the changed situation.
10. Do not use memes, stickers, reaction graphics, decorative overlays, downloaded footage, or copyrighted inserts in pure-gameplay mode.
11. A technical pass does not replace a human-watch pass. Run temporal context, coaching usefulness, session-memory/repetition, and final audio/pacing reviews on the rendered MP4 itself.

## Player-profile policy

Use prior games, roles, experience, self-rated proficiency, and learning preferences to calibrate vocabulary, analogy difficulty, review depth, and drills. Do not use them to override what the current video proves. If the self-rating and observed behavior differ, label the difference as a hypothesis and invite correction. Do not infer age, identity, health, or ability from the profile.

## Goal policy

If the user says the goal is extraction with valuable loot, rank choices in this order: preserve the loot route; solve an enemy that is already a nearby threat; then improve mechanics. Do not label every enemy sighting as mandatory combat. When a forced fight becomes unfavorable, use a conservative default: take the first safe exchange, then disengage when serious damage, bad position, or loss of a safe win path threatens extraction. If the user gives a different policy, persist that policy and use it instead.

## Output contract

A complete run must produce at least the following files:

| Artifact | Required contents |
| --- | --- |
| `player_profile.json` | Prior games, roles, experience, self-rated proficiency, teaching preferences, and privacy choices |
| `source_manifest.json` | Path, duration, dimensions, frame rate, streams, rights note, limitations |
| `goal_record.json` | Questionnaire result and explicit engagement policy |
| `raw_candidate_inventory.json` | Every broad candidate with source times and evidence |
| `resolved_event_map.json` | All resolved events plus promoted fights and rejection reasons |
| `session_map.json` | Patterns, strengths, weaknesses, evidence ledger, priorities, unknowns |
| `contextual_coaching_map.json` | Selected fights, boundaries, goal relation, risk, novelty, review depth |
| `trim_omission_ledger.json` | Kept fights, omitted fights, omitted ranges, reasons |
| `episode_script.json` | Question/reveal/alternative/drill beats and evidence references |
| `scene_manifest.json` | Render order, clip paths, visual lifetimes, audio timing |
| `final_qc_report.json` | Human-watch findings, technical measurements, severity, corrections, recheck |
| Final MP4 | H.264/AAC, measured loudness, true peak below target, no stale overlays |

## Failure handling

If a fight boundary is uncertain, keep it as `contact`, `information_limited`, or `unresolved` rather than promoting it. If the source is too compressed to prove a claim, state the limitation. If a render backend is unavailable, use the documented fallback and report the actual backend. If any human-watch pass reports a blocker or major, stop delivery, correct the map/script/composition, rerender, and rerun the affected passes.

## Deployment behavior

A deployment must be reproducible from a clean checkout. Profile persistence must be opt-in, external sharing must be explicit, and delete-after-run must be honored. It must accept a source path or mounted upload, create an isolated work directory, write artifacts to a declared output directory, and leave the source untouched. It must not require credentials for local-only operation. Optional services such as speech synthesis, LLM analysis, storage, or queues must be feature-detected and have explicit fallbacks. Never commit secrets or user recordings.
