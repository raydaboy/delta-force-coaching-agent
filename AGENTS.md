# AGENTS.md — Gameplay Coaching Agent Contract

## Mission

Build a useful coaching session from a user-authorized gameplay recording. Optimize for the user’s stated goal, not for raw combat count, model excitement, or video length. The default pure-gameplay mode removes filler and keeps complete meaningful engagements with enough setup and consequence to understand the decision.

## Mandatory startup

Read this file first. If no player profile exists, offer the optional profile questionnaire before the match-goal questionnaire. Then read the skill file matching the requested operation. For a full coaching video, read these in order: `skills/context-aware-fight-detector/SKILL.md`, `skills/gameplay-session-coach/SKILL.md`, `skills/teaching-engine/SKILL.md`, `skills/interactive-coaching-script/SKILL.md`, `skills/session-coaching-explainer/SKILL.md`, `skills/coaching-scene-qc/SKILL.md`, and `skills/pure-gaming-highlights/SKILL.md`. Inspect the applicable schema before writing each JSON artifact. Never rely on previous chat context as the only specification.

## Pipeline invariants

1. The player profile and match goal are separate data objects. The profile calibrates teaching; the goal judges decisions.
2. The player goal is data. Capture it before analysis and keep it unchanged in `goal_record.json`.
3. A raw candidate is not a fight. Preserve every candidate, including negative candidates, then run the deterministic resolver.
4. A promoted fight needs both an interaction and a consequence. A sighting, ADS frame, body, death crate, loot page, doorway peek, angle clear, heal, explosion, or generic audio peak is not enough by itself.
5. Maintain tactical memory. Merge uninterrupted exchanges into one cluster; split only after a meaningful reset, substantial relocation, objective change, or sustained loss of contact.
6. Every selected fight must show setup, real first combat, turning point, visible outcome, and short useful aftermath. A review begins only after the outcome.
7. Every spoken claim is labelled `observed`, `inferred`, or `unknown`. Do not invent enemy locations, intent, teammate presence, loot value, or guaranteed counterfactual results.
8. Questions appear before reveals. Use a 2–4 second thinking window when the player could answer from the paused frame.
9. Keep coaching specific. Use the teaching-engine contract: identify the goal conflict, turning point, what helped, what hurt, a local realistic alternative, the trade-off, one next-game cue, and a measurable drill. Reject any alternative that could be pasted into another fight unchanged.
10. Do not use memes, stickers, reaction graphics, decorative overlays, downloaded footage, or copyrighted inserts in pure-gameplay mode.
11. A technical pass does not replace a human-watch pass. Run temporal context, coaching usefulness, session-memory/repetition, and final audio/pacing reviews on the rendered MP4 itself.
12. When the user requests a printable session document, generate the optional Session Workbook & Tactical Playbook only from approved lessons and a local snapshot manifest. Validate source windows, evidence classes, local alternatives, cues, drills, and snapshot references before rendering. Keep source video, extracted snapshots, and generated PDFs outside Git.
13. When the user requests a player-facing tactical summary, write it in the standard format at `docs/tactical_playbook_standard.md`: Match Objective, Match Overview, Key Strengths, Primary Adjustments, scenario-based Tactical Decision Breakdown, Core Rules & Practice Plan, and Evidence Limits. Preserve `OBSERVED`, `INFERRED`, and `UNKNOWN` when the source has uncertainty.

## Player-profile policy

Use prior games, roles, experience, self-rated proficiency, and learning preferences to calibrate vocabulary, analogy difficulty, review depth, and drills. Do not use them to override what the current video proves. If the self-rating and observed behavior differ, label the difference as a hypothesis and invite correction. Do not infer age, identity, health, or ability from the profile.

## Goal policy

If the user says the goal is extraction with valuable loot, rank choices in this order: preserve the loot route; solve an enemy that is already a nearby threat; then improve mechanics. Do not label every enemy sighting as mandatory combat. When a forced fight becomes unfavorable, use a conservative default: take the first safe exchange, then disengage when serious damage, bad position, or loss of a safe win path threatens extraction. If the user gives a different policy, persist that policy and use it instead.

## Output contract

A complete run must produce at least the following files:

| Artifact | Required contents |
| --- | --- |
| `player_profile.json` | Prior games, roles, experience, self-rated proficiency, teaching preferences, and privacy choices |
| `source_manifest.json` | Path, duration, dimensions, frame rate, streams, rights note, limitations |
| `goal_record.json` | Questionnaire result and explicit engagement policy |
| `raw_candidate_inventory.json` | Every broad candidate with source times and evidence |
| `resolved_event_map.json` | All resolved events plus promoted fights and rejection reasons |
| `session_map.json` | Patterns, strengths, weaknesses, evidence ledger, priorities, unknowns |
| `contextual_coaching_map.json` | Selected fights, boundaries, goal relation, risk, novelty, review depth |
| `teaching_lessons.json` | Per-fight lesson type, evidence classes, local alternative, progression label, cue, and drill |
| `trim_omission_ledger.json` | Kept fights, omitted fights, omitted ranges, reasons |
| `episode_script.json` | Question/reveal/alternative/drill beats and evidence references |
| `scene_manifest.json` | Render order, clip paths, visual lifetimes, audio timing |
| `final_qc_report.json` | Human-watch findings, technical measurements, severity, corrections, recheck |
| Final MP4 | H.264/AAC, measured loudness, true peak below target, no stale overlays |
| Optional `session_workbook.json` | Printable training-workbook/playbook input containing selected lessons, reflection prompts, next-session rules, practice plan, and source-linked snapshot IDs |
| Optional `tactical_playbook.md` | Fast player reference using the standard objective, strengths, adjustments, scenario rules, drills, and evidence-limits format |

## Failure handling

If a fight boundary is uncertain, keep it as `contact`, `information_limited`, or `unresolved` rather than promoting it. If the source is too compressed to prove a claim, state the limitation. If a render backend is unavailable, use the documented fallback and report the actual backend. If any human-watch pass reports a blocker or major, stop delivery, correct the map/script/composition, rerender, and rerun the affected passes.

## Deployment behavior

A deployment must be reproducible from a clean checkout. Profile persistence must be opt-in, external sharing must be explicit, and delete-after-run must be honored. It must accept a source path or mounted upload, create an isolated work directory, write artifacts to a declared output directory, and leave the source untouched. It must not require credentials for local-only operation. Optional services such as speech synthesis, LLM analysis, storage, or queues must be feature-detected and have explicit fallbacks. Never commit secrets or user recordings.

## Repository development & verification

- `python3 -m pip install -e .` works in this checkout because `pyproject.toml` sets `packages = []` (avoids the setuptools flat-layout error from the multiple top-level dirs `deploy`, `skills`, `configs`, `schemas`, `templates`). On a fresh upstream clone before that fix it fails; install deps directly as a fallback: `pip install 'jsonschema>=4.23,<5' 'numpy>=1.26,<3' 'pillow>=10,<12' 'soundfile>=0.12,<1'`.
- `make smoke` passes in this checkout: `scripts/test_context_detector.py` paths were made repo-relative and a synthetic `tests/fixtures/context_detector_regression_fixture.json` was added (asserts 3 fights / 7 rejected lookalikes). On upstream it is still broken (hardcoded `/home/ubuntu/...` paths, missing fixture).
- Working verification path: `python -m pytest` (tests/), then the smoke-teaching validators `make smoke-teaching` (runs `validate_teaching.py`, `validate_episode_script.py`, `validate_episode_handoff.py`, `validate_edit_map.py` against `examples/`). All pass with dependencies installed directly. CI's full sequence is in `.github/workflows/validate.yml`.
- JSON artifacts are validated against `schemas/`. When changing a schema, update its validator and the `examples/` fixture in the same change. Media artifacts (`work/`, `*.mp4`, snapshots, PDFs) stay out of Git and off the machine-readable handoff list.
- This repo ships **no video model**. Candidate events for `build_candidate_inventory.py` come from the `frame_analyzer` sub-agent (model `opencode/mimo-v2.5-free`, multimodal), which emits `raw_candidate_inventory.json`-shaped JSON from frames/clips. The deterministic resolver (`resolve_candidates.py`) — not the model — decides what is a fight.
- Frame preparation for analysis uses **OpenCV** (`scripts/sample_frames.py`, cv2): it samples frames into `work/frames/*.png` plus `frames_manifest.json`, which the `frame_analyzer` sub-agent consumes. Install with the `frame-analysis` extra (`pip install '.[frame-analysis]'`) or `opencv-python-headless` directly.
- Optional local TTS (`kokoro-onnx`) is **force-installed in the Python 3.14 venv via `pip install --ignore-requires-python`** because its wheels cap at `<3.14`. Model/voice assets are NOT on PyPI and must be fetched separately. In this sandbox GitHub release-assets DNS and HuggingFace (`resolve`/`api`) both fail (401), but the **SourceForge mirror works**: `https://sourceforge.net/projects/kokoro-onnx.mirror/files/model-files-v1.1/kokoro-v1.0.int8.onnx/download` (114 MB) and `.../voices-v1.0.bin/download` (28 MB) → place in `/root/.cache/kokoro/`. Verified: `Kokoro(model, voices).create(text, voice='af_sarah', speed=1.0, lang='en-us')` returns 24 kHz samples; synthesis runs on CPU (no GPU here; onnxruntime logs a harmless `Permission denied /sys/class/drm` GPU-discovery warning).

## Design & composition tooling (OpenDesign + Diffusion Studio)

- **Asset design — OpenDesign** (`nexu-io/open-design`, open-source agent-native design tool). It generates the visual layer for the episode: overlay cards, `observed`/`inferred`/`unknown` evidence tags, causal strips, thumbnails, and a `DESIGN.md` brand contract. Wire it into this agent with `od mcp install opencode` (desktop/Docker must be running); then the `design_assets` sub-agent (`~/.config/opencode/agent/design_assets.md`) drives it. Keep generated assets in `work/assets/` (gitignored). OpenDesign also integrates HyperFrames (HTML+CSS+GSAP → headless Chrome + FFmpeg → MP4) if motion-graphic titles are wanted.
- **Video editing / Composer — Diffusion Studio** (`diffusionstudio/editor`, MPL-2.0, "video editor built for agents"). `render_episode.py --backend diffusionstudio` emits a JSX composition project to `work/render/diffusion_project/index.jsx` from `contextual_coaching_map.json` (one `<scene>` per selected fight: a `<video>` source clip plus a question/reveal `<text>` overlay, timed in frames at 30 fps). Open the project with `dapi open work/render/diffusion_project` (or `npx skills add diffusionstudio/skills`, then `/editor`), refine on the canvas, and render. `dapi media probe|grab|filmstrip|waveform|transcribe|listen` can replace the repo's `inspect_source.py`/`extract_workbook_snapshots.py` for richer media understanding.
- **Headless Diffusion Studio is NOT usable here.** `@diffusionstudio/core`'s `Encoder` *unconditionally* creates an `OfflineAudioContext` and calls `audioWorklet.addModule(...)`. The Web Audio `AudioWorklet` API is entirely absent in this PRoot/Android Chromium and in GitHub Actions' Chromium (verified under headless-shell, `--headless=new`, full Chromium + Xvfb, and `--disable-features=AudioServiceOutOfProcess` — `window.AudioWorklet` is `undefined` in all). So the JSX output is only renderable on a real desktop machine running the Diffusion Studio app/`dapi`.
- **Working render backend — FFmpeg (`scripts/render_ffmpeg.py`).** Because headless Diffusion Studio can't run, the actual MP4 is produced on-device with FFmpeg (no cloud needed). `render_episode.py --backend ffmpeg` dispatches to it. It consumes `contextual_coaching_map.json` (`selected_fights`): trims each fight from `--source` footage (or generates a solid title card when no source is supplied), burns a question/reveal caption overlay via a Pillow-rendered PNG (no drawtext/font dependency), and optionally synthesizes narration with Kokoro (feature-detected — silent if `kokoro_onnx` is unavailable). Output is H.264/AAC. Verified end-to-end on this device: 1920×1080, captioned, Kokoro-narrated MP4. Requirements: `ffmpeg` on PATH (has libx264 + aac), Python `Pillow`, and optionally `kokoro-onnx` (model/voices in `/root/.cache/kokoro/`, env-overridable via `KOKORO_MODEL`/`KOKORO_VOICES`). Run with whichever Python has both `Pillow` and `kokoro_onnx` installed.
