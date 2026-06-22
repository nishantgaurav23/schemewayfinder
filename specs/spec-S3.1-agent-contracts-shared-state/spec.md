# Specification — S3.1: Agent contracts + shared state

## Overview
Define the structured shared state model (`SessionState`) and the handoff contracts (`output_key` definitions) used for coordination among the Google Agent Development Kit (ADK) agents. Handoffs between agents must write to specific structured locations in the shared session state rather than relying on free-form text relays.

## Dependencies
- **Logical/Technical**:
  - [S0.2: Skills authored](file:///Users/nishantgaurav/Project/specs/spec-S0.2-skills-authored/spec.md) (ADK scaffolding templates context)
  - [S1.2: Corpus schema + models](file:///Users/nishantgaurav/Project/specs/spec-S1.2-corpus-schema-models/spec.md)

## Target Location
- [app/agents/contracts.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/agents/contracts.py)
- [tests/agents/test_contracts.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/agents/test_contracts.py)

## Functional Requirements (FRs)

### **FR1**: Structured `SessionState` Model
- **Inputs**: Dict representation of session state data.
- **Outputs**: Validated `SessionState` Pydantic model containing:
  - `citizen_profile`: `Optional[CitizenProfile]` (default `None`)
  - `matches`: `List[MatchResult]` (default empty list)
  - `checklist`: `List[str]` (default empty list)
  - `application_draft`: `Optional[str]` (default `None`)
  - `rejection_risk_audit`: `Optional[dict]` (default `None`)
  - `explanation`: `Optional[str]` (default `None`)

### **FR2**: Handoff `output_key` Constants
- **Inputs**: None.
- **Outputs**: Constant string identifiers ensuring type-safe keys during orchestrator delegation runs:
  - `PROFILE_KEY` = `"citizen_profile"`
  - `MATCHES_KEY` = `"matches"`
  - `CHECKLIST_KEY` = `"checklist"`
  - `DRAFT_KEY` = `"application_draft"`
  - `AUDIT_KEY` = `"rejection_risk_audit"`
  - `EXPLANATION_KEY` = `"explanation"`

---

## Tangible Outcomes
- `SessionState` Pydantic model and string keys implemented at [app/agents/contracts.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/agents/contracts.py).
- Integration test assertions verifying state schemas at [tests/agents/test_contracts.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/agents/test_contracts.py).

---

## Test-Driven Requirements (TDD)
1. **`test_session_state_defaults`**:
   - Instantiate `SessionState` with no arguments.
   - Assert all fields default to empty values (either `None` or `[]`).
2. **`test_session_state_validation`**:
   - Instantiate `SessionState` with valid profile and list matches, verifying type constraints.
   - Assert nested validation checks raise `ValidationError` when fields (such as `matches` or `citizen_profile`) contain malformed nested model data.
