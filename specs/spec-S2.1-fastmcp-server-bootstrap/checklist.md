# Checklist — S2.1: FastMCP server bootstrap

This checklist tracks the implementation of S2.1.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Add `mcp` (or `mcp[cli]`) and `fastmcp` to project dependencies in `pyproject.toml`.
  - [x] Sync the virtual environment.
- [x] **Phase 2: Tests First (TDD)**
  - [x] Create test file at `tests/mcp/test_server_sanity.py`.
  - [x] Write `test_mcp_instance_creation` to verify FastMCP instantiation and configuration.
  - [x] Write `test_status_tool_registration` to verify the health check tool works.
  - [x] Run `.venv/bin/pytest tests/mcp/test_server_sanity.py` and verify it fails (Red).
- [x] **Phase 3: Implementation**
  - [x] Bootstrap the FastMCP server at [app/mcp/scheme_search/server.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/server.py).
  - [x] Implement the `status` health check tool returning a summary of the corpus database status.
  - [x] Add main entrypoint calling `mcp.run()`.
- [x] **Phase 4: Integration**
  - [x] Run `.venv/bin/pytest tests/mcp/test_server_sanity.py` and verify it passes (Green).
  - [x] Run the complete test suite.
- [x] **Phase 5: Verification**
  - [x] Run `ruff check` and `ruff format` on the new files.
  - [x] Update `roadmap.md` status to `done` for S2.1.
