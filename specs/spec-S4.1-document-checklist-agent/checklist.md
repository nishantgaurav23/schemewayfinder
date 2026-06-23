# Checklist S4.1: DocumentChecklistAgent

Implementation progress tracker for spec S4.1.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Use `adk-agent-scaffold` skill to scaffold `app/agents/documents.py` and `tests/agents/test_documents.py`.
  - [x] Ensure the MCP `get_scheme` tool client is accessible to the agent.

- [x] **Phase 2: Tests First (TDD)**
  - [x] Implement `test_document_checklist_success` verifying deduplication of required documents.
  - [x] Implement `test_document_checklist_empty_matches`.
  - [x] Implement `test_document_checklist_handles_tool_failure`.
  - [x] Run `make test` and verify that the new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Implement `DocumentChecklistAgent` in `app/agents/documents.py`.
  - [x] Wire it to read from `SessionState.matches` and write to `SessionState.checklist`.
  - [x] Integrate the `get_scheme` MCP tool (or database lookup) to fetch required docs.
  - [x] Run `make test` and verify all tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Update `app/agents/orchestrator.py` to register `DocumentChecklistAgent` as a sub-agent.
  - [x] Update the Orchestrator's `instruction` to route to `DocumentChecklistAgent` after `EligibilityMatcherAgent` completes.

- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Run `make test` to ensure no regressions.
  - [x] Ensure no PII is logged during document fetching.
  - [x] Update `roadmap.md` status of `S4.1` to `done`.
