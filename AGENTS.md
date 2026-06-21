# AGENTS.md — SchemeWayfinder

> Cross-tool rules file (read by Antigravity and Cursor). These are always-active project instructions. Keep this concise; deep context lives in `.agents/rules/project-context.md`.

## Project
SchemeWayfinder — a multi-agent welfare-entitlement navigator. A citizen describes their situation (voice or text, 22 Indian languages) and receives the government schemes they qualify for, a document checklist, a pre-filled application draft, and a plain-language rejection-risk explanation.

- Stack: Python 3.11, Google Agent Development Kit (ADK), Gemini models, FastMCP, Bhashini (MCP), Cloud Run + Firestore.
- Built for the Kaggle × Google AI Agents: Intensive Vibe Coding Capstone (Agents for Good).
- Plan of record: `roadmap.md` (numbered specs, dependency order, status).

## Non-negotiable rules
- NEVER commit to `main` directly. Work on `feature/schemewayfinder-nishant`; PR into main.
- NEVER hardcode API keys or secrets. All secrets via `.env` → `app/core/config.py`; Secret Manager in production.
- NEVER persist identifiable citizen data (PII). Session-scoped state only (Firestore TTL). Logs are metadata-only (timestamp, language, scheme_count, latency) — never raw profile, audio, or identifying fields.
- NEVER add an AI tool as a commit co-author.
- A file is NOT done until its tests pass. Follow TDD: Red → Green → Refactor.

## How agents communicate
- Agents hand off via **structured outputs into shared state** (ADK `output_key` → `session.state`), not free-form text relay.
- Compose with ADK workflow agents: `SequentialAgent`, `ParallelAgent`, `LoopAgent`, plus LLM-driven delegation in the orchestrator.

## Code standards
- Pydantic models for all data in/out (`app/models/schemes.py`).
- Tenacity retries (3 attempts, exponential backoff) on every external API call (Gemini, Bhashini).
- Loguru logging with `request_id`; never log PII.
- Ruff for lint + format, line length 100.
- Package manager: `uv`, single source of truth `pyproject.toml` (no requirements.txt).

## Workflow
- Spec-driven. Each feature is a numbered spec from `roadmap.md` with a folder under `specs/`.
- Use the workflows in `.agents/workflows/` (`/create-spec`, `/check-spec-deps`, `/implement-spec`, `/verify-spec`).
- Plan before coding; produce the Implementation Plan + Task List artifacts and get review before executing.

## Course concepts to demonstrate (target all 6)
Multi-agent ADK (code) · custom MCP server + consumed MCP tool (code) · security/HITL (code/video) · deployability on Cloud Run (video) · agent skills (code/video) · Antigravity build (video).
