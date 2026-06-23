# Spec S4.4: ExplainerAgent

Plain-language summary + next steps + disclaimer.

## Overview
The `ExplainerAgent` is responsible for generating a plain-language summary of the results produced by the preceding agents. It takes the citizen profile, the matched schemes, the required document checklist, and any application drafts or rejected matches, and synthesizes them into an easy-to-understand explanation for the citizen. This includes summarizing what they qualify for, what they need to do next, and injecting a disclaimer that the output is informational and not a formal eligibility determination.

## Dependencies
- Logical: `S4.2` (FormFillerAgent), `S4.3` (RejectionRiskAuditorAgent)
- Technical: `google-adk`, `pydantic`

## Target Location
- [NEW] `app/agents/explainer.py`
- [NEW] `tests/agents/test_explainer.py`
- [MODIFY] `app/agents/orchestrator.py`

## Functional Requirements (FRs)

- **FR1: Plain-Language Generation**
  - **Inputs**: `SessionState` containing `citizen_profile`, `matches`, `checklist`, `application_draft`, and `rejected_matches`.
  - **Outputs**: Returns an updated `SessionState` with the `explanation` field populated. The string must contain a summary of matched schemes, next steps based on the checklist/drafts, and why some schemes were rejected (if applicable).
  - **Edge Cases**: If no matches are found, the explanation should gently inform the user that no schemes match their current profile.

- **FR2: Disclaimer Injection**
  - **Inputs**: The generated explanation string.
  - **Outputs**: Ensures that every generated explanation strictly ends with a standard disclaimer: *"This information is provided for guidance only and does not constitute a formal eligibility determination."* This can be done via prompt engineering or an ADK `after_model_callback`.

## Tangible Outcomes
1. `app/agents/explainer.py` implemented as an ADK `LlmAgent`.
2. Unit tests in `tests/agents/test_explainer.py` ensuring the explanation is generated and includes the disclaimer.
3. Orchestrator updated to route to the ExplainerAgent as the final step.

## Test-Driven Requirements (TDD)
- `test_explainer_success`: Mock the LLM call to return a standard explanation. Verify the `explanation` field is populated in state and includes the mandatory disclaimer.
- `test_explainer_no_matches`: Mock state with zero matches and verify the explanation gracefully handles this.
- `test_explainer_includes_disclaimer_callback`: Verify that the disclaimer is appended correctly via an `after_model_callback` or prompt.
