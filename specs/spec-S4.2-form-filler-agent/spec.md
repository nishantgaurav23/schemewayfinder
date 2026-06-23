# Spec S4.2: FormFillerAgent

Draft application from profile; emit structured form / PDF + apply URL.

## Overview
The `FormFillerAgent` generates a pre-filled application draft for the schemes matched by the `EligibilityMatcherAgent`. It uses the `CitizenProfile` data gathered during intake to auto-fill generic application fields (e.g., Name, Age, Income, State). It also extracts the application URL for each scheme and packages this into a single structured output, which acts as a draft for the citizen.

## Dependencies
- Logical: `S3.2` (IntakeAgent text), `S4.1` (DocumentChecklistAgent)
- Technical: `google-adk`

## Target Location
- [NEW] `app/agents/form_filler.py`
- [NEW] `tests/agents/test_form_filler.py`
- [MODIFY] `app/agents/contracts.py` (ensure DRAFT_KEY exists)
- [MODIFY] `app/agents/orchestrator.py`

## Functional Requirements (FRs)

- **FR1: Generate Application Draft**
  - **Inputs**: `SessionState.citizen_profile`, `SessionState.matches`
  - **Outputs**: A structured draft containing a form per matched scheme, auto-populated with data from `citizen_profile`, plus the `apply_url`. Written to `SessionState.application_draft` (or similar).
  - **Edge Cases**: If profile lacks certain fields, leave them blank or indicate "[To be filled]". If no matches, return an empty draft.

- **FR2: Handle Multiple Matches**
  - **Inputs**: Multiple `MatchResult` items.
  - **Outputs**: The draft should compile applications for all matched schemes, distinctly separated.

## Tangible Outcomes
1. `app/agents/form_filler.py` implemented as an `LlmAgent` or `BaseAgent`.
2. Unit tests in `tests/agents/test_form_filler.py`.
3. Orchestrator delegates to `FormFillerAgent` after the `DocumentChecklistAgent`.

## Test-Driven Requirements (TDD)
- `test_form_filler_success`: Mock a valid profile and matches. Verify the draft contains populated fields and apply URLs.
- `test_form_filler_empty_matches`: Verify that if matches are empty, it returns an empty or "No applications to fill" draft.
- `test_form_filler_missing_fields`: Verify it handles incomplete profiles correctly (e.g., by leaving placeholders).
