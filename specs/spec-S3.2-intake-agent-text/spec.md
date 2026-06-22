# Spec S3.2: IntakeAgent (text)

Free-text → structured `CitizenProfile`. English-only first.

## Overview

Translate a citizen's typed description of their situation (in English) into a validated, structured `CitizenProfile` using ADK's `LlmAgent` and Gemini. The structured profile is written directly into the ADK shared session state.

## Dependencies

- Technical: `google-adk` library, `google-genai` library, `pydantic`.
- Logical: `S3.1` (Agent contracts + shared state).

## Target Location

- [NEW] [intake.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/agents/intake.py)
- [NEW] [test_intake.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/agents/test_intake.py)

## Functional Requirements (FRs)

- **FR1**: Extract and build a structured `CitizenProfile` from English free-text user description.
  - **Inputs**: User input description text (string).
  - **Outputs**: A validated `CitizenProfile` Pydantic model.
  - **Edge Cases**:
    - Missing fields in user description: LLM should make reasonable assumptions/defaults or flag missing values if validation rules permit (e.g. default disability to false, category to General).
    - Invalid values: Ensure validations like `age > 0` and `income >= 0` are enforced. If invalid, the parser should fail gracefully with a descriptive error.
- **FR2**: Integrate with ADK `LlmAgent`.
  - **Inputs**: ADK `Context` enclosing the user message.
  - **Outputs**: Write the parsed model to `SessionState.citizen_profile` via the `PROFILE_KEY` (`"citizen_profile"`) shared state key.
  - **Edge Cases**: Model output fails JSON parsing or does not match the schema.
- **FR3**: Robust API Retries.
  - **Inputs**: Model API invocation.
  - **Outputs**: Automatic retry with exponential backoff on model failure (e.g., rate limit, server error) up to 3 attempts using `tenacity`.
- **FR4**: Metadata-only Logging.
  - **Inputs**: Run logs.
  - **Outputs**: Log request metadata, execution latency, and success/failure status via Loguru.
  - **Edge Cases**: Never log raw input text, name, address, or other PII.

## Tangible Outcomes

1. `app/agents/intake.py`: The `IntakeAgent` implementation, inheriting from or using ADK `LlmAgent` configured with `CitizenProfile` schema.
2. `tests/agents/test_intake.py`: Unit and integration tests using mocks to verify all extraction, validation, and state update pathways offline.

## Test-Driven Requirements (TDD)

- `test_intake_success`: Verifies a standard, descriptive free-text situation parses correctly into a valid `CitizenProfile` and is written to the session state under the `citizen_profile` key.
- `test_intake_invalid_values`: Verifies that if the user situation lists an invalid age or income, validation fails.
- `test_intake_missing_fields_defaults`: Verifies how the agent imputes defaults for parameters not specified in the text (e.g., default `disability = False` or `category = "General"`).
- `test_intake_retries_on_failure`: Verifies that `tenacity` retries are invoked 3 times before raising the API error if Gemini fails.
- `test_intake_logging_no_pii`: Verifies logs are written using `loguru` and do not contain the raw user text or sensitive profile fields.
