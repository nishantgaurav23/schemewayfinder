# Spec S5.2: Intake voice + in-language

## Overview
Enhance the existing `IntakeAgent` to support voice inputs and multilingual text. The agent will use the Bhashini MCP tools (from S5.1) to convert voice to text (ASR) and translate non-English text to the working language (English) via NMT. The user's original language must be carried through the session state to ensure downstream agents (like `ExplainerAgent`) can respond in the correct language.

## Dependencies
- Logical: `S5.1` (Bhashini MCP tool wiring), `S3.2` (IntakeAgent text)
- Technical: `BhashiniClient` from `app/mcp/bhashini/client.py`

## Target Location
- [MODIFY] `app/agents/intake.py`
- [MODIFY] `tests/agents/test_intake.py`

## Functional Requirements (FRs)

- **FR1: Audio processing via ASR**
  - **Inputs**: Base64 encoded audio data and source language identifier.
  - **Outputs**: Transcribed text in the source language using Bhashini ASR.
  - **Edge Cases**: Empty audio, unsupported format, or ASR service failure should raise a clear error or fallback gracefully.

- **FR2: Translation to Working Language**
  - **Inputs**: Non-English text (transcribed from audio or provided directly).
  - **Outputs**: English text translated via Bhashini NMT, which the LLM will then process to extract the `CitizenProfile`.
  - **Edge Cases**: NMT service timeout or failure should be handled via the Tenacity retries implemented in S5.1.

- **FR3: Language State Propagation**
  - **Inputs**: Source language parameter provided at intake.
  - **Outputs**: The structured state (e.g., `CitizenProfile` or session state) must explicitly store the `source_language` so downstream agents know which language to use.
  - **Edge Cases**: Default to English (`en`) if no language is specified or if detection fails.

## Tangible Outcomes
1. `app/agents/intake.py` updated to conditionally invoke `BhashiniClient.asr()` and `BhashiniClient.nmt()` before the LLM extraction step.
2. `tests/agents/test_intake.py` updated with mocks for Bhashini, testing the voice and translation paths. Test coverage must include Hindi and at least two other languages (e.g., Marathi, Tamil).

## Test-Driven Requirements (TDD)
- `test_intake_asr_transcription`: Mock `BhashiniClient.asr` and verify that audio input correctly routes through ASR and produces a profile.
- `test_intake_nmt_translation`: Mock `BhashiniClient.nmt` and verify that non-English text is translated to English before being sent to the LLM.
- `test_intake_multilingual_coverage`: Parameterize a test over Hindi (`hi`), Marathi (`mr`), and Tamil (`ta`) to ensure the pipeline correctly propagates the language ID and invokes the expected tools.
