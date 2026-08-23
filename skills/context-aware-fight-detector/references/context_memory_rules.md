# Context memory rules

## 1. Evidence is multi-channel

Use candidate evidence as observations, not as labels. The detector should count independent channels such as visible live enemy, weapon fire, hit/damage feedback, attributed kill feed, player death, retreat after damage, and aftermath recovery. UI-only channels such as an inventory page or death crate are not combat evidence.

A practical starting threshold is:

- **Promote to fight:** at least two combat channels, including one interaction signal and one consequence signal.
- **Promote as unresolved:** sustained interaction is visible but no winner or loser is established.
- **Keep as contact/information_limited:** one weak channel, one sighting, or no consequence.
- **Veto:** explicit loot, death-crate, inventory, angle-clear, peek, movement, or recovery with no independent combat channel.

These thresholds are guardrails, not a replacement for visual review. If the candidate description conflicts with the evidence list, abstain.

## 2. State transitions

```text
NEUTRAL
  -> CONTACT       when a live target or possible threat is observed
  -> NEUTRAL       when the event is loot, movement, or an angle check only

CONTACT
  -> FIGHT         when interaction + consequence evidence appears
  -> CONTACT       when another sighting occurs without exchange
  -> NEUTRAL       after a meaningful reset or sustained loss of contact

FIGHT
  -> AFTERMATH     after kill, player death, retreat, escape, or unresolved cutoff
  -> FIGHT         when another exchange continues without a reset

AFTERMATH
  -> FIGHT         only after a new live target and new interaction are confirmed
  -> RECOVERY      during heal, reload, loot, or safe reset

RECOVERY
  -> CONTACT       after a new threat is observed
  -> NEUTRAL       after the tactical episode is over
```

## 3. Memory variables

Store `active_episode_id`, `active_fight_id`, `continuity_key`, `phase`, `last_combat_signal_time`, `last_consequence_time`, `last_reset_time`, `last_live_target_time`, `last_outcome`, and `evidence_channels`. Update them after every candidate, including rejected candidates. A death crate should update aftermath or recovery, not open a new fight.

## 4. Merge and split rules

Merge adjacent contacts when they share a continuity key and the gap is short, there is no heal/inventory/relocation reset, and the second exchange is clearly part of the same tactical problem. Split when there is a meaningful reset, a new location/route, a sustained loss of contact, or a new objective. Two kills in one uninterrupted room fight may be one `fight_cluster`; the output must explain why.

Do not split because the target changes. Do not merge because the building stays the same. Tactical continuity matters more than map-level location.

## 5. False-positive examples

| Candidate description | Resolved label | Reason |
|---|---|---|
| Player aims at a doorway and scans left/right | `angle_clear` or `peek` | No exchange or consequence |
| Player sees an enemy at long range but does not fire | `contact` | Live target is visible; fight not established |
| Player opens a death crate after a prior kill | `death_crate` / aftermath | Inventory state is a consequence, not a new fight |
| Player opens a loot screen with a body visible | `loot` | No current combat evidence |
| Player walks through a red-lit corridor | `movement` | Atmosphere is not combat |
| Player fires several shots at an unseen target, no hit or outcome | `contact` or `information_limited` | Interaction is not confirmed enough |
| Player and enemy exchange fire, player heals after taking damage | `fight`, outcome `injured_retreat` | Interaction and consequence are visible |
| Player kills an enemy and immediately fights a second enemy from the same room | `fight_cluster` or one continuous fight | No meaningful reset; preserve continuity |
| Player dies after a visible exchange | `fight`, outcome `lost` | Player death is a clear consequence |

## 6. Audit language

Use statements such as: “The frame confirms a peek, not a fight.” “The death crate belongs to the previous fight’s aftermath.” “The exchange is visible, but the winner is not established, so this remains unresolved.” “This is a candidate contact because a live target is visible; we do not promote it without interaction and consequence.”

Never say “the player panicked,” “the player did not hear,” or “the enemy was definitely there” unless the recording proves it. Keep hidden position, intent, and counterfactual survival in `unknowns`.
