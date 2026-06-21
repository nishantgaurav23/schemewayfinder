# Spec S1.1 — Scheme corpus loader

## Overview
Load the myScheme corpus (e.g., HF `shrijayan/gov_myscheme` or Kaggle Indian Government Schemes dataset) into a normalized format. The loader must parse the raw dataset and extract the core details needed for the navigator: `id`, `name`, `level` (central/state), `eligibility_rules`, `required_documents`, and `apply_url`. The raw data must be bundled for reproducibility so it can run offline or on Cloud Run without downloading massive files at runtime.

## Dependencies
- **S0.1** (Repo scaffold)

## Target Location
- `app/data/loader.py`

---

## Functional Requirements

### FR-1: Load Dataset
- **What**: Safely read the raw corpus data (JSON or CSV, bundled locally).
- **Inputs**: Path to the raw dataset file.
- **Outputs**: Raw list of dictionaries representing the schemes.
- **Edge cases**: Missing file, invalid format.

### FR-2: Normalize Schema
- **What**: Transform the raw dataset schema into our uniform dictionary format.
- **Inputs**: Raw scheme dictionary.
- **Outputs**: Normalized dictionary containing `id`, `name`, `level`, `eligibility_rules`, `required_documents`, and `apply_url`.
- **Edge cases**: Missing fields (default to empty string or empty list). Parsing messy text into lists for rules/documents.

### FR-3: Bundle for Reproducibility
- **What**: Ensure the loader can be run purely locally using a static dump of the dataset.
- **Inputs**: None.
- **Outputs**: A reproducible loading mechanism.
- **Edge cases**: N/A

---

## Tangible Outcomes

- [ ] **Outcome 1**: `app/data/loader.py` exists with a functional `load_schemes()` method.
- [ ] **Outcome 2**: A small sample (or full dump) of the dataset is committed to the repository (e.g., `data/raw/` or `app/data/corpus/`) for reproducibility.
- [ ] **Outcome 3**: Normalized output clearly maps to the required fields.

---

## Test-Driven Requirements

### Tests to Write First (Red → Green)
1. **test_loader_file_not_found**: Assert that attempting to load a non-existent dataset raises a `FileNotFoundError`.
2. **test_normalize_schema_valid**: Assert that a mock raw scheme dictionary is correctly transformed into the normalized dictionary.
3. **test_normalize_schema_missing_fields**: Assert that missing fields in the raw data safely default to empty lists or strings without crashing.
4. **test_load_schemes**: Assert that the main loader successfully loads and normalizes the sample/bundled dataset.

### Mocking Strategy
- Mock the file reading operation for the normalization tests to avoid dependency on the real dataset file.

### Coverage Expectation
- 100% line coverage for `app/data/loader.py`.

---

## References
- roadmap.md, AGENTS.md
