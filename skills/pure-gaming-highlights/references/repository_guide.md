# Open-Source Gaming Highlight Repository Guide

Use these repositories as optional evidence sources around the Kinocut workflow. Do not clone or install them unless the current task benefits from the specific capability and the license/dependencies are acceptable.

| Repository | What it contributes | Practical role | Important caveat |
|---|---|---|---|
| [Flowtter/crispy](https://github.com/Flowtter/crispy) | Game-specific visual highlight detection using neural networks, image recognition, and OCR; configurable confidence, frame rate, and timing buffers | Candidate detection for supported games or adapted models | MIT license; requires game-specific models/adaptation and is not a complete continuity-aware editor |
| [Aseiel/VideoHighlighter](https://github.com/Aseiel/VideoHighlighter) | Local scene, motion, audio, object, action, transcript, subtitle, timeline, and highlight analysis | Broad local candidate generation and visual/search support | Depends on local AI/model setup; use as an analyzer, not as the final editorial authority |
| [msylvester/Clipception](https://github.com/msylvester/Clipception) | Audio/excitement/laughter and transcription-based engagement ranking with clip extraction | Optional ranked candidate discovery | MIT license; uses Whisper/OpenRouter/CUDA-oriented dependencies; no published releases and limited project history |
| [artkulak/twitch-stream-highlights-detection](https://github.com/artkulak/twitch-stream-highlights-detection) | Combines audio tagging, movement scoring, and live-chat sentiment over 10-second windows | Research reference for multimodal scoring | Unlicense; older web/server/cloud architecture; not a drop-in editor |

## Recommended architecture

Use Kinocut as the stable rendering and QC backbone. Add one analyzer at a time. For a fully local workflow, prefer VideoHighlighter or deterministic Kinocut signals. For supported game titles, Crispy may generate useful game-specific candidates. Use Clipception or Twitch Stream Highlights Detection only when their model and infrastructure costs are justified.

Merge analyzer outputs by confidence and evidence, then manually or multimodally inspect each candidate. Enforce a continuity rule after ranking: a candidate is not a final clip until its lead-in, engagement, decisive moment, and immediate outcome are present. Keep analyzer confidence, source timestamps, and the final editorial decision in the highlight map so the process remains auditable.

## What is not a substitute

None of the repositories above guarantees that a fight is complete, that a loot sequence is concise, or that a cut has a good energy curve. Automated detectors can identify a kill, loud reaction, scene change, or chat spike while missing the tactical setup and aftermath. The skill’s continuity-aware map and Kinocut review gate remain mandatory.
