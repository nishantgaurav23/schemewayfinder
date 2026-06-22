# Spec S3.3: EligibilityMatcherAgent

ParallelAgent fan-out: central ∥ state scoring via `find_schemes`. Writes ranked matches to state.

## Overview

The `EligibilityMatcherAgent` takes the `CitizenProfile` from the shared state and uses a `ParallelAgent` to concurrently search for eligible central and state schemes. It calls the `find_schemes` MCP tool, aggregates and ranks the resulting matches, and writes the final `matches` list back into the session state.

## Dependencies

- Technical: `google-adk` library, `mcp` (or the local tool implementation if integrated directly), `pydantic`.
- Logical: `S2.2` (`find_schemes` tool), `S3.1` (Agent contracts + shared state).

## Target Location

- [NEW] `app/agents/matcher.py`
- [NEW] `tests/agents/test_matcher.py`

## Functional Requirements (FRs)

- **FR1**: Execute parallel searches for "central" and "state" schemes.
  - **Inputs**: `SessionState.citizen_profile`.
  - **Outputs**: Concurrently calls the `find_schemes` tool for both levels (if state is specified).
  - **Edge Cases**: If `CitizenProfile.state` is not specified, it should only search for central schemes or gracefully handle the empty state query.
- **FR2**: Aggregate and rank scheme matches.
  - **Inputs**: Results from the parallel `find_schemes` calls.
  - **Outputs**: A single merged, deduplicated, and ranked list of `MatchResult` models.
  - **Edge Cases**: Empty results from one or both queries should result in an empty list.
- **FR3**: Integrate with ADK `ParallelAgent`.
  - **Inputs**: ADK `Context` with the `citizen_profile` populated.
  - **Outputs**: Writes the final ranked list to `SessionState.matches` via the appropriate output key mapping.
  - **Edge Cases**: Handling of sub-agent or tool execution errors gracefully (e.g., retries or returning partial results).

## Tangible Outcomes

1. `app/agents/matcher.py`: Implementation of `EligibilityMatcherAgent` (likely wrapping or inheriting from `ParallelAgent`) that uses the `find_schemes` capability.
2. `tests/agents/test_matcher.py`: Unit and integration tests using mocks for the MCP tool/sub-agents to verify parallel execution and result aggregation.

## Test-Driven Requirements (TDD)

- `test_matcher_success_parallel`: Verifies that central and state queries are dispatched and results are merged, ranked correctly, and written to state.
- `test_matcher_no_state_provided`: Verifies behavior when `CitizenProfile.state` is missing or null, ensuring only central schemes are queried.
- `test_matcher_empty_results`: Verifies that if no schemes match, an empty list is written to state without crashing.
- `test_matcher_tool_failure_handling`: Verifies how the agent handles failures from the underlying `find_schemes` calls (e.g., one fails but the other succeeds).
