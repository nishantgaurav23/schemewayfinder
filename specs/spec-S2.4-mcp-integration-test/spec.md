# Specification — S2.4: MCP integration test

## Overview
Implement end-to-end MCP integration tests for the custom `scheme-search` FastMCP server. The tests will verify that an MCP client can invoke both `find_schemes(profile)` and `get_scheme(id)` tools and receive the correct structured JSON outputs matching our Pydantic schemas.

## Dependencies
- **Logical/Technical**:
  - [S2.2: find_schemes(profile) tool](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S2.2-find-schemes-tool/spec.md)
  - [S2.3: get_scheme(id) tool](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S2.3-get-scheme-tool/spec.md)

## Target Location
- [tests/mcp/test_scheme_search.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_scheme_search.py)

## Functional Requirements (FRs)

### **FR1**: End-to-End Client Execution of `find_schemes`
- **Inputs**: A valid citizen profile payload.
- **Outputs**: Assert client-side execution returns a JSON representation of candidate matching scores and rules.

### **FR2**: End-to-End Client Execution of `get_scheme`
- **Inputs**: A valid scheme ID.
- **Outputs**: Assert client-side execution returns the correct serialized scheme structure.

---

## Tangible Outcomes
- Integration test suite at [tests/mcp/test_scheme_search.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_scheme_search.py) validating client tool execution.

---

## Test-Driven Requirements (TDD)
1. **`test_mcp_client_find_schemes`**:
   - Call the `find_schemes` tool through the FastMCP server client interface with a sample citizen profile.
   - Assert results match the eligibility output structure.
2. **`test_mcp_client_get_scheme`**:
   - Call the `get_scheme` tool through the FastMCP server client interface with a sample scheme ID.
   - Assert returns the serialized scheme.
