---
name: teaching-engine
description: Build source-specific, progressive gameplay coaching lessons from validated fight evidence. Use when an agent must explain why a player’s choice helped or hurt, adapt teaching to proficiency, avoid generic repetition, compare realistic alternatives, and produce measurable next-game drills.
---

# Teaching Engine

## Purpose

Turn verified fight evidence and the player profile into teaching that changes what the player does next game. Do not write commentary that merely describes the clip. Every lesson must answer: **what was the player trying to do, what information was available, what choice was made, what changed immediately, what preserved or threatened the player’s goal, and what repeatable action should happen next time?**

## Required inputs

Read the validated `session_map.json`, `contextual_coaching_map.json`, `goal_record.json`, `player_profile.json` when available, and the raw/resolved event evidence. Do not use a raw model candidate as proof. A lesson must reference a complete engagement with setup, real combat, decision point, outcome, and short consequence.

## Teaching contract

For each featured engagement, produce these fields:

```json
{
  "lesson_id": "fight_16_lesson",
  "lesson_type": "decision|mechanic|position|resource|goal_tradeoff|progression",
  "novelty_label": "new_lesson|progression|repeated_mistake|different_version|model_success|no_review",
  "player_goal_test": "Protect the extraction route while solving the forced close threat.",
  "observed": ["Only claims directly visible or audible in the source."],
  "inferred": ["Cautious interpretation with likelihood language."],
  "unknown": ["Enemy intent, hidden teammates, and unshown geometry."],
  "decision_point": "The smallest controllable choice that changed the exchange.",
  "what_helped": "A specific action that was correct, even inside a loss.",
  "what_hurt": "A specific action or timing that increased risk.",
  "realistic_alternative": {
    "action": "A concrete alternative using visible cover, range, timing, or target order.",
    "tradeoff": "What the player gives up by choosing it.",
    "likely_benefit": "Use likely/could language; never promise a different result.",
    "unknowns": ["What remains unproven."]
  },
  "next_game_cue": "One short instruction the player can remember under pressure.",
  "drill": {
    "name": "Short drill name",
    "trigger": "When the drill applies.",
    "action": "What to do.",
    "success_condition": "Observable/measurable completion condition.",
    "scope": "Next match, next three fights, or practice range."
  }
}
```

## Build the lesson in order

1. **Name the goal conflict.** Decide whether the fight was forced by a nearby threat to loot/position, optional contact, extraction-route danger, or a non-fight event. Never coach an optional fight as mandatory.
2. **Find the turning point.** Use the earliest controllable action that changed exposure, target order, range, cover, information, health, ammo, utility, or escape options. Do not call the death itself the mistake.
3. **Preserve correct choices.** In a lost fight, identify at least one action that helped. In a won fight, identify at least one risk or habit that could fail against a stronger opponent.
4. **Explain the causal chain.** Write `information → choice → immediate effect → outcome → goal consequence`. Keep facts and interpretations in separate evidence classes.
5. **Give one local alternative.** Name the visible room, doorway, container mouth, rock, stair landing, roof cover, smoke edge, audio cue, or extraction route only when the source supports it. If geometry is not clear, say “nearest visible hard cover” and mark the limitation.
6. **State the trade-off.** Explain what the alternative sacrifices: time, loot access, angle, speed, information, ammo, health, or chance to finish.
7. **End with one cue and one drill.** The cue is short enough to recall in combat. The drill must have a trigger and measurable success condition.

## Avoid generic teaching

Reject a lesson if its alternative could be pasted into another fight unchanged. Replace “use cover” with the local decision: “back to the container mouth,” “fall to the stair landing,” “leave the roof sightline,” “cancel the loot screen,” “change the smoke-side pillar,” or another evidence-supported action. Repeating a principle is allowed only when the context changes; label it `progression` or `different_version` and state what is new.

Do not make every fight a deep lesson. Use `deep` review for a turning point, death, extraction risk, loot interruption, multi-target cluster, or model success. Use `standard` review for a distinct but smaller lesson. Use `micro_bridge` for a short confirmation of a known pattern. Use `no_review` when the event has no unique teaching value.

## Calibrate to the player profile

Use prior games, roles, experience, self-rated proficiency, confidence by skill, preferred language, and desired explanation depth to adjust vocabulary, analogy difficulty, review length, and drill complexity. Do not use the profile to change what the recording proves. When self-rating and observed behavior differ, write a hypothesis and invite correction. Never infer age, identity, health, or ability.

For beginners, use one decision, one visible landmark, and plain verbs. For intermediate players, connect the decision to range, target order, timing, and resource trade-offs. For advanced players, add conditional branches and opponent-response checks, but retain a plain-language first sentence.

## Progression and memory

Maintain a lesson ledger across the session. For each new lesson, compare its trigger, decision, alternative, and drill with earlier lessons. Use these labels:

| Label | Use when |
| --- | --- |
| `new_lesson` | The session introduces a new controllable skill. |
| `progression` | The same principle appears, but execution or context changes. Explain the change. |
| `repeated_mistake` | The same trigger and same controllable error recur. Show both timestamps and one repair. |
| `different_version` | The principle is similar, but the threat, range, or objective materially changes the solution. |
| `model_success` | A later action demonstrates the desired behavior. |
| `no_review` | The clip adds no distinct teaching value. |

A full session should finish with no more than three priorities. Each priority must cite at least two supporting moments when available, state whether the pattern improved, and map to one drill.

## Interactive episode pattern

Show the complete action and visible outcome first. Then ask one simple question answerable from the paused frame. Allow 2–4 seconds of thinking time. Reveal `OBSERVED`, then `INFERRED`, then `UNKNOWN`. Rewind only to the decision. Compare the original choice with one realistic alternative. Resume or reference the consequence. End with the cue and drill. Never imply that the player answered unless an actual interaction was captured.

## Quality gates

Reject the teaching output when any featured lesson lacks a source reference, confuses a contact with a fight, starts before combat or outcome, invents enemy intent, offers a copy-paste generic alternative, repeats a prior lesson without a progression label, or ends without a measurable cue/drill. A local validator may check these invariants, but human-watch review of the rendered MP4 remains required.

Read `references/teaching_patterns.md` for concrete loss, win, loot-conflict, multi-target, extraction, and progression examples. Read `references/profile_calibration.md` when adapting lessons to a player’s background. Read `templates/teaching_lesson.json` before authoring machine-readable lessons.
