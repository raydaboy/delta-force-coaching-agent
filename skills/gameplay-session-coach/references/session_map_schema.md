# Session Map Schema

## Top-level fields

```json
{
  "source": {"path": "", "duration": 0, "fps": 0, "resolution": "", "game": "", "mode": "", "limitations": []},
  "session_goal": "",
  "events": [],
  "fights": [],
  "strengths": [],
  "weaknesses": [],
  "priorities": [],
  "learning_objectives": [],
  "session_summary": "",
  "evidence_ledger": [],
  "unknowns": []
}
```

## Event

An event has `event_id`, `start`, `end`, `type`, `summary`, `confidence`, and `evidence`. Use types such as `movement`, `loot`, `rotation`, `contact`, `fight`, `recovery`, `extraction`, `death`, and `unknown`.

## Fight reference

Each fight has `fight_id`, `start`, `end`, `status`, `outcome`, `loadout`, `strengths`, `mistakes`, `key_decisions`, `evidence`, `confidence`, and `unknowns`. `status` must be evidence-supported; use `unresolved` when the source does not establish the result.

## Pattern

A strength or weakness has:

```json
{
  "pattern_id": "pattern_01",
  "label": "advantage_conversion",
  "claim": "",
  "class": "observed|inference|unknown",
  "confidence": 0.0,
  "supporting_fights": ["fight_01"],
  "supporting_evidence": ["frame@94.0"],
  "observed_consequences": [],
  "unknowns": []
}
```

## Priority

```json
{
  "priority_id": "priority_01",
  "rank": 1,
  "title": "",
  "behavior_to_change": "",
  "why_it_matters": "",
  "supporting_fights": ["fight_01"],
  "observed_consequence": "",
  "alternative": "",
  "counterfactual": {"claim": "", "class": "inference", "confidence": 0.0, "unknowns": []},
  "drill": {"name": "", "success_condition": ""}
}
```

## Learning objective

Each objective should map directly to a priority or strength:

```json
{
  "objective_id": "objective_01",
  "rank": 1,
  "title": "",
  "opening_line": "",
  "question_for_player": "",
  "reveal": "",
  "supporting_fights": ["fight_01"],
  "visual_plan": ["freeze_frame", "causal_timeline", "alternative"],
  "drill": {"name": "", "success_condition": ""}
}
```

## Evidence

Evidence entries use `type`, `source_time` or `start`/`end`, `claim`, and `confidence`. Allowed evidence types are `frame`, `frames`, `audio`, `transcript`, `hud`, `ocr`, `telemetry`, `metadata`, `inference`, and `replay_test`.
