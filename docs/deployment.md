# Deployment

## Local deterministic run

Use a clean Python environment and install the base dependencies. FFmpeg must be available on `PATH`. For local narration, install the optional `local-tts` extra and place the Kokoro model and voice pack under a private model directory. For model-assisted analysis, configure the provider through environment variables; never write API keys into JSON artifacts.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[autonomous]'
ffmpeg -version
```

Run a small fixture before processing a full recording. Keep the source under a mounted media directory and write all artifacts under a run-specific work directory.

## Container worker

The worker should contain Python, FFmpeg, the repository, and optional TTS/model assets. Mount three volumes:

| Volume | Purpose | Writable |
| --- | --- | --- |
| `/data/input` | User-authorized source videos | read-only preferred |
| `/data/models` | Optional local speech or vision models | read-only |
| `/data/runs` | Per-run artifacts and final MP4s | yes |

A worker entry point should accept a run ID, source path, and configuration path. It should create `/data/runs/<run_id>/`, record the repository commit and tool versions, and return a status JSON with artifact paths. The worker must be restartable: completed artifacts are reused when their input hash and configuration hash match.

## Optional web/API layer

A web service is not required for local operation. If a deployment adds an API, keep it thin: upload or reference the source, collect the goal questionnaire, enqueue a run, expose status, and return artifact links. The service should call the same CLI scripts used locally rather than reimplement detection or QC logic. Upload limits, authentication, authorization, and object-store lifecycle rules must be configured outside this repository.

## Secrets

Use environment variables or a secret manager for model-provider keys, object-store credentials, webhook secrets, and authentication tokens. Recommended names are `OPENAI_API_KEY`, `OPENAI_API_BASE`, `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, and `COACHING_WEBHOOK_SECRET`. Do not include values in `.env` files committed to Git. Treat source URLs and user recordings as private unless the user explicitly authorizes publication.

## Backends

Prefer Kinocut when it is installed and verified. If it is unavailable, use the repository’s HyperFrames/FFmpeg fallback. Record the actual backend in `run_manifest.json` and `final_qc_report.json`. A fallback render is acceptable only when it passes the same temporal, coaching, audio, and technical QC gates.

## Persistent execution

For long renders, use a persistent worker, a queue, or a job scheduler rather than a browser request timeout. The job status should distinguish `queued`, `analyzing`, `selecting`, `scripting`, `rendering`, `qc`, `complete`, and `failed`. Keep logs per run and clean up abandoned temporary files according to the deployment’s retention policy.

## Publishing

The default deployment ends at artifact delivery. Posting to a platform, sending email, or sharing a public URL is a separate explicit operation that requires user confirmation. Do not auto-publish a gameplay recording from a background worker.
