# Checklist S3.2: IntakeAgent (text)

Implementation progress tracker for spec S3.2.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Verify `google-adk` package is importable and works in the local Python environment.

- [x] **Phase 2: Tests First (TDD)**
  - [x] Create `tests/agents/test_intake.py` with mock setups for Gemini API.
  - [x] Implement `test_intake_success` asserting correct parsing of a fully qualified user text.
  - [x] Implement `test_intake_invalid_values` asserting that bad inputs fail validation.
  - [x] Implement `test_intake_missing_fields_defaults` asserting imputation logic.
  - [x] Implement `test_intake_retries_on_failure` asserting `tenacity` retry behavior.
  - [x] Implement `test_intake_logging_no_pii` asserting logs do not contain raw profile strings.
  - [x] Run `make test` to ensure all new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Create `app/agents/intake.py`.
  - [x] Initialize `IntakeAgent` using `LlmAgent` and configuring the `output_schema` as `CitizenProfile`.
  - [x] Implement `output_key` integration to save output in `SessionState` under `citizen_profile`.
  - [x] Set up prompts instructing Gemini to extract age, income, state, category, disability, and occupation.
  - [x] Apply `tenacity` retries (3 attempts, exponential backoff) to Gemini API calls.
  - [x] Add loguru logger inside callbacks or wrappers to log metadata without PII.
  - [x] Run `make test` to ensure all tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Register `IntakeAgent` in the orchestrator file `app/agents/orchestrator.py`.
  - [x] Wire the intake agent output key to the orchestrator execution path.

- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Run the complete test suite: `make test`.
  - [x] Verify no secrets are checked in or PII persisted.
  - [x] Update `roadmap.md` status of `S3.2` to `done`.
