---
name: interactive-coaching-script
description: Write interactive whole-session gameplay coaching scripts from a validated session map. Use when the video should open with strengths and weaknesses, announce what will be learned, ask the player questions before revealing analysis, and connect multiple fights into one training story.
---

# Interactive Coaching Script

## Purpose

Turn a validated `gameplay-session-coach` session map into a clear, engaging coaching episode script. The episode should feel like a coach guiding a review with the player, not a commentator reading a timeline.

Do not invent findings. Every strength, weakness, question, reveal, alternative, and drill must trace to the session map or its evidence ledger.

## Inputs and outputs

Required inputs:

- `session_map.json` or the summary from `gameplay-session-coach`.
- Fight evidence windows and source timestamps.
- Optional transcript and player commentary.

Outputs:

- `interactive_coaching_script.md`: complete narration and scene directions.
- `episode_script.json`: machine-readable beats, questions, reveals, evidence, and visual plans.
- `narration.txt`: spoken text only, ready for TTS.
- `script_evidence_ledger.json`: claims mapped to timestamps and evidence classes.

## Episode structure

Use this default sequence:

1. **Cold open:** Show a compelling action and consequence without explaining it yet.
2. **Session promise:** State what was analyzed and what the player will learn.
3. **Strengths first:** Name the repeatable behaviors worth preserving.
4. **Today’s agenda:** Announce no more than three learning objectives.
5. **Interactive question:** Pause before a high-leverage decision and ask what the player would do.
6. **Reveal:** Show the observed action, immediate effect, consequence, and causal interpretation.
7. **Analogy or tactical model:** Explain the principle in simple language.
8. **Alternative:** Compare the original choice with a realistic better option and state the trade-off.
9. **Pattern bridge:** Connect the lesson to another fight or later session moment.
10. **Progress check:** Identify whether the same behavior improved, repeated, or remained unresolved.
11. **Final scorecard:** Summarize strengths, priority corrections, confidence, and unknowns.
12. **Drills:** End with measurable next-session exercises.

## Interactive writing rules

Ask questions before revealing answers. Questions should be answerable from the paused frame or short lead-in:

- “Where is your safest reset before you start the heal?”
- “Do you spend the grenade now, or hold it for the predictable route?”
- “What information is confirmed, and what is still only a possibility?”

Give the player a short thinking window in the scene plan. Do not use fake scoring or imply that the player answered unless an actual interaction is captured.

Use direct coaching language:

- “Here is what the frame confirms.”
- “This is the inference I am making from that evidence.”
- “The alternative would likely reduce exposure, but it does not guarantee survival.”
- “The win was earned by these controllable decisions.”

## Explain wins and losses correctly

For a win, explain how the player created and converted an advantage. Do not reduce the lesson to aim or luck. For a loss, explain the turning point and the controllable choice without treating the outcome alone as proof of error. Preserve correct decisions inside lost fights and mistakes inside won fights.

## Evidence contract

Each script beat must include:

```json
{
  "beat_id": "beat_07",
  "kind": "question|narration|reveal|analogy|alternative|pattern_bridge|drill",
  "source_times": [1260.0, 1274.0],
  "claim_class": "observed|inference|unknown",
  "spoken_text": "",
  "visual_plan": ["freeze_frame", "causal_timeline"],
  "evidence_refs": ["fight_03.decision_01"],
  "pause_seconds": 0,
  "uncertainty": []
}
```

A spoken sentence can contain multiple claims. Split them into separate beats when their evidence classes differ. Do not let a visual overlay imply more certainty than the narration.

## Script pacing

Use short sentences for action and questions. Give the viewer enough time to read tactical overlays. A typical episode should use one major lesson every three to six minutes, with shorter pattern bridges between them. If the session is short, compress the structure without removing the agenda, evidence, alternative, or drills.

Do not narrate every frame. Let gameplay audio and natural consequences breathe before the rewind or explanation.

## Validation and handoff

Validate the session map first. Then run:

```bash
python scripts/validate_episode_script.py episode_script.json
python scripts/render_narration.py episode_script.json narration.txt
```

Pass `episode_script.json` and `narration.txt` to `session-coaching-explainer`.

## Bundled resources

Read `references/interactive_episode_workflow.md` for scene-by-scene writing rules. Read `references/script_schema.md` before authoring JSON. Copy `templates/episode_script_template.json` and `templates/interactive_script_template.md` for new episodes. Read `references/question_reveal_patterns.md` for reusable interactive prompts and reveal shapes.
