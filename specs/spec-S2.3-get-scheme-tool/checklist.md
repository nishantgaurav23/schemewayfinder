# Checklist — S2.3: get_scheme(id) tool

This checklist tracks the implementation of S2.3.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Ensure FastMCP and app models are correctly loaded.
- [x] **Phase 2: Tests First (TDD)**
  - [x] Create test file at `tests/mcp/test_get_scheme.py`.
  - [x] Write `test_get_scheme_success` verifying positive lookup.
  - [x] Write `test_get_scheme_not_found` verifying error response.
  - [x] Run `uv run pytest tests/mcp/test_get_scheme.py` and confirm tests fail (Red).
- [x] **Phase 3: Implementation**
  - [x] Register the `get_scheme` tool on the custom server at [app/mcp/scheme_search/tools.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/tools.py).
  - [x] Implement lookup using `load_schemes` and matching by ID.
  - [x] Handle missing scheme ID edge cases.
- [x] **Phase 4: Integration**
  - [x] Confirm the tool registers properly when the server starts.
  - [x] Run `uv run pytest tests/mcp/test_get_scheme.py` and confirm tests pass (Green).
  - [x] Run the full test suite (`make test`).
- [x] **Phase 5: Verification**
  - [x] Run `make lint` and fix any linting issues.
  - [x] Update `roadmap.md` status to `done` for S2.3.
