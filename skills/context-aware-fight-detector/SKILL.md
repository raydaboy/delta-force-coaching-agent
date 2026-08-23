---
name: context-aware-fight-detector
description: Resolve broad gameplay event candidates into evidence-backed fights while preserving tactical context and memory. Use when a gameplay analyzer overcounts looting, death crates, peeks, angle clears, movement, or visual peaks as fights, or when a full-session coaching edit needs reliable fight boundaries and outcomes.
---

# Context-Aware Fight Detector

## Purpose

Separate **candidate events** from **real fights**. Maintain a small state machine for the active tactical episode so a loot screen, death crate, doorway peek, or angle clear cannot become a fight without sustained combat evidence and a consequence.

Use this skill before `gameplay-session-coach`, `interactive-coaching-script`, or any fight-by-fight coaching edit. The detector should prefer an honest `contact`, `information_limited`, or `non_fight` label over an invented fight.

## Required input

Use a coarse event inventory from video analysis or manual annotation. Each candidate should have:

```json
{
  "event_id": "event_014",
  "start": 120.0,
  "end": 124.0,
  "type_guess": "peek|angle_clear|loot|death_crate|contact|combat|recovery|movement|unknown",
  "summary": "short visible description",
  "location_id": "optional continuity key",
  "evidence": [
    {"kind": "shots_exchanged|damage_feedback|live_enemy|kill_feed_attributed|player_death|retreat_after_damage|inventory_screen|loot_screen|angle_clear|movement", "strength": 0.0, "claim": "what is visible"}
  ]
}
```

Do not accept a prose list of “fights” as ground truth. Convert it into candidates and resolve it with the evidence contract.

## Promotion contract

Promote a candidate to `fight` only when the evidence shows both **combat interaction** and a **combat consequence**. A practical promotion requires one of these combinations:

| Combat interaction | Consequence | Result |
|---|---|---|
| Shots exchanged or visible weapon fire at a confirmed live enemy | Damage feedback, kill feed attributed to the player, player death, or retreat after damage | Promote |
| Damage feedback or hit marker with a confirmed live enemy | Kill, retreat, heal, death, or clear loss of contact caused by the exchange | Promote |
| Attributed kill feed or death screen | Prior shot/damage context within the same tactical episode | Promote |
| Sustained exchange across multiple candidate events | Outcome remains unclear | Promote as `unresolved`, not as a win or loss |

A single sighting, aiming frame, ADS frame, visual peak, body, death crate, inventory page, grenade in hand, doorway peek, angle clear, or dangerous-looking corridor is **not** enough. A single unexplained sound is a `contact` or `information_limited` event unless another channel confirms combat.

## Memory state

Maintain state while scanning the timeline:

- `active_episode_id`: the current tactical problem.
- `active_fight_id`: the promoted fight, if any.
- `last_combat_signal_time`: most recent shots, damage, or live-target exchange.
- `last_consequence_time`: most recent damage, kill, death, retreat, or escape.
- `last_reset_time`: heal, inventory/loot, relocation, objective change, or sustained loss of contact.
- `continuity_key`: room, route, or visual location when available.
- `phase`: `neutral`, `contact`, `fight`, `aftermath`, or `recovery`.

Never use a single frame in isolation. Look backward for setup and forward for consequence before creating a fight boundary.

## Clustering and splitting

Merge contacts into one fight when the player remains in the same tactical problem and the next exchange follows without a meaningful reset. Looting, checking the room, reloading, or clearing the next angle immediately after a kill is aftermath unless a new live enemy and new combat exchange are established.

Split into a new fight after a meaningful heal/reset, inventory or death-crate interaction, substantial relocation, objective change, or sustained loss of contact. Use a short gap alone only as supporting evidence; time is not a fight boundary by itself. If the location key is missing, lower confidence rather than pretending two scenes are unrelated.

Use `fight_cluster` only when several enemies are part of one uninterrupted exchange. Do not split every target, kill, or doorway into a separate fight. Conversely, do not merge a later fight simply because it occurs in the same building after a genuine reset.

## Non-fight veto rules

The following labels remain non-fights unless independent combat evidence appears in the same episode:

- `loot` or `death_crate`: inventory/box interaction; attach as aftermath to the previous fight when causally connected.
- `angle_clear` or `peek`: checking a sightline; do not infer an enemy or exchange.
- `movement`, `rotation`, or `dangerous_area`: navigation without combat evidence.
- `body_seen` or `death_screen` without attribution: do not infer that the player won the fight.
- `visual_peak`, `screen_flash`, or generic audio peak: trigger inspection only; never promotion by itself.
- `recovery` or `healing`: may be a consequence of a fight, but is not a fight alone.

## Outcome and confidence

Use only evidence-supported outcomes:

- `won`: player-attributed elimination is visible and tied to the exchange.
- `lost`: player death is visible and tied to the exchange.
- `injured_retreat`: damage is visible and the player disengages or heals without a confirmed kill.
- `escaped`: contact ends and the player safely resets without a confirmed winner.
- `unresolved`: the recording cuts away or lacks enough evidence.

Set confidence from independent evidence channels, not model certainty. `high` means at least three agreeing channels; `medium` means two strong channels; `low` or `information_limited` means a single weak signal. Low-confidence candidates should remain `contact` or `information_limited` unless the consequence is unmistakable.

## Output contract

Write both levels:

1. `events`: every candidate with a resolved label, evidence reasons, state transitions, and rejection reason when it is not a fight.
2. `fights`: only promoted fights with `fight_id`, complete boundaries, setup, first contact, turning point, outcome, aftermath, confidence, supporting event IDs, evidence classes, and unknowns.

Downstream coaching must consume `fights`, not the raw candidate list. A review card must never be generated for an event whose resolved label is `loot`, `death_crate`, `peek`, `angle_clear`, `movement`, `recovery`, or `information_limited`.

## Workflow

1. Build a broad candidate inventory; do not call it a fight list.
2. Normalize event types and evidence names.
3. Scan candidates in time order with the memory state.
4. Apply non-fight vetoes before scoring.
5. Promote only when the interaction-plus-consequence contract is met.
6. Merge or split using tactical continuity and reset evidence.
7. Assign outcome, confidence, unknowns, and evidence reasons.
8. Run the regression fixture and inspect rejected false positives.
9. Pass the resolved `fights` to session analysis and keep rejected events available for audit.

## Resources

Run `scripts/resolve_event_candidates.py` for deterministic resolution. Read `references/context_memory_rules.md` for thresholds, edge cases, and audit language. Copy `templates/context_event_inventory.json` when starting a new inventory. Use the regression fixture as a minimum smoke test before rendering coaching scenes.
