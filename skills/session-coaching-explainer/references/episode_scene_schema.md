# Full-Session Episode Scene Schema

## Scene object

```json
{
  "scene_id": "scene_07",
  "kind": "live_action|consequence|rewind|question|evidence_panel|causal_timeline|tactical_board|alternative_compare|pattern_bridge|scorecard|drill",
  "start": 0.0,
  "duration": 0.0,
  "source_times": [0.0, 1.0],
  "asset_refs": [],
  "spoken_text": "",
  "claim_class": "observed|inference|unknown|production",
  "evidence_refs": [],
  "audio": {"gameplay": 1.0, "narration": 0.0, "duck_db": 0},
  "annotations": [],
  "unknowns": []
}
```

## Annotation object

```json
{
  "kind": "label|arrow|route|cover_zone|sightline|timeline_marker|evidence_chip",
  "text": "",
  "class": "observed|inference|unknown|production",
  "position": {"x": 0, "y": 0},
  "evidence_ref": ""
}
```

## Scene requirements

`live_action` and `consequence` need source times. `question` needs a question and thinking duration. `evidence_panel` needs observed, inferred, and unknown text. `alternative_compare` needs original action, alternative, trade-off, and uncertainty. `tactical_board` must declare that it is a simplified geometry model. `drill` must include a measurable success condition.
