# Checklist S3.4: Orchestrator (delegation)

Implementation progress tracker for spec S3.4.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Run the `adk-agent-scaffold` skill to scaffold the `tests/agents/test_orchestrator.py` and prepare the structure.
  - [x] Verify `IntakeAgent` and `EligibilityMatcherAgent` are importable.

- [x] **Phase 2: Tests First (TDD)**
  - [x] Implement `test_orchestrator_delegates_to_intake_when_profile_empty`.
  - [x] Implement `test_orchestrator_delegates_to_matcher_when_profile_ready`.
  - [x] Implement `test_orchestrator_handles_subagent_errors`.
  - [x] Run `make test` to ensure new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Refactor `app/agents/orchestrator.py` to change `SchemeWayfinderOrchestrator` from `SequentialAgent` to an `LlmAgent` delegator.
  - [x] Provide explicit delegation instructions and register the sub-agents as tools or downstream nodes.
  - [x] Run `make test` to ensure all tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Verify that `main.py` or the entry point correctly invokes the new Orchestrator root.
  - [x] Ensure state passing across delegations is intact.

- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Run the complete test suite: `make test`.
  - [x] Update `roadmap.md` status of `S3.4` to `done`.
