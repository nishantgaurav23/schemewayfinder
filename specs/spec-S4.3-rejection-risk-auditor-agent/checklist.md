# Checklist S4.3: RejectionRiskAuditorAgent

Implementation progress tracker for spec S4.3.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Use `adk-agent-scaffold` skill to scaffold `app/agents/auditor.py` and `tests/agents/test_auditor.py`.
  - [x] Check `app/agents/contracts.py` for any needed state keys (e.g., `REJECTED_MATCHES_KEY`).

- [x] **Phase 2: Tests First (TDD)**
  - [x] Implement `test_auditor_pass`.
  - [x] Implement `test_auditor_reject_hallucination`.
  - [x] Implement `test_auditor_max_iterations`.
  - [x] Run `make test` and verify that the new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Implement `RejectionRiskAuditorAgent` in `app/agents/auditor.py` as a `LoopAgent`.
  - [x] Implement the critic prompt to evaluate matches against the citizen profile.
  - [x] Format the output structure to safely update `SessionState.matches` and `SessionState.rejected_matches`.
  - [x] Run `make test` and verify all tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Update `app/agents/orchestrator.py` to register the Auditor agent.
  - [x] Update the Orchestrator's `instruction` to invoke the Auditor after the Matcher.

- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Run `make test` to ensure no regressions.
  - [x] Update `roadmap.md` status of `S4.3` to `done`.
