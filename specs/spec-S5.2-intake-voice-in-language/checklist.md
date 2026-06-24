# Checklist S5.2: Intake voice + in-language

Implementation progress tracker for spec S5.2.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Verify that S5.1 (Bhashini MCP client) is complete and accessible.
  - [x] Review `app/agents/intake.py` to identify injection points for ASR and NMT.

- [x] **Phase 2: Tests First (TDD)**
  - [x] Add `test_intake_asr_transcription` to `tests/agents/test_intake.py` mocking `BhashiniClient.asr`.
  - [x] Add `test_intake_nmt_translation` to `tests/agents/test_intake.py` mocking `BhashiniClient.nmt`.
  - [x] Add `test_intake_multilingual_coverage` parameterized for Hindi, Marathi, and Tamil.
  - [x] Run `make test` and verify that the new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Update `IntakeAgent` to accept `audio_data` and `source_language` parameters.
  - [x] Inject `BhashiniClient` into `IntakeAgent` (or instantiate it from config).
  - [x] Implement ASR processing step if `audio_data` is provided.
  - [x] Implement NMT processing step if `source_language` is not `en`.
  - [x] Ensure `source_language` is saved into the output state (`CitizenProfile` or session state).
  - [x] Run `make test` and verify all tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Verify that `app/agents/orchestrator.py` correctly passes language/audio context to `IntakeAgent`.
  - [x] Ensure the updated state matches the `output_key` contract for downstream agents.

- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Update `roadmap.md` status of `S5.2` to `done`.
