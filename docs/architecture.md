# Architecture

The system is a staged pipeline with explicit handoff artifacts. Each stage is deterministic where possible and replaceable where model judgment is required.

## Artifact graph

```text
player-profile questionnaire       match-goal questionnaire
       |                              |
       v                              v
player_profile.json              goal_record.json
       |                              |
       +--------------+---------------+
                      |
source --> source_manifest.json --> raw_candidate_inventory.json
                                      |
                                      v
                              resolved_event_map.json
                                      |
                                      v
                         session_map.json + learning agenda
                                      |
                                      v
                     contextual_coaching_map.json
                                      |
                                      v
                         episode_script.json
                                      |
                                      v
                source clips + narration + visual manifest
                                      |
                                      v
                     HyperFrames / FFmpeg composition
                                      |
                                      v
                    final MP4 + technical QC + human QC
```

## Components

| Component | Responsibility | Replaceable implementation |
| --- | --- | --- |
| Player profile | Persist prior games, roles, proficiency, learning preferences, and privacy choices | CLI questionnaire, web form, or API |
| Goal capture | Convert match-specific answers into a stable policy object | CLI questionnaire, web form, or API |
| Source inspector | Record media metadata and limitations | FFprobe wrapper |
| Candidate analyzer | Propose broad events and evidence | Multimodal LLM, game-specific model, or manual CSV |
| Context resolver | Promote only interaction-plus-consequence events and cluster tactical episodes | `context-aware-fight-detector` deterministic resolver |
| Session coach | Aggregate patterns and rank up to three priorities | LLM or structured analyst |
| Edit selector | Choose scenes by goal relevance and novelty | Rule-based filter plus analyst confirmation |
| Script writer | Build question-first reviews with evidence classes | LLM constrained by JSON schema |
| Composer | Render source clips, rewinds, stills, labels, and narration | HyperFrames plus FFmpeg fallback |
| QC | Audit temporal order, coaching specificity, repetition, audio, and mechanical integrity | Four human-watch roles plus scripts |
| Deployment worker | Run jobs, store artifacts, and expose status | Local CLI, container worker, queue-backed API |

## State and idempotency

Each run lives in its own work directory. Inputs are immutable. Every stage writes a named artifact and may be rerun without recomputing earlier stages when the input hash and configuration hash have not changed. A run manifest records the source hash, repository commit, configuration, backend versions, timestamps, and output paths.

Large files remain outside Git. A deployment may use local storage, an object store, or a mounted volume, but the artifact names and JSON contracts remain stable. Paths inside manifests may be absolute for local runs and URI-based for deployed runs.

## Evidence model

Evidence is attached to events, fights, claims, and visual annotations. A source frame or audio cue can support an `observed` claim. A tactical conclusion derived from visible geometry is `inferred`. Off-screen enemy intent, hidden teammates, and guaranteed counterfactual outcomes are `unknown` unless later evidence establishes them.

The profile is a calibration input, while the match goal is a decision-policy input. They must remain separate in the artifact graph and in prompts. The resolver is deliberately conservative. A raw candidate can contain a live target or a danger signal, but the final fight list requires a combat interaction and a combat consequence. Negative events are not thrown away: they become part of the audit trail and regression fixtures.

## Rendering model

The edit is a sequence of source clips and post-outcome review blocks. The source clip always precedes its review block. A review may contain a question, pause, rewind or freeze, observed/inferred/unknown labels, a compact causal strip, a realistic alternative, a trade-off, and a next-game cue. Visual elements have explicit start and end times; no annotation is allowed to persist merely because a fixed card is still on screen.

The source’s native aspect ratio is preferred. If a delivery target requires 16:9, the full gameplay canvas is letterboxed rather than cropped. The current example is a compressed ultrawide source and therefore uses a clean 16:9 letterbox to preserve HUD information.

## QC gates

A run is releasable only when all of these are true:

| Gate | Question |
| --- | --- |
| Evidence | Does every featured fight have a real exchange and visible outcome? |
| Temporal | Does each review start after the outcome, not before combat or extraction? |
| Coaching | Could a player apply this lesson to the visible situation next game? |
| Memory | Are repeated mistakes and progress labelled instead of restated? |
| Visual | Do annotations point only to evidence and disappear after their sentence? |
| Audio | Is game audio preserved during fights and narration intelligible without clipping? |
| Technical | Does the final MP4 pass metadata, duration, frame rate, loudness, and true-peak checks? |
| Rights | Is the source authorized and is automatic publishing disabled unless confirmed? |

A single blocker or major finding is sufficient to fail the run. Findings are corrected and rechecked; they are not averaged away.
