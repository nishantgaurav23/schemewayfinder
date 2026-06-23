# Checklist S4.5: TDD Eligibility Test Set

Implementation progress tracker for spec S4.5.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Create `eval/personas/` directory.
  - [x] Create JSON files for 4 personas (farmer, widow-pension, student, pwd).
  - [x] Create `eval/scorer.py` and `tests/eval/test_scorer.py`.

- [x] **Phase 2: Tests First (TDD)**
  - [x] Implement `test_eval_scorer_precision_recall` in `tests/eval/test_scorer.py`.
  - [x] Implement `test_eval_harness_integration` using a dummy persona.
  - [x] Run `make test` and verify that the new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Implement logic in `eval/scorer.py` to run the Matcher and Auditor against each persona.
  - [x] Implement the precision/recall math.
  - [x] Implement `REPORT.md` markdown generation from the metrics.
  - [x] Run `make test` and verify tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Add `eval` target to `Makefile` that runs `python -m eval.scorer`.

- [x] **Phase 5: Verification**
  - [x] Run `make eval` to generate `eval/REPORT.md`.
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Update `roadmap.md` status of `S4.5` to `done`.
