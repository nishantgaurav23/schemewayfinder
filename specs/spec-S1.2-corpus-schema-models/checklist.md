# Checklist — S1.2: Corpus schema + models

This checklist tracks the implementation of S1.2.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Verify `pydantic` package is active in python environment.
- [x] **Phase 2: Tests First (TDD)**
  - [x] Create test file at `tests/models/test_schemes.py`.
  - [x] Write `test_eligibility_rule_validation` to check invalid operators.
  - [x] Write `test_scheme_state_validation` to verify state presence condition on state-level schemes.
  - [x] Write `test_citizen_profile_bounds` to verify age > 0 and income >= 0 constraints.
  - [x] Write `test_match_result_score_bounds` to verify overall_score range is between 0.0 and 1.0.
  - [x] Run `make test` and confirm tests fail (Red).
- [x] **Phase 3: Implementation**
  - [x] Implement `EligibilityRule` in [app/models/schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/models/schemes.py).
  - [x] Implement `Scheme` in [app/models/schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/models/schemes.py) with custom validator for `state`/`level`.
  - [x] Implement `CitizenProfile` in [app/models/schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/models/schemes.py) with field bounds validations.
  - [x] Implement `MatchResult` in [app/models/schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/models/schemes.py) with score range validation.
- [x] **Phase 4: Integration**
  - [x] Run `make test` to ensure all model tests pass (Green).
- [x] **Phase 5: Verification**
  - [x] Run `make lint` using Ruff check and format.
  - [x] Confirm no secrets or citizen PII are committed in codes or tests.
  - [x] Sync status of S1.2 to `done` in `roadmap.md`.
