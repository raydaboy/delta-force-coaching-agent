# Session Workbook & Tactical Playbook

## Purpose

The **Session Workbook & Tactical Playbook** is a printable, player-facing training document generated from one approved gameplay coaching run. It combines two outputs that solve different problems:

| Component | Player need it serves |
| --- | --- |
| **Tactical playbook** | Explains the match story, major turning points, evidence, alternatives, and goal trade-offs in enough depth for a serious review. |
| **Training workbook** | Turns those findings into short drills, reflection prompts, next-session rules, and progress checks that the player can use away from the video. |

The document is deliberately **not** a transcript, a kill montage, or a screenshot dump. It normally targets **10–12 pages** and selects only the moments that teach a different reusable decision.

## Privacy and source boundary

The renderer is designed for a local private run directory. It consumes validated coaching artifacts plus a local snapshot manifest; it never downloads gameplay, embeds a source recording into Git, or requires screenshots to be committed.

> Keep recordings, extracted images, rendered PDFs, narration, private URLs, and credentials outside the repository. Commit only code, schemas, sanitized examples, tests, and documentation.

Every factual statement in the document must preserve the evidence vocabulary used by the coaching pipeline:

| Label | Meaning in the workbook |
| --- | --- |
| **OBSERVED** | Directly visible or audible in the selected snapshot or supported source window. |
| **INFERRED** | A cautious tactical interpretation grounded in visible timing, geometry, resources, or player state. |
| **UNKNOWN** | Hidden intent, unseen threats, unshown geometry, or any conclusion the recording cannot prove. |

## Recommended layout

The default layout is a compact 10–12 page A4/Letter portrait workbook. It can expand only when a user explicitly requests a deeper coaching dossier.

1. **Cover and session promise.** Match goal, one-sentence outcome, source duration, and the three things the player will improve.
2. **Match-at-a-glance.** A concise timeline of attempts, extraction result, selected turning points, strengths, and priorities.
3. **Strengths worth keeping.** Two or three repeatable choices that helped the player, with a short reason and a snapshot where available.
4–8. **Deep lesson spreads.** One spread per selected decision. Each contains an annotated snapshot, source window, decision question, evidence stack, causal chain, local alternative, trade-off, cue, drill, and reflection box.
9. **Loot and resource playbook.** Only when the match contains a meaningful loot, capacity, screen-time, medical, or extraction-value lesson.
10. **Next-session rules.** Three trigger-action rules, a pre-match intention, and a post-match reflection checklist.
11. **Practice plan.** Measurable drills grouped by match, next three fights, or practice range scope.
12. **Evidence and limits.** Snapshot index, source timestamps, unresolved questions, and renderer/QC provenance.

## Lesson spread contract

Every deep lesson needs an approved coaching-map entry and a linked snapshot. The renderer should reject a lesson that lacks a source window, evidence separation, local alternative, trade-off, cue, or measurable drill.

```json
{
  "lesson_id": "scan_reset",
  "title": "A scan warning must change the route",
  "source_window": {"start": 692.0, "decision": 692.0, "outcome": 703.0, "end": 710.0},
  "snapshot_id": "scan_warning",
  "goal_relation": "Threatened the extraction route before loot value was secured.",
  "observed": ["Position Exposed warning appears before first contact."],
  "inferred": ["Continuing on the direct lane creates an open first fight."],
  "unknown": ["Exact scan source and enemy count are not visible."],
  "decision_point": "Continue forward after the warning instead of taking the visible break in cover.",
  "alternative": {
    "action": "Break to the visible rock or building edge, stop sprinting, then identify the first firing lane.",
    "tradeoff": "Gives up a few seconds of tempo.",
    "likely_benefit": "Could improve the first shot and keep a reset route available."
  },
  "cue": "Scan: cover before gun.",
  "drill": {
    "trigger": "Any scan, exposure warning, or unexpected close contact.",
    "action": "Break line of sight before committing to the duel.",
    "success_condition": "Name one cover break and one firing lane before shooting.",
    "scope": "Next three forced fights."
  },
  "reflection_prompt": "What visible cover would have preserved your next decision here?"
}
```

## Snapshot policy

Snapshots are evidence anchors, not decoration. The local snapshot extractor may create full-resolution frame PNGs from an authorized source. An optional annotation file may describe pointers to visible warning text, doors, stairs, crates, cover edges, route lanes, or inventory UI. It must never draw hidden enemies, invent a safe route, or label an unshown location as fact.

The snapshot manifest should identify whether each callout is `OBSERVED`, `INFERRED`, or `UNKNOWN`. If no source-supported pointer is available, the renderer shows the image without fabricated graphics and prints the limitation in the evidence stack.

## Clone-run contract

The public repository will provide these commands:

```bash
# 1. Extract only the approved local evidence frames.
python3 scripts/extract_workbook_snapshots.py \
  --source /private/source.mp4 \
  --manifest /private/run/artifacts/workbook_snapshot_manifest.json \
  --output-dir /private/run/workbook/snapshots

# 2. Validate lesson data and snapshot references before PDF creation.
python3 scripts/validate_session_workbook.py \
  /private/run/artifacts/session_workbook.json \
  --snapshot-manifest /private/run/artifacts/workbook_snapshot_manifest.json

# 3. Generate the private PDF and an auditable build manifest.
python3 scripts/render_session_workbook.py \
  --input /private/run/artifacts/session_workbook.json \
  --snapshot-manifest /private/run/artifacts/workbook_snapshot_manifest.json \
  --output-dir /private/run/workbook/output
```

The generated build manifest must identify input files, selected lesson IDs, missing/optional snapshots, output paths, renderer version, and any limitation. A successful PDF render does not replace source-evidence validation, and it does not imply that an independent human reviewed the video.
