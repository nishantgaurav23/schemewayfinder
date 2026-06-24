# SchemeWayfinder — Roadmap

> Spec-driven, test-driven build plan for the Kaggle × Google AI Agents: Intensive Vibe Coding Capstone (Agents for Good).
> Every feature is a numbered spec with a dedicated folder under `specs/`, built Red → Green → Refactor.

---

## Project

**SchemeWayfinder** — a multi-agent system that takes a citizen's profile (spoken or typed in any of 22 Indian languages) and returns the welfare schemes they qualify for, a document checklist, a pre-filled application draft, and a plain-language rejection-risk explanation.

- **Agents:** Google Agent Development Kit (ADK), Python 3.11
- **Models:** Gemini (Flash for routing/extraction, Pro for eligibility reasoning)
- **Tools:** custom `scheme-search` MCP server (FastMCP) + consumed Bhashini MCP tool (ASR/MT/TTS)
- **Deploy:** Cloud Run (container) + Firestore (session state, TTL)
- **Build:** Antigravity + agent skills; spec-driven/TDD workflow

---

## How this roadmap is used

| Command | Invocation | Purpose |
|---------|------------|---------|
| Create spec | `/create-spec S1.1 scheme-corpus-loader` | Creates `spec.md` + `checklist.md` in the spec folder from this roadmap. |
| Check deps | `/check-spec-deps S4.1` | Verifies all prerequisite specs are `done` and their tests pass. |
| Implement spec | `/implement-spec S1.1` | TDD implementation following spec + checklist. |
| Verify spec | `/verify-spec S1.1` | Post-implementation audit: tests, lint, outcomes, wiring. |

**Status flow:** `pending` → `spec-written` → `done`. Update the status in **both** the phase table and the Master Spec Index whenever it changes.

**Spec folder convention:**
```
specs/spec-{id}-{slug}/
  spec.md        ← detailed specification
  checklist.md   ← implementation progress tracker
```

---

## Skills (project-scoped, under `.agents/skills/`)

Reusable capability modules the coding agent loads on demand. Build these early (Phase 0) so every later spec benefits.

| Skill | Path | What it does |
|-------|------|--------------|
| `adk-agent-scaffold` | `.agents/skills/adk-agent-scaffold/SKILL.md` | Scaffolds a new ADK sub-agent (LlmAgent/Sequential/Parallel/Loop) with a matching pytest file, wired to the orchestrator. Encodes our agent-contract + structured-output conventions. |
| `mcp-tool-scaffold` | `.agents/skills/mcp-tool-scaffold/SKILL.md` | Scaffolds a FastMCP tool (schema, handler, test) and registers it on the `scheme-search` server. |
| `eval-harness` | `.agents/skills/eval-harness/SKILL.md` | Adds a persona test case + scorer entry to `eval/`; runs the eligibility precision/recall + auditor before/after report. |
| `cloud-deploy` | `.agents/skills/cloud-deploy/SKILL.md` | Containerize + `gcloud run deploy` with Firestore wiring and a reproducible deploy script; never bakes secrets in. |

---

## Hooks (Git hooks under `githooks/`)

Automation that enforces the standards on every change — TDD and security guardrails that don't depend on memory.

| Hook | Trigger | Action |
|------|---------|--------|
| `pre-commit-tests` | before commit | Run `make test`; block commit on any failing test. |
| `pre-commit-lint` | before commit | Run `ruff check + format`; block on lint errors in changed files. |
| `secret-scan` | before commit / on write | Block any commit containing API-key-like strings or `.env` contents; enforce "never hardcode secrets". |
| `no-pii-guard` | on write to `agents/`, `mcp/` | Warn if code paths persist raw profile/PII beyond session scope (enforces session-TTL rule). |
| `post-implement-status` | after `/implement-spec` | Remind to flip roadmap + checklist status to `done`. |

> Mirror Nishant's SehatSamjho `settings.local.json` pattern: pre-approve the safe, repeated bash commands (tests, lint, deploy) so the loop stays fast, and keep destructive commands gated.

---

## Project structure (created by S0.1)

This is the canonical layout. S0.1 scaffolds the entire tree below in one step so every later spec has its target folder ready.

```
schemewayfinder/                  # repo root
├── AGENTS.md                     # project instructions (auto-loaded each session)
├── README.md                     # project overview (GitHub + judges)
├── roadmap.md                    # this file — spec index the commands read
├── pyproject.toml                # uv, single source of truth (no requirements.txt)
├── Makefile                      # make test / lint / eval / mcp / run / deploy
├── .env.example                  # placeholders only — never commit the real .env
├── .gitignore                    # .env, .venv, __pycache__
│
├── .agents/                      # Antigravity tooling (workflows, skills)
│   ├── settings.json             # permissions + pre-commit hooks
│   ├── commands/                 # slash-commands
│   │   ├── create-spec.md
│   │   ├── check-spec-deps.md
│   │   ├── implement-spec.md
│   │   └── verify-spec.md
│   └── hooks/
│       ├── secret-scan.sh
│       └── no-pii-guard.sh
│
├── .agents/                      # agent skills (the "Agent skills" course concept)
│   └── skills/
│       ├── adk-agent-scaffold/SKILL.md
│       ├── mcp-tool-scaffold/SKILL.md
│       ├── eval-harness/SKILL.md
│       └── cloud-deploy/SKILL.md
│
├── specs/                        # one folder per spec (created by /create-spec)
│   └── spec-S0.1-repo-scaffold/
│       ├── spec.md
│       └── checklist.md
│
├── app/                          # SchemeWayfinder application code
│   ├── __init__.py
│   ├── main.py                   # entry point (agent runner / web)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # settings from .env (pydantic-settings)
│   │   └── telemetry.py          # OpenTelemetry tracing over agent runs
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── contracts.py          # shared state schema + output_key handoffs
│   │   ├── orchestrator.py       # LlmAgent root; delegation; HITL gate
│   │   ├── intake.py             # text/voice → CitizenProfile (Bhashini)
│   │   ├── matcher.py            # EligibilityMatcher (ParallelAgent)
│   │   ├── documents.py          # DocumentChecklistAgent
│   │   ├── form_filler.py        # FormFillerAgent (draft + PDF)
│   │   ├── auditor.py            # RejectionRiskAuditor (LoopAgent critic)
│   │   ├── explainer.py          # plain-language + TTS + disclaimer
│   │   └── guards.py             # input guardrails (before_model_callback)
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── scheme_search/        # custom MCP server (FastMCP)
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   └── tools.py          # find_schemes(profile), get_scheme(id)
│   │   └── bhashini/             # consumed MCP tool
│   │       ├── __init__.py
│   │       └── client.py         # ASR / NMT / TTS via McpToolset
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py             # myScheme corpus → normalized schema
│   │   └── index.py              # embeddings + vector index (cached)
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemes.py            # Scheme, EligibilityRule, CitizenProfile, MatchResult
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py            # Firestore session store (TTL), PII minimization
│   └── web/
│       ├── __init__.py
│       └── seed.py               # demo personas for the video
│
├── eval/                         # the technical differentiator
│   ├── personas/                 # labeled citizen personas + expected matches
│   ├── scorer.py                 # precision/recall + auditor before/after
│   └── REPORT.md                 # results
│
├── tests/                        # mirrors app/ ; pytest ; all externals mocked
│   ├── __init__.py
│   ├── conftest.py
│   ├── agents/
│   ├── mcp/
│   ├── data/
│   └── db/
│
├── deploy/
│   ├── Dockerfile
│   └── deploy.sh                 # gcloud run deploy (secrets via Secret Manager)
│
└── docs/                         # submission assets
    ├── architecture.png
    ├── cover-560x280.png
    ├── video-link.md
    └── antigravity/              # S0.5 build-capture artifacts
```

> **Placement rule:** root holds *content Antigravity reads* (`AGENTS.md`, `README.md`, `roadmap.md`); `.agents/` holds *tooling that drives Antigravity* (workflows, skills). `AGENTS.md` is advisory; the security guarantees live in `githooks/` (enforced), not in `AGENTS.md` prose.

---

## Build phases (17-day capstone)

### Phase 0 — Foundations, skills & hooks  *(Days 1–2)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S0.1 | Repo + project scaffold | whole tree (see **Project structure**) | — | done | Create the entire folder tree from the Project structure section: all dirs + `__init__.py` stubs, `pyproject.toml` (uv, no requirements.txt), `Makefile`, `.gitignore`, `.env.example`, empty placeholder modules. Python 3.11; ruff line length 100; pytest configured. After this, `make test` runs (even if 0 tests) and every later spec has its target file ready. |
| S0.2 | Skills authored | `.agents/skills/*/SKILL.md` | S0.1 | done | Author the 4 skills above. Each SKILL.md: trigger, steps, conventions, output. |
| S0.3 | Git Hooks | `githooks/` | S0.1 | done | Author the hooks above; pre-approve safe bash (test/lint/deploy). No secrets in repo. |
| S0.4 | Spec workflows | `.agents/workflows/*.md` | S0.1 | done | Port create-spec / check-spec-deps / implement-spec / verify-spec, retargeted to ADK paths + `make test`/`make lint`. |
| S0.5 | Antigravity build capture | `docs/antigravity/` | S0.1 | spec-written | Build inside Antigravity; capture Manager surface, an implementation plan, and browser-verification artifacts as B-roll for the video. This is the deliverable that demonstrates the **Antigravity** course concept. |

### Phase 1 — Data layer & scheme corpus  *(Days 2–3)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S1.1 | Scheme corpus loader | `app/data/loader.py` | S0.1 | done | Load myScheme corpus (HF `shrijayan/gov_myscheme` / Kaggle dataset) into a normalized schema: id, name, level (central/state), eligibility rules, required docs, apply URL. Bundle for reproducibility. |
| S1.2 | Corpus schema + Pydantic models | `app/models/schemes.py` | S1.1 | done | `Scheme`, `EligibilityRule`, `CitizenProfile`, `MatchResult` models. Every field typed; validation. |
| S1.3 | Embeddings + vector index | `app/data/index.py` | S1.1, S1.2 | done | Build embeddings over scheme eligibility text; local vector store for retrieval. Deterministic, cached. |

### Phase 2 — Custom MCP server (scheme-search)  *(Days 3–4)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S2.1 | FastMCP server bootstrap | `app/mcp/scheme_search/server.py` | S0.2, S1.3 | done | Stand up FastMCP server; health/list tools; runnable via `python -m`. |
| S2.2 | `find_schemes(profile)` tool | `app/mcp/scheme_search/tools.py` | S2.1 | done | Returns ranked candidate schemes for a `CitizenProfile`, with rule-level match detail. Use `mcp-tool-scaffold` skill. |
| S2.3 | get_scheme(id) tool | app/mcp/scheme_search/tools.py | S2.1 | done | Returns full scheme detail incl. required documents + apply URL. |
| S2.4 | MCP integration test | `tests/mcp/test_scheme_search.py` | S2.2, S2.3 | done | End-to-end: client calls tools, asserts structured results against known fixtures. |

### Phase 3 — Core agents (English text path)  *(Days 4–6)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S3.1 | Agent contracts + shared state | `app/agents/contracts.py` | S0.2, S1.2 | done | Define `output_key` → session.state schema; structured handoffs (no free-form relay). |
| S3.2 | IntakeAgent (text) | `app/agents/intake.py` | S3.1 | done | Free-text → structured `CitizenProfile`. English-only first. |
| S3.3 | EligibilityMatcherAgent | `app/agents/matcher.py` | S2.2, S3.1 | done | ParallelAgent fan-out: central ∥ state scoring via `find_schemes`. Writes ranked matches to state. |
| S3.4 | Orchestrator (delegation) | `app/agents/orchestrator.py` | S3.2, S3.3 | done | LlmAgent root; LLM-driven delegation; composes the run. Use `adk-agent-scaffold` skill. |

### Phase 4 — Document, form & the auditor critic loop  *(Days 6–9)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S4.1 | DocumentChecklistAgent | `app/agents/documents.py` | S2.3, S3.4 | done | For each matched scheme, assemble required-document checklist. |
| S4.2 | FormFillerAgent | `app/agents/form_filler.py` | S3.2, S4.1 | done | Draft application from profile; emit structured form / PDF + apply URL. |
| S4.3 | RejectionRiskAuditorAgent (LoopAgent) | `app/agents/auditor.py` | S3.3 | done | **Critic loop**: re-check each match against eligibility rules; flag weak/hallucinated eligibility; `max_iterations`, early-exit on pass. Quality guardrail. |
| S4.4 | ExplainerAgent | `app/agents/explainer.py` | S4.2, S4.3 | done | Plain-language summary + next steps + disclaimer. |
| S4.5 | TDD eligibility test set | `eval/personas/`, `eval/scorer.py` | S3.3, S4.3 | done | Labeled personas (farmer, widow-pension, student, PwD) with known-correct matches. Use `eval-harness` skill. |

### Phase 5 — Multilingual layer (Bhashini MCP)  *(Days 9–11)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S5.1 | Bhashini MCP tool wiring | `app/mcp/bhashini/client.py` | S0.2, S3.2 | done | Consume Bhashini via McpToolset: ASR, NMT, TTS. Tenacity retries; graceful timeouts; audio format handling. |
| S5.2 | IntakeAgent voice + in-language | `app/agents/intake.py` | S5.1, S3.2 | done | Voice-in → text; translate to working language; carry user's language through. Hindi + 2 more tested. |
| S5.3 | ExplainerAgent TTS out | `app/agents/explainer.py` | S5.1, S4.4 | done | Translate summary back + speak via TTS in user's language. |

### Phase 6 — Security & human-in-the-loop  *(Day 12)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S6.1 | HITL confirmation gate | `app/agents/orchestrator.py` | S4.2 | pending | Pause for explicit user confirmation before generating any application draft. |
| S6.2 | Input guardrails | `app/agents/guards.py` | S3.2 | pending | ADK `before_model_callback` on free-text: injection/abuse filtering; out-of-scope redirect. |
| S6.3 | PII minimization + session TTL | `app/db/session.py` | S0.1 | pending | No persistent identifiable data; Firestore session TTL; metadata-only logs (mirror SehatSamjho "zero PHI" rule). |
| S6.4 | Disclaimer injection | `app/agents/explainer.py` | S4.4 | pending | `after_model_callback` appends "informational, not an eligibility determination" to every result. |

### Phase 7 — Deploy & observability  *(Days 13–14)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S7.1 | Containerize | `deploy/Dockerfile` | S3.4 | pending | Repo-root build context; uv install from pyproject. |
| S7.2 | Cloud Run deploy script | `deploy/deploy.sh` | S7.1, S6.3 | pending | `gcloud run deploy --source .`; secrets via Secret Manager; reproducible. Use `cloud-deploy` skill. |
| S7.3 | Firestore session store | `app/db/session.py` | S6.3 | pending | Session state persistence with TTL. |
| S7.4 | Tracing / observability | `app/core/telemetry.py` | S3.4 | pending | OpenTelemetry traces over agent runs for the eval/trace-review story. |

### Phase 8 — Web UI, eval report & submission  *(Days 15–17)*

| Spec | Feature | Location | Depends On | Status | Notes |
|------|---------|----------|------------|--------|-------|
| S8.1 | Web UI | `app/web/` | S3.4, S5.3 | pending | Simple demo UI (or `adk web`); voice in, results + checklist + draft out. |
| S8.2 | Demo personas seeded | `app/web/seed.py` | S8.1, S4.5 | pending | 3 canonical demo personas for the video. |
| S8.3 | Eval results report | `eval/REPORT.md` | S4.5, S7.4 | pending | Precision/recall on persona set; auditor before/after; coverage (schemes indexed, languages). **The 50-pt technical differentiator.** |
| S8.4 | README + architecture diagram | `README.md`, `docs/` | all | pending | Problem, solution, architecture image, setup, security, eval table. |
| S8.5 | Demo video | `docs/video-link.md` | S8.1, S8.2 | pending | ≤5 min on YouTube: problem stats → live voice demo → architecture → deploy proof → security. |

---

## Master Spec Index

| Spec | Feature | Location | Depends On | Status |
|------|---------|----------|------------|--------|
| S0.1 | Repo + project scaffold | whole tree (see Project structure) | — | done |
| S0.2 | Skills authored | `.agents/skills/*/SKILL.md` | S0.1 | done |
| S0.3 | Git Hooks | `githooks/` | S0.1 | done |
| S0.4 | Spec workflows | `.agents/workflows/*.md` | S0.1 | done |
| S0.5 | Antigravity build capture | `docs/antigravity/` | S0.1 | spec-written |
| S1.1 | Scheme corpus loader | `app/data/loader.py` | S0.1 | done |
| S1.2 | Corpus schema + models | `app/models/schemes.py` | S1.1 | done |
| S1.3 | Embeddings + vector index | `app/data/index.py` | S1.1, S1.2 | done |
| S2.1 | FastMCP server bootstrap | `app/mcp/scheme_search/server.py` | S0.2, S1.3 | done |
| S2.2 | `find_schemes` tool | `app/mcp/scheme_search/tools.py` | S2.1 | done |
| S2.3 | get_scheme tool | app/mcp/scheme_search/tools.py | S2.1 | done |
| S2.4 | MCP integration test | `tests/mcp/test_scheme_search.py` | S2.2, S2.3 | done |
| S3.1 | Agent contracts + state | `app/agents/contracts.py` | S0.2, S1.2 | done |
| S3.2 | IntakeAgent (text) | `app/agents/intake.py` | S3.1 | done |
| S3.3 | EligibilityMatcherAgent | `app/agents/matcher.py` | S2.2, S3.1 | done |
| S3.4 | Orchestrator | `app/agents/orchestrator.py` | S3.2, S3.3 | done |
| S4.1 | DocumentChecklistAgent | `app/agents/documents.py` | S2.3, S3.4 | done |
| S4.2 | FormFillerAgent | `app/agents/form_filler.py` | S3.2, S4.1 | done |
| S4.3 | RejectionRiskAuditorAgent | `app/agents/auditor.py` | S3.3 | done |
| S4.4 | ExplainerAgent | `app/agents/explainer.py` | S4.2, S4.3 | done |
| S4.5 | TDD eligibility test set | `eval/personas/`, `eval/scorer.py` | S3.3, S4.3 | done |
| S5.1 | Bhashini MCP tool | `app/mcp/bhashini/client.py` | S0.2, S3.2 | done |
| S5.2 | Intake voice + in-language | `app/agents/intake.py` | S5.1, S3.2 | done |
| S5.3 | Explainer TTS out | `app/agents/explainer.py` | S5.1, S4.4 | done |
| S6.1 | HITL confirmation gate | `app/agents/orchestrator.py` | S4.2 | pending |
| S6.2 | Input guardrails | `app/agents/guards.py` | S3.2 | pending |
| S6.3 | PII minimization + TTL | `app/db/session.py` | S0.1 | pending |
| S6.4 | Disclaimer injection | `app/agents/explainer.py` | S4.4 | pending |
| S7.1 | Containerize | `deploy/Dockerfile` | S3.4 | pending |
| S7.2 | Cloud Run deploy script | `deploy/deploy.sh` | S7.1, S6.3 | pending |
| S7.3 | Firestore session store | `app/db/session.py` | S6.3 | pending |
| S7.4 | Tracing / observability | `app/core/telemetry.py` | S3.4 | pending |
| S8.1 | Web UI | `app/web/` | S3.4, S5.3 | pending |
| S8.2 | Demo personas seeded | `app/web/seed.py` | S8.1, S4.5 | pending |
| S8.3 | Eval results report | `eval/REPORT.md` | S4.5, S7.4 | pending |
| S8.4 | README + architecture | `README.md`, `docs/` | all | pending |
| S8.5 | Demo video | `docs/video-link.md` | S8.1, S8.2 | pending |

---

## Critical path & MVP

**Ship-something-every-day rule (mirrors the 17-day plan):** get the **English text path** working end-to-end first (S0 → S1 → S2 → S3 → S4), so there is always a demoable system. Voice/multilingual (Phase 5), security hardening (Phase 6), and deploy (Phase 7) are additive — each makes the submission stronger but none blocks a working demo.

**Minimum viable submission** (if time runs short): S0.1, S1.1–S1.3, S2.1–S2.4, S3.1–S3.4, S4.1, S4.3, S4.5, S8.4. That alone demonstrates 3 course concepts (multi-agent ADK + MCP server + the eval rigor) with honest numbers.

**Stretch for full 6-concept claim:** add Phase 5 (multilingual), Phase 6 (security/HITL), Phase 7 (deploy on Cloud Run), plus S0.2 (agent skills) and S0.5 (Antigravity build capture). That covers all six course concepts: multi-agent ADK (code), MCP server (code), security (code/video), deployability (video), agent skills (code/video), and Antigravity (video).

---

## Project rules (carry over from SehatSamjho conventions)

- **NEVER commit to main directly** — feature branches → PR → main.
- **NEVER hardcode API keys** — all secrets via `.env` → config; Secret Manager in prod. (`secret-scan` hook enforces.)
- **NEVER persist identifiable citizen data (PII)** — session-scoped only, metadata logs (timestamp, language, scheme_count, latency). (`no-pii-guard` hook enforces.)
- **NEVER add an AI tool as commit co-author.**
- **A file is never done until its tests pass** — TDD, Red → Green → Refactor.
- **Async where it matters; Pydantic for all data in/out; Tenacity retries on every external API (Gemini, Bhashini); structured logging with request_id.**
- **Ruff** for lint + format (line length 100).
