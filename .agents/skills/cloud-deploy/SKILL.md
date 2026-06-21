---
name: cloud-deploy
description: Containerize SchemeWayfinder and deploy to Cloud Run with Firestore session state, without baking secrets into the image. Use for deployment tasks.
---

# Skill: cloud-deploy

When asked to deploy:

1. Write `deploy/Dockerfile` (repo-root build context; `uv` install from `pyproject.toml`; non-root user).
2. Write `deploy/deploy.sh` running `gcloud run deploy schemewayfinder --source .` with: secrets via Secret Manager (NEVER baked into the image or committed), Firestore for session state, and region asia-south1.
3. Ensure `app/db/session.py` uses Firestore with a session TTL (PII minimization).
4. Wire OpenTelemetry tracing (`app/core/telemetry.py`) so agent runs are observable (supports the eval/trace-review story).
5. Document exact reproduce steps in `README.md` (deploy section).
6. Verify: build succeeds locally; the deploy script is idempotent; no secret strings anywhere in the repo (the secret-scan hook must pass).

Output: Dockerfile, deploy.sh, session/telemetry wiring, and README deploy docs.
