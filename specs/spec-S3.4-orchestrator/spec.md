# Spec S3.4: Orchestrator (delegation)

LlmAgent root; LLM-driven delegation; composes the run. Use `adk-agent-scaffold` skill.

## Overview

The Orchestrator agent will act as the root delegator for the SchemeWayfinder system. Instead of a rigid `SequentialAgent` pipeline, it will be refactored into an `LlmAgent` capable of LLM-driven delegation. It will inspect the current session context and the user's input, and dynamically decide which sub-agent to invoke next (e.g., routing to `IntakeAgent` to gather missing profile data, or `EligibilityMatcherAgent` once the profile is complete). 

## Dependencies

- Technical: `google-adk` library.
- Logical: `S3.2` (IntakeAgent), `S3.3` (EligibilityMatcherAgent).

## Target Location

- [MODIFY] `app/agents/orchestrator.py`
- [NEW] `tests/agents/test_orchestrator.py`

## Functional Requirements (FRs)

- **FR1: LLM-driven Delegation**
  - **Inputs**: User input query, current `SessionState`.
  - **Outputs**: Selection and invocation of the correct sub-agent (`IntakeAgent` or `EligibilityMatcherAgent`).
  - **Edge Cases**: Prevent infinite delegation loops; handle ambiguous user queries gracefully.
  
- **FR2: State Orchestration**
  - **Inputs**: Sub-agent responses.
  - **Outputs**: Properly passed and maintained `SessionState` context across delegations.
  - **Edge Cases**: Corrupted state or agent failures must be handled and surfaced properly.

## Tangible Outcomes

1. `app/agents/orchestrator.py`: Refactored `SchemeWayfinderOrchestrator` implemented as an `LlmAgent` (or equivalent delegation root) replacing the static `SequentialAgent`.
2. `tests/agents/test_orchestrator.py`: Unit tests asserting the LLM delegates correctly based on the session state.

## Test-Driven Requirements (TDD)

- `test_orchestrator_delegates_to_intake_when_profile_empty`: Asserts the orchestrator routes to `IntakeAgent` when `SessionState.citizen_profile` is missing or incomplete.
- `test_orchestrator_delegates_to_matcher_when_profile_ready`: Asserts the orchestrator routes to `EligibilityMatcherAgent` when a valid `CitizenProfile` exists.
- `test_orchestrator_handles_subagent_errors`: Asserts resilient error handling if a delegated sub-agent fails.
