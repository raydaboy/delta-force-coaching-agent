# Whole-Session Analysis Workflow

## Contents

1. Session boundary and limitations
2. Event inventory
3. Fight clustering
4. Pattern aggregation
5. Priority scoring
6. Learning-objective selection
7. Abstention rules

## 1. Session boundary and limitations

Record the exact source path, duration, frame rate, resolution, audio availability, game, mode, map, and analysis goal. Record limitations before interpreting behavior. A cropped HUD may prevent health or armor claims. A silent recording cannot support missed-audio conclusions. A cut-away cannot support a final outcome.

## 2. Event inventory

Use a coarse pass to mark movement, looting, rotations, contacts, fights, healing, extraction, death, and downtime. Use a fine pass only on high-leverage events. Every candidate event should have a start, end, type, confidence, and reason for inspection.

A fight window should include enough lead-in to establish health, armor, weapon, resources, cover, visible threats, and objective. Extend after the apparent kill, retreat, or escape until the immediate consequence is clear.

## 3. Fight clustering

Group related contacts into one fight when the player remains in the same tactical problem or the aftermath of one exchange directly causes the next action. Split fights when the player has a meaningful reset, relocation, heal, objective change, or loss of contact.

Use the fight-level statuses `won`, `lost`, `escaped`, `injured_retreat`, and `unresolved`. Do not convert an unresolved cut into a win or loss.

## 4. Pattern aggregation

A session pattern should cite the fight IDs and timestamps that support it. Distinguish:

- **Repeated behavior:** appears in at least two comparable events.
- **High-leverage exception:** one event is enough because the causal evidence is unusually clear.
- **Possible pattern:** plausible but under-sampled; do not make it a top priority without a confidence downgrade.

Compare both successes and failures. A pattern can be “creates first advantage but does not reset” even when some fights are won.

## 5. Priority scoring

Use a qualitative or normalized score for:

- impact on survival, conversion, or objective success;
- frequency across comparable events;
- controllability by the player;
- transferability to future fights;
- evidence confidence.

Do not display a fake precise score if the underlying evidence is qualitative. Rank priorities as high, medium, or low and explain the reason.

## 6. Learning-objective selection

Select no more than three objectives for one episode. Prefer objectives that explain multiple events, are actionable, and can be drilled. Start with strengths to establish what should be preserved, then introduce the highest-impact correction, then show how the correction changes a real decision.

Each objective needs:

- a short title;
- the player behavior to preserve or change;
- supporting fight IDs;
- observed consequence;
- likely alternative benefit;
- trade-off or unknowns;
- a measurable drill.

## 7. Abstention rules

Write `information_limited` when a claim depends on audio, telemetry, enemy position, or intent that the recording does not establish. Do not infer “panic,” “greed,” “tunnel vision,” or “did not hear” from behavior alone. Describe what is visible first, then offer a tactical interpretation with a confidence label.
