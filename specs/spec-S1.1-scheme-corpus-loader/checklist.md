# Checklist — Spec S1.1: Scheme corpus loader

## Phase 1: Setup & Dependencies
- [x] Determine the dataset format (JSON/CSV) to bundle.
- [x] Create a dummy/sample dataset file in `app/data/corpus/sample.json` (or similar) to use for testing.

## Phase 2: Tests First (TDD)
- [x] Create `tests/data/test_loader.py`.
- [x] Write `test_loader_file_not_found`.
- [x] Write `test_normalize_schema_valid`.
- [x] Write `test_normalize_schema_missing_fields`.
- [x] Write `test_load_schemes` using the sample dataset.
- [x] Run `make test` — verify all tests fail (Red).

## Phase 3: Implementation
- [x] Implement `normalize_scheme(raw_data: dict) -> dict` in `app/data/loader.py` to extract and format the required fields.
- [x] Implement `load_schemes(filepath: str) -> list[dict]` in `app/data/loader.py` to open the file and apply the normalizer.
- [x] Re-run `make test` until all tests pass (Green).

## Phase 4: Integration
- [x] Add the actual real dataset bundle to `app/data/corpus/` if not already done.
- [x] Add code to load the default bundled dataset if no path is provided.
- [x] Ensure the bundled dataset file is tracked by git if it's small, or use `git-lfs`/scripting if it is large.

## Phase 5: Verification
- [x] Run `make lint` and fix any issues.
- [x] Confirm the output dictionaries strictly have `id`, `name`, `level`, `eligibility_rules`, `required_documents`, and `apply_url`.
- [x] Ensure no PII or secrets are logged.
- [x] Update roadmap.md status: pending → done (when ready)
