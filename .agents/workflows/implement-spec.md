---
name: implement-spec
description: Implement a SchemeWayfinder spec following strict TDD. Use after the spec exists and its dependencies are done.
---

# /implement-spec — TDD implementation

Input: a spec id (e.g., `S1.1`).

## Step 1: Load Spec Context

1. Find the spec folder: search for `specs/spec-{id}*/` or look up in `roadmap.md` Master Spec Index
2. Read `specs/spec-{id}-{slug}/spec.md` — requirements, outcomes, TDD notes
3. Read `specs/spec-{id}-{slug}/checklist.md` — phases to follow
4. Read `roadmap.md` phase table row for this spec
5. Read `AGENTS.md` and `.agents/rules/project-context.md` for project rules (no PII, structured-state handoffs, etc.)

## Step 2: Verify Prerequisites

- Dependencies (Depends On) are implemented (use /check-spec-deps if unsure)
- Target files/locations exist or can be created

## Step 3: Follow TDD Strictly

**Red → Green → Refactor**

1. **Red**: Write failing tests first in `tests/` (mirror app structure). Mock all external services (Gemini, Bhashini, Firestore, the MCP server). For agents, assert on structured outputs written to shared state. Run `make test` — expect failures.
2. **Green**: Implement minimal code to pass tests. No extra features beyond spec.
3. **Refactor**: Clean up; re-run tests after each change.

**Checklist updates**: After completing each phase (Setup, Tests, Implementation, Integration), immediately update `checklist.md` — change `- [ ]` to `- [x]` for every item completed in that phase. Do not wait until the end.

## Step 4: Implementation Rules

| Rule | Action |
|------|--------|
| Agents | ADK agents; compose with Sequential / Parallel / Loop; LLM-driven delegation in the orchestrator |
| State | Agents hand off via structured outputs (output_key → session.state), never free-form text relay |
| Config | All secrets from config.py, never hardcode; Secret Manager in prod |
| Retries | Tenacity (3 attempts, exponential backoff) on external APIs (Gemini, Bhashini) |
| Logging | Loguru with request_id where applicable; never log PII |
| Models | Pydantic for all in/out; use app/models/schemes.py |
| PII | Never log/store raw profile, audio, or identifying data; session-scoped only (Firestore TTL) |
| MCP | New tools registered on the scheme-search server with a schema + handler + test |
| Lint | Ruff, line length 100; run `make lint` before done |

## Step 5: Verification

- [ ] All tests pass: `make test`
- [ ] Lint passes: `make lint`
- [ ] All Tangible Outcomes from spec.md are met
- [ ] If eligibility-related: persona eval still passes (`make eval`)

## Step 6: Update Checklist & Roadmap

After all tests pass and verification is complete:

### 6a. Finalize checklist.md
1. Mark all remaining Phase 5 (Verification) items as `- [x]` in `checklist.md`
2. Confirm every item across all phases is `- [x]` — no unchecked items should remain
3. If any item was skipped (not applicable), change it to `- [x] N/A — {reason}`

### 6b. Update roadmap.md
1. Find the spec row in **both** the Phase table and the Master Spec Index table
2. Change the Status column from `spec-written` (or `pending`) to `done` for this spec in **both** tables
3. Verify the edit — ensure no other rows were accidentally modified

Work through checklist.md phases in order. Do not skip "Tests First". Update checklist.md progressively as each phase completes — not all at once at the end. When done, report completion and confirm both checklist.md and roadmap.md were updated.
