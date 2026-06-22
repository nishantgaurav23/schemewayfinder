# Checklist — S2.4: MCP integration test

This checklist tracks the implementation of S2.4.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Ensure the test suite environment has the required mock contexts loaded.
- [/] **Phase 2: Tests First (TDD)**
  - [/] Create test file at `tests/mcp/test_scheme_search.py`.
  - [ ] Write `test_mcp_client_find_schemes` calling `find_schemes` through the client context.
  - [ ] Write `test_mcp_client_get_scheme` calling `get_scheme` through the client context.
  - [ ] Run `uv run pytest tests/mcp/test_scheme_search.py` and confirm tests fail (Red).
- [x] **Phase 3: Implementation**
  - [x] Implement/wire the client execution context using FastMCP list/call tool utilities.
  - [x] Fix any import errors or tool resolution failures.
- [x] **Phase 4: Integration**
  - [x] Run `uv run pytest tests/mcp/test_scheme_search.py` and confirm tests pass (Green).
  - [x] Run the complete project test suite (`make test`).
- [x] **Phase 5: Verification**
  - [x] Run `make lint` and fix any formatting/lint issues.
  - [x] Update `roadmap.md` status to `done` for S2.4.
