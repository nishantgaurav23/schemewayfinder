# Checklist — S2.2: find_schemes(profile) tool

This checklist tracks the implementation of S2.2.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Ensure FastMCP and dependencies are correctly loaded.
- [x] **Phase 2: Tests First (TDD)**
  - [x] Create test file at `tests/mcp/test_find_schemes.py`.
  - [x] Write `test_find_schemes_fully_eligible` verifying positive match flow.
  - [x] Write `test_find_schemes_ineligible_rule` verifying rule failures.
  - [x] Run `.venv/bin/pytest tests/mcp/test_find_schemes.py` and confirm tests fail (Red).
- [x] **Phase 3: Implementation**
  - [x] Register the `find_schemes` tool on the custom server at [app/mcp/scheme_search/tools.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/tools.py) (importing `mcp` from `server.py`).
  - [x] Implement the profile parsing and semantic retrieval logic.
  - [x] Implement rule comparison evaluation checks (`>=`, `<=`, `==`, `in`, `contains`).
  - [x] Implement score calculations and `MatchResult` construction.
- [x] **Phase 4: Integration**
  - [x] Import `tools.py` in `server.py` so the tool registers when the server starts.
  - [x] Run `.venv/bin/pytest tests/mcp/test_find_schemes.py` and confirm all tests pass (Green).
  - [x] Run the complete test suite.
- [x] **Phase 5: Verification**
  - [x] Run `ruff check` and `ruff format` on the new files.
  - [x] Update `roadmap.md` status to `done` for S2.2.
