# Checklist S5.3: ExplainerAgent TTS out

Implementation progress tracker for spec S5.3.

- [ ] **Phase 1: Setup & Dependencies**
  - [ ] Verify S5.1 (Bhashini client) is ready and supports TTS.
  - [ ] Review `app/agents/explainer.py` for injection points after the LLM generates the summary.

- [ ] **Phase 2: Tests First (TDD)**
  - [ ] Add `test_explainer_extracts_language` to `tests/agents/test_explainer.py`.
  - [ ] Add `test_explainer_skips_translation_for_en`.
  - [ ] Add `test_explainer_nmt_and_tts` mocking `BhashiniClient.nmt` and `BhashiniClient.tts`.
  - [ ] Run `make test` and verify new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Update `app/agents/explainer.py` to extract `source_language` from `ctx.state.citizen_profile`.
  - [x] Inject `BhashiniClient` and invoke `nmt` to translate the summary if language is not `en`.
  - [x] Invoke `tts` on the translated summary.
  - [x] Update the return object of ExplainerAgent to include the translated text and audio data.
  - [x] Run `make test` and verify tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Ensure the ExplainerAgent output schema reflects the new fields (e.g. `translated_text`, `audio_base64`).
  
- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Update `roadmap.md` status of `S5.3` to `done`.
