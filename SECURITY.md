# Security Policy

This project processes user-owned gameplay recordings and optional player profiles. Treat every recording, profile, transcript, screenshot, and generated artifact as private by default.

## Do not commit

Never commit gameplay recordings, generated MP4 files, voice files, model weights, access tokens, API keys, passwords, private source URLs, or deployment credentials. Use environment variables, a secret manager, and mounted volumes. The repository’s ignore rules are defensive but are not a substitute for reviewing `git diff --cached` before a push.

## Deployment safeguards

Run each job in an isolated work directory. Leave the source recording untouched. Make profile persistence opt-in, external sharing explicit, and delete-after-run behavior configurable and auditable. Expose worker status only through an authenticated service when deployed beyond a local machine. Feature-detect optional external services and fail closed when credentials or authorization are missing.

## Reporting

For a suspected secret exposure, unauthorized source access, or unsafe publication, stop the affected run and report the issue privately to the repository owner. Do not paste credentials or private media into a public issue.

## Scope

The repository provides workflow contracts and adapters; it does not guarantee the security posture of a hosting provider, object store, queue, model endpoint, or third-party renderer. Review those components separately before production deployment.
