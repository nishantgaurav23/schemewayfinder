# Checklist S5.1: Bhashini MCP tool wiring

Implementation progress tracker for spec S5.1.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Ensure required dependencies (`tenacity`, ADK MCP components) are in `pyproject.toml`.
  - [x] Create `app/mcp/bhashini/client.py` and `tests/mcp/test_bhashini_client.py`.

- [x] **Phase 2: Tests First (TDD)**
  - [x] Write `test_bhashini_client_initialization` in `test_bhashini_client.py`.
  - [x] Write `test_bhashini_retries_on_failure` demonstrating Tenacity logic.
  - [x] Write `test_bhashini_graceful_timeout`.
  - [x] Run `make test` and verify that the new tests fail (Red phase).

- [x] **Phase 3: Implementation**
  - [x] Implement the Bhashini `McpToolset` setup in `client.py`.
  - [x] Implement wrappers for ASR, NMT, and TTS tools with `@retry` and timeouts.
  - [x] Run `make test` and verify tests pass (Green phase).

- [x] **Phase 4: Integration**
  - [x] Verify that the `config.py` correctly loads Bhashini connection secrets.
  - [x] Ensure the tools can be imported and injected into agents (preparation for S5.2 and S5.3).

- [x] **Phase 5: Verification**
  - [x] Run `make lint` to verify code format with Ruff.
  - [x] Ensure no API keys or secrets are hardcoded.
  - [x] Update `roadmap.md` status of `S5.1` to `done`.
