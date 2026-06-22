# Specification — S2.1: FastMCP server bootstrap

## Overview
Stand up the bootstrap configuration and main runner for the custom `scheme-search` FastMCP server. This server will host tools for matching and details retrieval, allowing the ADK orchestrator/matcher agents to consume them. It must expose a status/health check tool and be executable via `python -m app.mcp.scheme_search.server`.

## Dependencies
- **Logical/Technical**:
  - [S0.2: Skills authored](file:///Users/nishantgaurav/Project/schemewayfinder/roadmap.md)
  - [S1.3: Embeddings + vector index](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S1.3-embeddings-vector-index/spec.md)

## Target Location
- [app/mcp/scheme_search/server.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/server.py)
- [tests/mcp/test_server_sanity.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_server_sanity.py)

## Functional Requirements (FRs)

### **FR1**: FastMCP Server Instance
- **Inputs**: None.
- **Outputs**: An instantiated `FastMCP` server instance named `mcp`.
- **Edge Cases**: None.

### **FR2**: Server Status/Health Tool
- **Inputs**: None.
- **Outputs**: `str` indicating the server's health, number of schemes loaded, and cache status.
- **Edge Cases**:
  - Handles cases where no schemes are loaded by returning a valid status string indicating 0 schemes loaded, rather than crashing.

### **FR3**: Module Main Entrypoint
- **Inputs**: Running via `python -m app.mcp.scheme_search.server` or running the script directly.
- **Outputs**: Invokes standard FastMCP runner (`mcp.run()` or `mcp.settings`).
- **Edge Cases**: Ensures standard `if __name__ == "__main__":` block is configured.

---

## Tangible Outcomes
- Custom FastMCP server code at [app/mcp/scheme_search/server.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/server.py).
- Sanity unit tests verifying server properties at [tests/mcp/test_server_sanity.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_server_sanity.py).

## Test-Driven Requirements (TDD)
1. **`test_mcp_instance_creation`**:
   - Import the `mcp` instance from `app.mcp.scheme_search.server`.
   - Assert it is an instance of `FastMCP` and has the correct server name (`scheme-search`).
2. **`test_status_tool_registration`**:
   - Assert that a tool named `status` is registered on the `mcp` instance.
   - Execute the status tool handler function and verify the return string contains information like `"healthy"`.
