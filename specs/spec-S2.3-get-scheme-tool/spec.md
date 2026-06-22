# Specification — S2.3: get_scheme(id) tool

## Overview
Implement the `get_scheme(id)` MCP tool on the custom `scheme-search` server. The tool takes a scheme ID, retrieves the full scheme details (including required documents, eligibility rules, and application URL), and returns the serialized scheme.

## Dependencies
- **Logical/Technical**:
  - [S2.1: FastMCP server bootstrap](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S2.1-fastmcp-server-bootstrap/spec.md)

## Target Location
- [app/mcp/scheme_search/tools.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/tools.py)
- [tests/mcp/test_get_scheme.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_get_scheme.py)

## Functional Requirements (FRs)

### **FR1**: Scheme Retrieval by ID
- **Inputs**: `id`: `str` (the unique identifier of the scheme, e.g. `pm-kisan`)
- **Outputs**: A JSON string representing the full details of the retrieved scheme.
- **Edge Cases**:
  - If the scheme ID is empty or not found in the corpus, return a JSON string with an error message: `{"error": "Scheme with ID '{id}' not found"}`.

### **FR2**: Full Scheme Details Serialization
- **Inputs**: A matched scheme from the corpus.
- **Outputs**: A JSON serialized string matching the `Scheme` model structure, ensuring that the eligibility rules, required documents list, and application URL are completely included.

---

## Tangible Outcomes
- Custom `get_scheme` tool registered at [app/mcp/scheme_search/tools.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/tools.py).
- Tool unit tests verifying successful lookup and missing scheme handling at [tests/mcp/test_get_scheme.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_get_scheme.py).

---

## Test-Driven Requirements (TDD)
1. **`test_get_scheme_success`**:
   - Mock/load a sample scheme corpus containing a test scheme (e.g., ID: `pm-kisan`).
   - Run the tool with `id="pm-kisan"`.
   - Assert that the output JSON string successfully parses back to a dict matching the scheme ID, description, required documents, and application URL.
2. **`test_get_scheme_not_found`**:
   - Run the tool with a non-existent scheme ID (e.g., `invalid-id`).
   - Assert that the output JSON string contains `{"error": "Scheme with ID 'invalid-id' not found"}`.
