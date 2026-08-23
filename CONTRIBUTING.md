# Contributing

Thank you for improving the Goal-Aware Gameplay Coaching Agent. Contributions should make the workflow more evidence-first, easier for another LLM to operate, or more useful to the player. The project values honest uncertainty over impressive but unsupported analysis.

## Before opening a change

Read [`AGENTS.md`](AGENTS.md), the relevant skill, and the schema for the artifact you will modify. Run `make test`, `make smoke`, and `make smoke-teaching` from a clean checkout. Do not add recordings, generated renders, model weights, credentials, or private URLs.

## Change principles

A detector change must include a regression case for both the event it promotes and the lookalike event it rejects. A teaching change must demonstrate a source-specific decision, an evidence-labelled explanation, a realistic alternative with a trade-off, a novelty/progression label, and a measurable drill. A schema change must update its example and validator in the same commit.

Keep raw candidates separate from resolved fights. Keep player profile data separate from match evidence. Do not use profile information to override what the current recording proves. Do not claim a rendering or QC backend ran unless its output exists and is recorded in the run manifest.

## Pull requests

Describe the problem, the artifact contracts affected, the validation commands run, and any known limitations. Include a small before/after example for teaching or selection changes. If the change affects a rendered video, provide the scene manifest and the human-watch QC receipts without committing the media itself.

## Local commands

```bash
make test
make smoke
make smoke-teaching
python3 -m py_compile scripts/*.py deploy/worker.py
```
