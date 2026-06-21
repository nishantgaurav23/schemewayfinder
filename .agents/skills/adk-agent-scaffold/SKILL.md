---
name: adk-agent-scaffold
description: Scaffold a new ADK sub-agent for SchemeWayfinder plus its pytest, wired to the orchestrator. Use when adding any agent (intake, matcher, documents, form_filler, auditor, explainer, guards).
---

# Skill: adk-agent-scaffold

When asked to create an ADK agent, do ALL of the following:

1. Create `app/agents/{name}.py` defining the agent. Pick the right ADK primitive:
   - simple step → `LlmAgent`
   - concurrent fan-out → `ParallelAgent` (write each branch to a UNIQUE state key)
   - iterative critic/refine → `LoopAgent` with `max_iterations` and early exit
2. Inputs/outputs are Pydantic models from `app/models/schemes.py`. Read from and write to shared state via `output_key` — never free-form text relay.
3. Create `tests/agents/test_{name}.py` FIRST (TDD): mock Gemini and any MCP calls; assert on the structured state the agent writes, plus edge cases (empty match, timeout, invalid profile).
4. Register the agent under the orchestrator in `app/agents/orchestrator.py` (sub_agents / delegation).
5. Apply project rules: Tenacity retries on external calls, Loguru with request_id, no PII in logs, ruff line length 100.
6. Run `make test` and `make lint`; do not finish until green.

Output: the agent file, its test file, and the orchestrator wiring — all passing.
