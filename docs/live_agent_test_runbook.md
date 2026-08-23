# Live-agent test runbook

## What happens after cloning

A fresh agent can discover the workflow by reading `AGENTS.md`, `README.md`, the relevant skill files, and the schemas. The repository’s examples and validators run without access to the original recording. The agent can therefore test artifact creation, fight-resolution rules, lesson contracts, question-first episode structure, edit-map completeness, and deployment handoff immediately.

A clone does **not** automatically know the contents of a new gameplay recording. The user must provide an authorized source file and answer the player-profile and match-goal questionnaires. The agent must then obtain candidate events from a multimodal analyzer, a game-specific analyzer, or a human annotation file. The deterministic resolver is the authority for promotion and rejection after those candidates are supplied.

## Clean-clone smoke test

```bash
git clone https://github.com/raydaboy/delta-force-coaching-agent.git
cd delta-force-coaching-agent
python3 -m pip install -e .
make test
make smoke
make smoke-teaching
```

The smoke test proves that the checkout is syntactically valid and that the included examples satisfy the profile, teaching, episode, scene, and edit contracts.

## Live run with a new recording

Create an isolated run directory and never modify the source file in place.

```bash
mkdir -p work/live_run/{input,artifacts,render,qc}
cp /path/to/authorized/gameplay.mp4 work/live_run/input/source.mp4

python3 scripts/inspect_source.py \
  --input work/live_run/input/source.mp4 \
  --output work/live_run/artifacts/source_manifest.json

python3 scripts/capture_player_profile.py \
  --template templates/player_profile_questionnaire.json \
  --output work/live_run/artifacts/player_profile.json

python3 scripts/capture_goal.py \
  --input templates/goal_questionnaire.json \
  --output work/live_run/artifacts/goal_record.json
```

At this point the agent should call the configured multimodal analyzer or accept a human/manual event file. It must record broad candidates, including rejected lookalikes, in `raw_candidate_inventory.json`. It must not jump directly from a model’s fight list to editing.

```bash
python3 scripts/resolve_candidates.py \
  work/live_run/artifacts/raw_candidate_inventory.json \
  --output work/live_run/artifacts/resolved_event_map.json

python3 scripts/build_session_map.py \
  --events work/live_run/artifacts/resolved_event_map.json \
  --goal work/live_run/artifacts/goal_record.json \
  --profile work/live_run/artifacts/player_profile.json \
  --output work/live_run/artifacts/session_map.json

python3 scripts/build_coaching_map.py \
  --session work/live_run/artifacts/session_map.json \
  --output work/live_run/artifacts/contextual_coaching_map.json

python3 scripts/build_teaching_ledger.py \
  --map work/live_run/artifacts/contextual_coaching_map.json \
  --output work/live_run/artifacts/teaching_lessons.json

python3 scripts/validate_teaching.py \
  work/live_run/artifacts/teaching_lessons.json
```

The teaching engine must then fill each selected lesson with the source-specific turning point, what helped, what hurt, realistic alternative, trade-off, novelty label, next-game cue, and measurable drill. It must create the episode script and scene recipe before rendering.

## Rendering and QC adapters

The repository’s generic `scripts/render_episode.py` creates a scene manifest and reports the backend selected. It is intentionally an adapter boundary. A deployment must connect a verified HyperFrames/FFmpeg implementation or another authorized renderer for actual media output. If Kinocut is not installed and configured, the agent must report the fallback backend rather than claiming Kinocut ran.

The generic `scripts/run_human_watch_qc.py` creates four explicit review contracts. It does not pretend to watch the final MP4. A live deployment must connect independent rendered-video review for temporal context, coaching usefulness, session memory/repetition, and audio/pacing. Local metadata and loudness checks are useful gates but cannot replace those viewer passes.

## Minimum live-run acceptance

A run is ready for a human to watch only when the output directory contains a source manifest, player profile, goal record, raw candidate inventory, resolved event map, session map, contextual coaching map, teaching ledger, episode script, scene recipe, scene manifest, final MP4, technical QC, and four human-watch QC receipts. Every receipt must state whether it is an actual rendered-video review or only a local proxy.
