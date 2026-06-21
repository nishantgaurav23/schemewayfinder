---
name: project-context
description: Persistent architecture and codebase context for SchemeWayfinder. Always active.
---

# SchemeWayfinder — Project Context

> Always-active rule. Antigravity reads this every conversation in this workspace. Re-run the repo-research skill to update it as the project grows.

## What this is
A multi-agent welfare-entitlement navigator. Citizen profile (voice/text, 22 Indian languages) → eligible government schemes + document checklist + pre-filled application draft + rejection-risk explanation. Built on Google ADK for the Kaggle × Google Vibe Coding Capstone (Agents for Good).

## Technology stack
- **Language:** Python 3.11
- **Agents:** Google Agent Development Kit (ADK) — Sequential / Parallel / Loop + LLM-driven delegation
- **Models:** Gemini (Flash for routing/extraction, Pro for eligibility reasoning) — confirm current model IDs at build time
- **Custom MCP:** `scheme-search` (FastMCP) — `find_schemes(profile)`, `get_scheme(id)`
- **Consumed MCP:** Bhashini — ASR / NMT / TTS for 22 Indian languages
- **Data:** myScheme corpus (HF `shrijayan/gov_myscheme` / Kaggle Indian Government Schemes), data.gov.in
- **Deploy:** Cloud Run (container) + Firestore (session state, TTL)
- **Build tooling:** Antigravity (native), uv, ruff, pytest

## Project structure (target)
```
app/
  core/        config.py, telemetry.py
  agents/      orchestrator, intake, matcher, documents, form_filler, auditor, explainer, guards, contracts
  mcp/
    scheme_search/   server.py, tools.py          # custom FastMCP
    bhashini/        client.py                     # consumed MCP
  data/        loader.py, index.py
  models/      schemes.py
  db/          session.py
  web/         demo UI + seeded personas
eval/          personas/, scorer.py, REPORT.md
tests/         mirrors app/
deploy/        Dockerfile, deploy.sh
docs/          architecture.png, cover image, video link, antigravity/
```

## Agent pipeline
```
citizen (voice/text) → Intake&Translation (Bhashini) → Orchestrator (delegation)
→ EligibilityMatcher (ParallelAgent: central ∥ state → scheme-search MCP)
→ RejectionRiskAuditor (LoopAgent: critic re-checks rules until pass)
→ DocumentChecklist + FormFiller (get_scheme MCP)
→ Explainer (plain-language + TTS + disclaimer)
→ HITL confirm → result to citizen ; metadata-only logging (zero PII)
```

## Data model (Pydantic, app/models/schemes.py)
- `Scheme` — id, name, level (central/state), eligibility_rules, required_documents, apply_url
- `EligibilityRule` — field, operator, value
- `CitizenProfile` — age, income, occupation, state, gender, category, land_holding, disability, …
- `MatchResult` — scheme_id, score, matched_rules, weak_rules, rejection_risk

## Constraints
- PII minimization: session-scoped only, Firestore TTL, metadata-only logs.
- No secrets in code; `.env` → config; Secret Manager in prod.
- Structured-state handoffs between agents (output_key), not free-form text.
- TDD; ruff line length 100.

## Status
See `roadmap.md` Master Spec Index for per-spec status (pending / spec-written / done).
