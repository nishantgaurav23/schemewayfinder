# Spec S5.3: ExplainerAgent TTS out

## Overview
Enhance the existing `ExplainerAgent` to support returning an explanation in the user's native language via text-to-speech (TTS). After generating the plain-language English summary of matched schemes and rejected risks, the agent will translate the English summary back to the citizen's `source_language` using Bhashini NMT, and then generate an audio representation using Bhashini TTS.

## Dependencies
- Logical: `S5.1` (Bhashini MCP tool wiring), `S4.4` (ExplainerAgent)
- Technical: `BhashiniClient` from `app/mcp/bhashini/client.py`

## Target Location
- [MODIFY] `app/agents/explainer.py`
- [MODIFY] `tests/agents/test_explainer.py`

## Functional Requirements (FRs)

- **FR1: Read user's source_language from context**
  - **Inputs**: Session context containing `CitizenProfile` state with `source_language`.
  - **Outputs**: Extraction of the source language or a default to `en`.
  - **Edge Cases**: Missing state, missing profile, or missing language should safely default to `en`.

- **FR2: NMT Translation (English -> source_language)**
  - **Inputs**: Generated English plain-language summary string and the user's target `source_language`.
  - **Outputs**: Translated string in the target language.
  - **Edge Cases**: If `source_language` is `en`, skip NMT translation. Bhashini NMT failures should fallback gracefully, returning the English text.

- **FR3: TTS Audio Generation**
  - **Inputs**: Translated text and the `source_language`.
  - **Outputs**: Base64 encoded audio data containing the spoken text.
  - **Edge Cases**: If `source_language` is `en`, skip TTS (unless English TTS is supported natively without translation). Bhashini TTS failures should fail gracefully and just return the text response without audio.

## Tangible Outcomes
1. `app/agents/explainer.py` updated to conditionally invoke `BhashiniClient.nmt()` and `BhashiniClient.tts()` on the final LLM response.
2. `tests/agents/test_explainer.py` updated with mocks for Bhashini NMT and TTS, testing translation and audio generation paths.

## Test-Driven Requirements (TDD)
- `test_explainer_extracts_language`: Verify the ExplainerAgent extracts `source_language` from the context or correctly defaults to `en`.
- `test_explainer_skips_translation_for_en`: Verify that if language is `en`, neither NMT nor TTS are invoked.
- `test_explainer_nmt_and_tts`: Mock `BhashiniClient.nmt` and `BhashiniClient.tts` and verify they are correctly invoked when `source_language` is `hi` (Hindi) and the translated text + base64 audio is returned in the response object.
