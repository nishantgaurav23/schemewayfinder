# Checklist — S3.1: Agent contracts + shared state

This checklist tracks the implementation of S3.1.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Ensure app models and dependencies are correctly loaded.
- [x] **Phase 2: Tests First (TDD)**
  - [x] Create test file at `tests/agents/test_contracts.py`.
  - [x] Write `test_session_state_defaults` checking empty/clean defaults.
  - [x] Write `test_session_state_validation` verifying nested validation constraints.
  - [x] Run `uv run pytest tests/agents/test_contracts.py` and confirm tests fail (Red).
- [x] **Phase 3: Implementation**
  - [x] Implement the `SessionState` Pydantic model in [app/agents/contracts.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/agents/contracts.py).
  - [x] Define constant output keys for agent state handoffs.
- [x] **Phase 4: Integration**
  - [x] Run `uv run pytest tests/agents/test_contracts.py` and confirm all tests pass (Green).
  - [x] Run the complete project test suite (`make test`).
- [x] **Phase 5: Verification**
  - [x] Run `make lint` and fix formatting/warnings.
  - [x] Update `roadmap.md` status to `done` for S3.1.
