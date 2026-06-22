# Specification — S2.2: find_schemes(profile) tool

## Overview
Implement the `find_schemes(profile)` MCP tool on the custom `scheme-search` server. The tool takes a citizen's profile, retrieves relevant candidate schemes from the cached index, runs detailed rule evaluations against their profile criteria, and returns matching status and rule-level results.

## Dependencies
- **Logical/Technical**:
  - [S2.1: FastMCP server bootstrap](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S2.1-fastmcp-server-bootstrap/spec.md)

## Target Location
- [app/mcp/scheme_search/tools.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/tools.py)
- [tests/mcp/test_find_schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_find_schemes.py)

## Functional Requirements (FRs)

### **FR1**: CitizenProfile Input Handling
- **Inputs**: `profile`: `Dict[str, Any]` (or `CitizenProfile` model representation)
- **Outputs**: A parsed `CitizenProfile` instance.
- **Edge Cases**:
  - Invalid profile schema should raise a validation error.

### **FR2**: Rule Comparison Evaluation
- **Inputs**: `Scheme` eligibility rules and parsed `CitizenProfile`.
- **Outputs**: Categorized lists of `matched_rules` and `failed_rules`.
- **Supported operators**:
  - `>=`: profile value must be greater than or equal to rule value.
  - `<=`: profile value must be less than or equal to rule value.
  - `==`: profile value must be equal to rule value (handling casing differences).
  - `in`: profile value must be present in the rule's value list.
  - `contains`: profile value list must contain the rule's value.

### **FR3**: Overall Matching & Score Calculation
- **Inputs**: Categorized evaluation lists.
- **Outputs**: A structured list of matching candidate results (`MatchResult`), where:
  - `is_eligible` is `True` if no critical rules fail.
  - `overall_score` represents the ratio of passed rules to total rules (`1.0` if all pass, `0.0` if none pass or if a critical blocker fails).

---

## Tangible Outcomes
- Custom `find_schemes` tool registered at [app/mcp/scheme_search/tools.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/mcp/scheme_search/tools.py).
- Tool unit tests verifying matcher logic at [tests/mcp/test_find_schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/mcp/test_find_schemes.py).

## Test-Driven Requirements (TDD)
1. **`test_find_schemes_fully_eligible`**:
   - Mock candidate schemes loaded in the database.
   - Run search with profile matching all criteria.
   - Assert `is_eligible=True`, `overall_score=1.0`, and empty `failed_rules`.
2. **`test_find_schemes_ineligible_rule`**:
   - Run search with profile failing a specific criteria (e.g. age limit).
   - Assert `is_eligible=False`, `overall_score < 1.0`, and the failed rule is in `failed_rules`.
