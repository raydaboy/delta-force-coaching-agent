# Kinocut Workflow Reference

Use the installed Kinocut CLI for deterministic media operations. Inspect exact help output on the current installation before using a command because flags can change between releases.

## Inspect and analyze

```bash
kino read-metadata INPUT
kino video-info-detailed INPUT
kino video-ai-transcribe INPUT -o analysis/transcript.json
kino video-ai-scene-detect INPUT -o analysis/scenes.json
kino audio-waveform INPUT -o analysis/waveform.json
```

If an analysis command fails because an optional model is unavailable, continue with deterministic metadata, scene detection, audio peaks, frame extraction, and manual or multimodal review. Never invent timestamps from a failed analyzer.

## Assemble a timeline

Create a JSON timeline from the map schema. A minimal video clip entry is:

```json
{
  "source": "/absolute/path/gameplay.mp4",
  "trim_start": 90.0,
  "duration": 42.0
}
```

Use `kino edit TIMELINE.json -o OUTPUT.mp4` to assemble the edit. Keep all source paths absolute and local. Avoid mixing source clips with different frame rates or resolutions when possible; if mixing is necessary, normalize deliberately and record the choice.

## Audio and polish

Preserve the source track by extracting it before adding any optional accents:

```bash
kino extract-audio EDIT.mp4 -f wav -o base_audio.wav
kino audio-compose -o mixed_audio.wav -d DURATION --tracks TRACKS_JSON
kino add-audio EDIT.mp4 mixed_audio.wav --duration-policy keep_video -o audio_edit.mp4
kino normalize-audio audio_edit.mp4 --lufs -16 -o normalized.mp4
```

Use `kino filter` with a modest `saturation` or `brightness` adjustment only when source conditions require it. Do not use aggressive grading to conceal poor continuity or unreadable gameplay. Keep true peak below clipping and verify the final measured loudness.

## Typography

Kinocut text styling is driven by the timeline’s text elements. Prefer a locally installed heavy font such as Noto Sans Black or another bold condensed display face. Use all-caps labels sparingly. Keep titles and labels within safe margins and away from HUD elements, minimaps, kill feeds, subtitles, weapon sights, and face/hand cameras.

## QC and inspection

```bash
kino video-quality-check FINAL.mp4 --format json
kino video-design-quality-check FINAL.mp4 --format json
kino extract-frame FINAL.mp4 --time SECONDS -o review/frame.png
```

Review at minimum the opening hook, every combat clip’s first contact, decisive outcome, and aftermath, every loot bridge, and the final payoff. Check codecs, dimensions, duration, frame rate, audio stream, and source rights separately. Kinocut’s automated score is evidence, not a substitute for continuity review.
