# Checklist — Spec S0.1: Repo + project scaffold

## Phase 1: Setup & Dependencies
- [x] Verify dependencies (none)
- [x] Initialize `pyproject.toml` with `uv init` (or manual creation) for Python 3.11
- [x] Add `ruff` and `pytest` dependencies to `pyproject.toml`

## Phase 2: Tests First (TDD)
- [x] Create `tests/` directory and `tests/__init__.py`
- [x] Write `tests/test_sanity.py` with a basic test asserting True
- [x] Run `pytest` — expect pass (Green)

## Phase 3: Implementation
- [x] Create all directories listed in the Project structure
- [x] Create all `__init__.py` stubs and placeholder module files in `app/`, `eval/`, etc.
- [x] Create `.env.example`
- [x] Create `.gitignore` (ignore `.env`, `.venv`, `__pycache__`)
- [x] Create `Makefile` with `test`, `lint`, `eval`, `mcp`, `run`, `deploy` targets
- [x] Configure `ruff` in `pyproject.toml` (line-length = 100)

## Phase 4: Integration
- [x] Run `make lint` and fix any issues
- [x] Run full test suite: `make test`

## Phase 5: Verification
- [x] All tangible outcomes checked
- [x] No hardcoded secrets
- [x] No PII persisted beyond session scope
- [x] Update roadmap.md status: pending → done (when ready)
