# Highlight Map Schema

Use a JSON map with source-backed ranges. Keep source time in seconds so it can be converted directly into a Kinocut timeline.

```json
{
  "source_file": "/path/to/gameplay.mp4",
  "target_duration_seconds": 240,
  "excluded_ranges": [
    {"start": 22, "end": 51, "reason": "sponsor"}
  ],
  "clips": [
    {
      "label": "Round 1 — Red Corridor",
      "kind": "combat",
      "source_start": 90,
      "source_end": 132,
      "keep_complete": true,
      "outcome": "kill and immediate reposition",
      "notes": "Keep approach, first contact, damage exchange, kill, and two seconds of aftermath."
    },
    {
      "label": "Loot reward",
      "kind": "loot",
      "source_start": 169,
      "source_end": 176,
      "keep_complete": false,
      "notes": "Show only the rare item and the player reaction; remove repeated sorting."
    }
  ]
}
```

## Required fields

`source_file` identifies the local source. `target_duration_seconds` sets the intended assembled runtime. `clips` is an ordered list of source ranges. Each clip requires a `label`, `kind`, `source_start`, and `source_end`. Combat clips must set `keep_complete` to `true` and should include an `outcome`.

Allowed `kind` values are `combat`, `loot`, `traverse`, `extraction`, `transition`, and `context`. Use `excluded_ranges` for sponsors, ads, and material that must not appear.

## Boundary rules

A combat range should begin early enough to establish the tactical setup and end only after the decisive moment and immediate outcome. Do not use a kill timestamp alone as the clip. If the source contains a long fight, remove only redundant inactivity while keeping each causal exchange intelligible.

Keep loot under roughly 20–25% of the assembled runtime by default. Use a short loot range as a reward or transition, not as a substitute for a fight. Validate the map with `scripts/validate_edit_map.py` before rendering.
