# Spec S5.1: Bhashini MCP tool wiring

## Overview
Consume Bhashini via McpToolset to enable ASR (Automatic Speech Recognition), NMT (Neural Machine Translation), and TTS (Text-to-Speech) capabilities. This establishes the foundational multilingual layer. The integration must include Tenacity retries, graceful timeouts, and robust audio format handling to ensure reliability.

## Dependencies
- Logical: `S0.2` (Skills authored), `S3.2` (IntakeAgent text)
- Technical: `google.adk.mcp.McpToolset`, `tenacity`

## Target Location
- [NEW] `app/mcp/bhashini/client.py`
- [NEW] `tests/mcp/test_bhashini_client.py`

## Functional Requirements (FRs)

- **FR1: Bhashini MCP Client Setup**
  - **Inputs**: Bhashini MCP server configuration (e.g., API keys, endpoint URL from `config.py`).
  - **Outputs**: An initialized `McpToolset` instance connected to the Bhashini server, exposing ASR, NMT, and TTS tools.
  - **Edge Cases**: Handle connection timeouts or missing configuration gracefully without crashing the app.

- **FR2: Tool Wrappers with Retries**
  - **Inputs**: Native calls to the underlying MCP tools for ASR, NMT, and TTS.
  - **Outputs**: Wrapped functions or methods that apply Tenacity retries (e.g., 3 attempts, exponential backoff) and graceful timeouts.
  - **Edge Cases**: Handle underlying HTTP errors, rate limits, or invalid audio formats by throwing structured exceptions or returning safe fallback values.

## Tangible Outcomes
1. `app/mcp/bhashini/client.py` containing the `McpToolset` configuration and robust tool wrappers.
2. `tests/mcp/test_bhashini_client.py` validating the retries, timeouts, and successful tool binding.

## Test-Driven Requirements (TDD)
- `test_bhashini_client_initialization`: Verify that the MCP toolset is correctly configured and loads the expected tools.
- `test_bhashini_retries_on_failure`: Mock a tool failure and verify that Tenacity retries the call up to 3 times before failing.
- `test_bhashini_graceful_timeout`: Verify that the wrappers enforce a timeout and handle it cleanly.
