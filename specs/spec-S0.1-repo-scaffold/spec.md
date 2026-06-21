# Spec S0.1 — Repo + project scaffold

## Overview
Create the entire folder tree from the Project structure section: all dirs + `__init__.py` stubs, `pyproject.toml` (uv, no requirements.txt), `Makefile`, `.gitignore`, `.env.example`, empty placeholder modules. Python 3.11; ruff line length 100; pytest configured. After this, `make test` runs (even if 0 tests) and every later spec has its target file ready.

## Dependencies
None

## Target Location
Whole tree (see **Project structure** in roadmap.md)

---

## Functional Requirements

### FR-1: Directory Structure
- **What**: Create the full directory structure described in the roadmap.
- **Inputs**: None
- **Outputs**: Directories for `app/`, `eval/`, `tests/`, `deploy/`, `docs/`, and their subdirectories.
- **Edge cases**: None

### FR-2: Boilerplate Files
- **What**: Create necessary boilerplate files: `__init__.py` stubs, empty placeholder modules, `.env.example`, `.gitignore`.
- **Inputs**: None
- **Outputs**: File placeholders.
- **Edge cases**: Ensure `.gitignore` ignores `.env`, `.venv`, `__pycache__`.

### FR-3: Project Configuration (`pyproject.toml`)
- **What**: Initialize `pyproject.toml` for Python 3.11 using `uv`. Configure `ruff` (line length 100) and `pytest`.
- **Inputs**: None
- **Outputs**: `pyproject.toml` with dependencies and tool configurations.
- **Edge cases**: No `requirements.txt` should be used.

### FR-4: Makefile
- **What**: Create a `Makefile` with commands for `test`, `lint`, `eval`, `mcp`, `run`, and `deploy`.
- **Inputs**: None
- **Outputs**: A functional `Makefile`.
- **Edge cases**: Ensure `make test` and `make lint` execute without errors even on an empty project.

---

## Tangible Outcomes

- [ ] **Outcome 1**: The directory tree exactly matches the `Project structure` layout in roadmap.md.
- [ ] **Outcome 2**: `make test` executes successfully (0 tests collected).
- [ ] **Outcome 3**: `make lint` executes successfully with ruff configured to line-length=100.
- [ ] **Outcome 4**: `pyproject.toml` exists and manages dependencies (no `requirements.txt`).

---

## Test-Driven Requirements

### Tests to Write First (Red → Green)
1. **test_scaffold_sanity**: A dummy test in `tests/test_sanity.py` ensuring `pytest` resolves the `app` module and runs correctly.

### Mocking Strategy
- N/A for scaffolding.

### Coverage Expectation
- Infrastructure setup, no functional code yet. `make test` must run without environment errors.

---

## References
- roadmap.md, AGENTS.md
