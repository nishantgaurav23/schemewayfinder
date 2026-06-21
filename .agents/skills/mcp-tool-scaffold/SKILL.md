---
name: mcp-tool-scaffold
description: Scaffold a FastMCP tool on the SchemeWayfinder scheme-search server (schema, handler, test) or wire a consumed MCP tool. Use when adding find_schemes, get_scheme, or any MCP tool.
---

# Skill: mcp-tool-scaffold

When asked to add an MCP tool:

1. In `app/mcp/scheme_search/tools.py`, define the tool with a typed signature and a clear docstring (the MCP description). Inputs/outputs use Pydantic models from `app/models/schemes.py`.
2. Register it on the FastMCP server in `app/mcp/scheme_search/server.py` so it appears in the server's tool list.
3. Create `tests/mcp/test_{tool}.py` FIRST: call the tool through an MCP client against fixtures; assert the structured result and edge cases (no match, malformed profile).
4. For a CONSUMED tool (e.g., Bhashini), wire it via `McpToolset` in `app/mcp/bhashini/client.py` with Tenacity retries and graceful timeouts; mock it in tests.
5. No secrets in code; read endpoints/keys from `app/core/config.py`.
6. Run `make test`; the server must list the tool and tests must pass.

Output: tool definition + registration + test, all green.
