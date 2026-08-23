# Episode Script Schema

## Top-level structure

```json
{
  "metadata": {"title": "", "source": "", "duration": 0, "audience": "", "tone": ""},
  "opening": {"spoken_text": "", "evidence_refs": []},
  "beats": [],
  "scorecard": {},
  "drills": [],
  "evidence_ledger": [],
  "unknowns": []
}
```

## Beat object

```json
{
  "beat_id": "beat_01",
  "kind": "cold_open|session_promise|strength|agenda|question|reveal|analogy|alternative|pattern_bridge|progress_check|scorecard|drill",
  "source_times": [0.0, 1.0],
  "claim_class": "observed|inference|unknown|production",
  "spoken_text": "",
  "visual_plan": ["live_clip", "freeze_frame", "causal_timeline"],
  "evidence_refs": ["fight_01"],
  "pause_seconds": 0,
  "uncertainty": [],
  "transition": ""
}
```

`production` is allowed only for neutral directions such as “hold the frame for reading.” It must not smuggle in factual game claims.

## Question beat

A question beat requires `question`, `answerable_from_visible_evidence`, and `thinking_window_seconds`. The answer must not depend on hidden enemy positions or telemetry that is not available.

## Reveal beat

A reveal beat requires `observed_claims`, `inference_claims`, and `unknowns`. Separate these fields even when the spoken narration flows as one paragraph.

## Alternative beat

An alternative requires `original_action`, `better_action`, `tradeoff`, `likely_benefit`, `confidence`, and `unknowns`. Set the claim class to `inference`; never use guaranteed-survival language.

## Scorecard

The scorecard includes `strengths`, `priority_corrections`, `confidence_notes`, `unresolved_questions`, and `next_session_focus`. Keep priority corrections to three or fewer.
