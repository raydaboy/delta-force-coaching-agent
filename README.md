# Goal-Aware Gameplay Coaching Agent

> An evidence-first pipeline for turning gameplay recordings into focused, interactive coaching sessions—without mistaking loot screens, peeks, travel, or enemy sightings for fights.

[![CI](https://github.com/OWNER/REPOSITORY/actions/workflows/validate.yml/badge.svg)](https://github.com/OWNER/REPOSITORY/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Media](https://img.shields.io/badge/media-FFmpeg%20%7C%20HyperFrames-111827)](https://ffmpeg.org/)
[![Mode](https://img.shields.io/badge/mode-pure%20gameplay-16A34A)](#design-principles)

This repository turns an authorized gameplay recording into a **goal-aware coaching edit** for an autonomous or semi-autonomous LLM agent. It preserves causal context, separates verified fights from lookalikes, explains what helped and hurt, adapts teaching to the player’s experience, and produces machine-readable handoff artifacts for rendering and quality control.

The system is designed for extraction shooters and tactical games, but the contracts are deliberately general. A player can say “extract with valuable loot first,” “win only fights that come to me,” or “practice movement and aim.” The agent then uses those priorities to decide which engagements deserve attention and how the lesson should be taught.

## Why this exists

Many gameplay-review systems over-select visible action. They call a death crate a fight, start analysis before combat begins, cut away before the outcome, repeat “use cover” twenty times, or treat every enemy sighting as a mandatory duel. This project takes the opposite approach.

> **Show the action and visible outcome first. Ask a simple question. Rewind to the decision. Separate observed facts from inference and unknowns. End with one cue the player can use next game.**

The result is not a montage of raw combat. It is a structured coaching session that explains the player’s decisions in the context of their goal.

## Core capabilities

| Capability | What it prevents or enables |
| --- | --- |
| Goal capture | Judges decisions against the player’s actual objective instead of raw kill count. |
| Player profile | Calibrates vocabulary, explanation depth, analogies, and drills using prior games, roles, and proficiency. |
| Context-aware fight detection | Requires interaction plus consequence and vetoes loot, menus, peeks, angle clears, travel, healing, and death-crate browsing. |
| Tactical memory | Clusters uninterrupted pressure into one episode and avoids splitting a squad fight into fake separate fights. |
| Teaching engine | Produces a local turning point, what helped, what hurt, realistic alternative, trade-off, novelty label, cue, and measurable drill. |
| Interactive script | Shows complete action and outcome before the question, rewind, evidence reveal, and alternative. |
| Evidence discipline | Labels claims as `observed`, `inferred`, or `unknown`; never invents enemy intent or guaranteed counterfactuals. |
| Session workbook/playbook | Builds a printable tactical playbook and training workbook with selected local snapshots, evidence stacks, drills, reflection prompts, and next-session rules. |
| Human-watch QC contract | Treats temporal context, coaching usefulness, repetition, and audio/pacing as separate release gates. |

## Pipeline at a glance

```text
player profile + match goal
             |
             v
source inspection --> candidate inventory --> context resolver
                                              |
                                              v
                                      session map + agenda
                                              |
                                              v
                                  coaching map + trim ledger
                                              |
                                              v
                               teaching lessons + drill ledger
                                              |
                                              v
                             question-first episode script
                                              |
                                              v
                           source clips + visual scene manifest
                                              |
                                              v
                            HyperFrames / FFmpeg composition
                                              |
                                              v
                         technical QC + four human-watch gates
                                              |
                                              v
                                      final coaching MP4
```

Each handoff is a named JSON artifact. Raw candidates are retained even when rejected. A final fight must have real combat evidence, a visible outcome, complete boundaries, and a reason to teach it.

## Teaching philosophy

The teaching layer is intentionally stricter than a commentator. Every featured lesson must identify the player’s goal conflict, the earliest controllable turning point, at least one correct action, the action or timing that increased risk, and one realistic local alternative. It must explain the trade-off and finish with a short cue plus a drill whose success condition can be observed.

The system tracks memory across the session using `new_lesson`, `progression`, `repeated_mistake`, `different_version`, `model_success`, and `no_review`. A repeated principle is not presented as new insight unless the threat, range, objective, or solution materially changes.

The player profile personalizes teaching but never overrides evidence. A beginner receives one landmark and one action. An intermediate player receives timing, target order, and resource trade-offs. An advanced player can receive conditional branches and opponent-response checks. All levels get a plain-language first sentence.

For a player-facing quick reference after a session, use the mandatory [`Standard Tactical Playbook Format`](docs/tactical_playbook_standard.md). It turns approved lessons into a goal-aware match objective, strengths, primary adjustments, scenario rules, core operating rules, measurable drills, and visible evidence limits. See the sanitized [`Delta Force extraction example`](examples/delta_force_extraction_tactical_playbook.md).

## Repository layout

```text
skills/
  context-aware-fight-detector/   Conservative event resolution and tactical memory
  gameplay-session-coach/         Whole-session patterns and learning agenda
  teaching-engine/                Source-specific lessons, progression, and drills
  interactive-coaching-script/    Question-first episode writing
  session-coaching-explainer/     Action-first pauses, rewinds, and tactical UI
  coaching-scene-qc/              Scene and post-render quality rules
  pure-gaming-highlights/         Focused trim and pure-gameplay rules

scripts/                          Deterministic CLI builders and validators
schemas/                          JSON contracts for goals, profiles, events, and lessons
templates/                        Goal and player-profile questionnaires
templates/workbook_typst_base/     Portable Typst base for private training PDFs
examples/                         Inspectable artifacts from a real Delta Force session
configs/                          Local and deployment defaults
deploy/                           Container worker and Compose configuration
docs/                             Architecture, deployment, profile, and agent contracts
tests/                            Regression tests
```

## Quickstart

Use the scripts directly from a clean checkout. Keep large recordings and renders outside Git, normally under an ignored `work/` directory or a mounted media volume.

```bash
python3 -m pip install -e .

python3 scripts/inspect_source.py \
  --input /path/to/gameplay.mp4 \
  --output work/source_manifest.json

python3 scripts/capture_player_profile.py \
  --template templates/player_profile_questionnaire.json \
  --output work/player_profile.json

python3 scripts/capture_goal.py \
  --input templates/goal_questionnaire.json \
  --output work/goal_record.json

# Supply candidate events from a multimodal analyzer or manual annotator.
python3 scripts/build_candidate_inventory.py \
  --source work/source_manifest.json \
  --goal work/goal_record.json \
  --output work/raw_candidate_inventory.json

python3 scripts/resolve_candidates.py \
  work/raw_candidate_inventory.json \
  --output work/resolved_event_map.json

python3 scripts/build_session_map.py \
  --events work/resolved_event_map.json \
  --goal work/goal_record.json \
  --profile work/player_profile.json \
  --output work/session_map.json

python3 scripts/build_coaching_map.py \
  --session work/session_map.json \
  --output work/contextual_coaching_map.json

python3 scripts/build_teaching_ledger.py \
  --map work/contextual_coaching_map.json \
  --output work/teaching_lessons.json

python3 scripts/validate_teaching.py work/teaching_lessons.json
python3 scripts/validate_pipeline.py --workdir work
```

The generic repository render command creates a scene handoff manifest. Connect a verified HyperFrames/FFmpeg or Kinocut adapter for the actual media export; the agent must record the backend that truly ran.

## Build a session workbook & tactical playbook

The optional PDF subsystem turns an **approved**, source-specific coaching map into a printable hybrid training workbook and tactical playbook. It is designed for the player to read away from the video: selected evidence snapshots, decision explanations, local alternatives, trade-offs, drills, reflection prompts, and a three-rule next-session plan.

The PDF uses a local Typst installation. Keep the source, extracted snapshots, build directory, and PDF outside Git. The repository includes only the renderer, schema, sanitized examples, and portable Typst base.

```bash
# Build a private snapshot manifest from your approved lessons first.
python3 scripts/extract_workbook_snapshots.py \
  --source /private/source.mp4 \
  --manifest /private/run/artifacts/workbook_snapshot_manifest.json \
  --output-dir /private/run/workbook/snapshots

# Reject generic, unsupported, or incomplete lessons before rendering.
python3 scripts/validate_session_workbook.py \
  /private/run/artifacts/session_workbook.json \
  --snapshot-manifest /private/run/workbook/snapshots/workbook_snapshot_manifest.json \
  --require-snapshot-files

# Render the private PDF and build manifest.
python3 scripts/render_session_workbook.py \
  --input /private/run/artifacts/session_workbook.json \
  --snapshot-manifest /private/run/workbook/snapshots/workbook_snapshot_manifest.json \
  --output-dir /private/run/workbook/output
```

See [`docs/session_workbook_playbook.md`](docs/session_workbook_playbook.md) for the complete contract and page design. A PDF build is a document-rendering stage only; it does not replace evidence validation, video QC, or independent human review.

## Validation

Run the complete clean-checkout suite with:

```bash
make test
make smoke
make smoke-teaching
```

The release contract requires more than syntax checks. The rendered MP4 must be reviewed independently for temporal context, coaching usefulness, session-memory/repetition, and final audio/pacing. A technical loudness scan cannot substitute for a human-watch review. Any blocker or major finding stops delivery until the affected artifact is corrected and rechecked.

## Evidence model

| Class | Meaning | Safe language |
| --- | --- | --- |
| `observed` | Directly visible or audible in the recording | “The frame shows…” |
| `inferred` | A cautious conclusion from visible geometry or repeated evidence | “This likely reduced exposure…” |
| `unknown` | Not established by the source | “Enemy intent is unknown…” |

Never claim that an unseen teammate existed, that an enemy intended a specific action, or that a different choice would definitely have won. If the source is too compressed to prove a claim, retain the limitation.

## Deployment

The repository includes a Dockerfile, Compose configuration, environment template, worker entry point, CI workflow, and deployment notes. A deployment accepts a mounted source, creates an isolated work directory, leaves the source untouched, writes declared artifacts, and feature-detects optional model, speech, storage, queue, and rendering services.

See [`docs/architecture.md`](docs/architecture.md), [`docs/agent_contract.md`](docs/agent_contract.md), [`docs/deployment.md`](docs/deployment.md), and [`skills/teaching-engine/SKILL.md`](skills/teaching-engine/SKILL.md) before wiring a production adapter.

## Privacy and rights

Process only recordings that the user owns or is authorized to review. Do not commit recordings, model weights, credentials, private URLs, or generated renders. Profile persistence is opt-in, external sharing is explicit, and delete-after-run behavior must be honored. Pure-gameplay mode excludes memes, stickers, reaction graphics, downloaded footage, and copyrighted inserts.

## Contributing

Contributions should preserve the artifact contracts and add regression coverage for every new detector veto, teaching rule, or renderer behavior. When changing a schema, update its example and validator in the same change. When changing teaching language, demonstrate that the lesson remains source-specific, evidence-labelled, and non-repetitive.

## Project status

The repository is **agent-ready and contract-complete**. The context resolver, goal/profile contracts, teaching engine, validators, examples, deployment scaffolding, and CI checks are included. Backend-specific media rendering and independent human-watch QC remain replaceable adapters by design; a deployment must not claim that an unavailable backend or reviewer ran.
