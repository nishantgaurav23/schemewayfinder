---
name: verify-spec
description: Audit that a SchemeWayfinder spec is fully and correctly implemented — tests, lint, outcomes, wiring.
---

# /verify-spec — Post-implementation audit

Input: a spec id (e.g., `S4.3`).

## Step 1: Load Spec Context

1. Find spec folder: `specs/spec-{id}*/`
2. Read `spec.md` — extract Tangible Outcomes and Functional Requirements
3. Read `checklist.md` — note any unchecked items
4. Read `roadmap.md` row for this spec — get Location, Feature, Notes

## Step 2: Code Existence

- Check every file listed in the spec's **Target Location** exists
- Check each file is non-empty and has the expected public functions / agent classes mentioned in FRs
- Report: files found, missing files, missing functions

## Step 3: Test Suite

1. Find test files: glob `tests/**/test_*.py` matching the module
2. Run tests: `python -m pytest {test_files} -v --tb=short`
3. Report: total tests, passed, failed, errors
4. If any failures: show the first 3 failure summaries

## Step 4: Lint

Run: `python -m ruff check app/ --select E,F,W`
Report: clean or list issues in spec's files only

## Step 5: Tangible Outcomes Audit

For each Tangible Outcome listed in spec.md:
- Check if there is a corresponding test that verifies it
- Check if the implementation satisfies it (read the relevant code)
- Mark: PASS / FAIL / UNCLEAR

## Step 6: Integration Check

- If spec adds a sub-agent: verify it is registered under the orchestrator (`app/agents/orchestrator.py`) and reachable
- If spec adds an MCP tool: verify it is registered on the scheme-search server and listed by the server
- If spec adds a consumed MCP tool (Bhashini): verify it is wired via McpToolset
- If spec adds config fields: verify they exist in `app/core/config.py`
- If spec touches session/PII: verify no identifying data is persisted beyond session TTL
- If spec is security-related: verify the callback/guardrail/HITL gate is actually invoked in the run path

## Step 7: Report + Verdict

```
Verification Report — Spec {spec_id}: {feature}
────────────────────────────────────────────────
Code files:      ✓ All present
Tests:           ✓ 8/8 passing
Lint:            ✓ Clean
Outcomes:        ✓ 3/3 verified
Integration:     ✓ Sub-agent wired into orchestrator
Checklist:       ⚠ 1 unchecked item (Phase 4 — lint)

VERDICT: PASS (with 1 minor item)
```

If PASS: suggest updating `roadmap.md` status from `pending`/`spec-written` → `done`.
If FAIL: list exactly what needs to be fixed, in priority order.
