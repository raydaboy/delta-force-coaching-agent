# Goal-Aware Gameplay Coaching Agent

This repository turns a gameplay recording into a focused coaching edit. It is designed for an autonomous or semi-autonomous LLM agent that must understand the player’s goal, separate real fights from lookalikes, explain complete engagements, preserve causal context, and produce a validated video deliverable.

The repository is intentionally **goal-aware, evidence-first, and pure gameplay**. It does not assume that every enemy sighting is a fight, every kill is a good decision, or every death proves a mistake. The player’s stated objective is persisted as data and used to judge whether an engagement was forced, optional, extraction-relevant, or a poor risk for the loot objective. A separate player profile records prior games, roles, experience, self-rated proficiency, and teaching preferences so the coach can calibrate its language and drills without using background information to override current-video evidence.

> Core rule: show the action and visible outcome first; ask a simple question; then rewind or freeze the decision; distinguish observed facts from inference and unknowns; and end with one usable next-game cue.

## What the agent builds

The normal pipeline converts one source recording into the following artifact chain:

| Stage | Input | Output | Acceptance condition |
| --- | --- | --- | --- |
| Source inspection | Video file | `source_manifest.json` | Duration, frame rate, dimensions, audio, and limitations recorded |
| Player profile | Profile questionnaire | `player_profile.json` | Prior games, roles, experience, proficiency, learning preferences, and privacy choices persisted |
| Goal capture | Match questionnaire responses | `goal_record.json` | Primary goal, secondary goals, forced-fight definition, and risk policy persisted |
| Candidate scan | Source plus coarse analysis | `raw_candidate_inventory.json` | Broad events retained, including negative evidence |
| Context resolution | Candidate inventory | `resolved_event_map.json` | Only interaction-plus-consequence events become fights; vetoed events stay auditable |
| Session coaching | Resolved fights plus goal record | `session_map.json`, learning agenda | Strengths and priorities cite timestamped evidence |
| Edit selection | Session map | `contextual_coaching_map.json`, trim ledger | Complete setup, exchange, outcome, and short consequence retained |
| Script generation | Coaching map | Episode script and narration | Questions precede reveals; language is concrete; claims carry evidence classes |
| Composition | Clips, stills, narration | HyperFrames project and scene manifest | Source action plays before review; annotations have bounded lifetime |
| Finishing | Composition plus source audio | Final H.264/AAC MP4 | Audio is measured, true-peak safe, and human-watch QC passes |

## Repository layout

```text
skills/                         Agent operating instructions
  context-aware-fight-detector/ Conservative event resolver and veto rules
  gameplay-session-coach/       Whole-session pattern and agenda workflow
  interactive-coaching-script/  Question-first script contract
  session-coaching-explainer/   Action-first coaching video recipe
  coaching-scene-qc/            Semantic scene and post-render QC rules
  pure-gaming-highlights/       Focused edit and pure-gameplay rules
scripts/                        Deterministic command-line pipeline
schemas/                        JSON contracts and validation schemas
templates/                      Starter artifacts, goal questionnaire, and player-profile questionnaire
configs/                        Defaults for local and deployed runs
examples/                       Small, inspectable artifacts from a real session
tests/                          Regression fixtures and pipeline tests
docs/                           Architecture, agent contract, and deployment notes
deploy/                         Container and service entry points
```

## Minimal run

The intended clean-run sequence is:

```bash
python3 scripts/inspect_source.py --input /path/to/gameplay.mp4 --output work/source_manifest.json
python3 scripts/capture_goal.py --input templates/goal_questionnaire.json --output work/goal_record.json
python3 scripts/build_candidate_inventory.py --source work/source_manifest.json --goal work/goal_record.json --output work/raw_candidate_inventory.json
python3 scripts/resolve_candidates.py work/raw_candidate_inventory.json --output work/resolved_event_map.json
python3 scripts/build_session_map.py --events work/resolved_event_map.json --goal work/goal_record.json --output work/session_map.json
python3 scripts/build_coaching_map.py --session work/session_map.json --output work/contextual_coaching_map.json
python3 scripts/validate_pipeline.py --workdir work
python3 scripts/render_episode.py --workdir work --output dist/gameplay_coaching.mp4
python3 scripts/run_human_watch_qc.py --video dist/gameplay_coaching.mp4 --map work/contextual_coaching_map.json --output qc
```

The player profile is optional but recommended for personalized coaching. It changes vocabulary, analogy difficulty, review depth, and drill complexity; it must not change what the source proves. The current sandbox build uses FFmpeg and HyperFrames equivalents where Kinocut is unavailable. The agent must report which finishing backend was actually used; it must never claim Kinocut finishing when only FFmpeg was available.

## Agent operating contract

Before acting, read `AGENTS.md`, the relevant skill files, and the input artifact schemas. Keep raw candidates separate from resolved fights. Never delete negative evidence. Never use a raw vision-model fight list as a final edit map.

During analysis, maintain these evidence classes:

| Class | Meaning | Allowed language |
| --- | --- | --- |
| `observed` | Directly visible or audible in the source | “The frame shows…” |
| `inferred` | A cautious conclusion from visible geometry or repeated evidence | “This likely reduced exposure…” |
| `unknown` | Not established by the recording | “Enemy intent is unknown…” |

During editing, every featured engagement must have a `setup_start`, `combat_start`, `outcome_time`, and `aftermath_end`. `review_start` must be at or after `outcome_time + 0.3` seconds. The edit may use a micro-review, standard review, deep review, pattern bridge, or no-review outcome, but it must not create a review card for loot, death-crate browsing, inventory, peeking, angle clearing, movement, recovery, menus, or extraction countdowns by themselves.

## Safety and rights

Only process recordings supplied by the user or otherwise authorized for review. Do not bypass DRM, authentication, paywalls, or platform restrictions. Do not publish automatically without explicit confirmation. Keep secrets in environment variables or a deployment secret store; never commit account credentials, API keys, or private source URLs.

## Current example

`examples/delta_force_session/` contains the goal record, raw candidate inventory, deterministic resolver output, focused coaching map, source audit, and omission ledger created from a Delta Force Mobile recording. The raw video is intentionally not committed. Its source path is an example-only reference and must be replaced in a clean deployment.

## Deployment summary

For local work, use the scripts directly and keep large source and render files under an ignored `work/` or mounted media volume. For a persistent deployment, run the worker in a container with FFmpeg, Python, optional ONNX speech dependencies, and a writable artifact volume. A web API or queue should call the same deterministic scripts rather than duplicate their logic. See `docs/architecture.md`, `docs/agent_contract.md`, and `docs/deployment.md`.
