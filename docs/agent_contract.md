# Agent Contract

This contract is the operational specification for an LLM agent using the repository.

## Run modes

| Mode | Produces | Use case |
| --- | --- | --- |
| `analyze` | Source manifest, goal record, raw inventory, resolved map, session map | Inspect a new recording without rendering |
| `select` | Contextual coaching map and omission ledger | Decide what belongs in a focused edit |
| `script` | Episode script, narration source, evidence ledger | Write the coaching lesson |
| `render` | Clips, stills, composition, final MP4 | Build the video |
| `qc` | Four human-watch reports and technical report | Decide whether to release |
| `all` | Every artifact and final deliverable | Full autonomous run |

## Required handoffs

The agent must pass artifacts forward, not memory-only summaries. A stage may refuse to run when its required artifact is absent or invalid.

```yaml
analyze:
  requires: [source, goal_record]
  writes: [source_manifest, raw_candidate_inventory, resolved_event_map, session_map]
select:
  requires: [goal_record, resolved_event_map, session_map]
  writes: [contextual_coaching_map, trim_omission_ledger]
script:
  requires: [goal_record, contextual_coaching_map, session_map]
  writes: [episode_script, narration, script_evidence_ledger]
render:
  requires: [source, episode_script, contextual_coaching_map, narration]
  writes: [scene_manifest, composition, final_mp4]
qc:
  requires: [final_mp4, scene_manifest, contextual_coaching_map]
  writes: [technical_qc, temporal_qc, coaching_qc, memory_qc, audio_qc, final_qc_report]
```

## Decision logic

Use the following order for every candidate:

1. Normalize the candidate type and evidence names.
2. Apply hard vetoes for loot, death crates, inventory, menus, movement, recovery, peeks, angle clears, body-only views, generic audio peaks, and extraction countdowns.
3. Check for a live target or confirmed threat.
4. Check for a combat interaction: shots exchanged, weapon fire at a live enemy, a live-enemy hit, or a sustained exchange.
5. Check for a consequence: damage, attributed elimination, player death, retreat after damage, healing caused by the exchange, or clear loss of contact after exchange.
6. Maintain continuity and reset state. Merge only when the player is solving the same tactical problem without a meaningful reset.
7. Assign outcome and confidence. If the winner is unclear, use `unresolved`.
8. Attach `observed`, `inferred`, and `unknown` claims separately.

## Scene selection logic

Select a fight when it is high leverage for the user goal, a strong example of a repeatable behavior, a meaningful progression point, or necessary to explain a later consequence. Prefer complete clusters over isolated kills. Use a pattern bridge or omit the scene when it adds no distinct lesson. Preserve at least one success example, one loss, one escape, one loot-interruption event, and the final extraction-route consequence when they exist.

For every selected fight, compute:

```yaml
setup_start: before first contact, but not a long travel block
combat_start: first confirmed combat interaction
decision_time: the first controllable commitment or reset decision
outcome_time: kill, death, escape, retreat, or other visible result
aftermath_end: short useful consequence only
review_start: outcome_time + 0.3 seconds or later
goal_relation: forced threat, optional risk, extraction risk, loot interruption, or progression
lesson_category: specific skill dimension
novelty: new lesson, progression, repeated mistake, different version, or micro bridge
review_depth: micro, standard, or deep
```

## Script logic

The script must open with the user’s goal and a short agenda supported by the session evidence. For each featured fight, use action, consequence, question, thinking pause, rewind/freeze, observed facts, inference, unknowns, realistic alternative, trade-off, and next-game cue. Do not imply that the player answered a question unless an actual interactive answer exists.

Use plain game language. Prefer “move behind the wall before healing” over “create a defensive reset” and “stop sorting the bag when shots start” over “suspend inventory optimization under threat.”

## QC logic

Run four independent viewer roles on the final MP4:

| Role | Must catch |
| --- | --- |
| Temporal-context viewer | Review before combat, review before outcome, non-fight reviews, missing setup, missing consequence |
| Coaching-usefulness viewer | Generic advice, unsupported claims, unclear alternatives, absent goal connection, jargon |
| Session-memory viewer | Duplicate lessons, missing progression, repeated wording, over-weighting easy AI kills |
| Audio/pacing viewer | Stale overlays, silent gaps, duplicated words, clipped speech, buried game audio, weak start/end |

Every role records timestamps, evidence, severity, and a proposed correction. Block release on any blocker or major. Minor issues must still be logged and fixed when practical.

## Release checklist

The agent may say “final” only when:

- source rights are recorded;
- the raw and resolved maps are present;
- no vetoed event became a fight;
- every featured fight reaches its visible outcome;
- every review starts after that outcome;
- the final video is materially shorter than the source when filler was requested;
- the goal record is included;
- all four human-watch reports and the technical report are present;
- actual audio measurements are recorded;
- the backend used is named truthfully;
- no secrets or private credentials are included.
