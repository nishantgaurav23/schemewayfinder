import uuid
import asyncio
from typing import Any
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from google.adk.agents import LlmAgent
from app.models.schemes import CitizenProfile
from app.agents.contracts import PROFILE_KEY
from app.mcp.bhashini.client import BhashiniClient

INTAKE_INSTRUCTION = """
You are the SchemeWayfinder Intake Agent.
Your job is to extract a citizen's profile from their situation description.
Extract: age, income, state, category, disability, occupation.
If any field is missing:
- disability defaults to False
- category defaults to "General"
- occupation defaults to None
- state is required. If not provided, make your best guess based on language or location mentions.
"""


class IntakeAgent(LlmAgent):
    def __init__(self, **data: Any):
        super().__init__(
            name="IntakeAgent",
            description="Extracts a CitizenProfile from a user description",
            instruction=INTAKE_INSTRUCTION,
            output_schema=CitizenProfile,
            output_key=PROFILE_KEY,
            **data,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def run(
        self,
        node_input: str = None,
        audio_data: bytes = None,
        source_language: str = "en",
        ctx=None,
        **kwargs,
    ) -> Any:
        req_id = str(uuid.uuid4())
        # We only log metadata, NEVER the raw text input or outputs
        logger.info(
            f"[{req_id}] Invoking IntakeAgent (audio: {bool(audio_data)}, lang: {source_language})."
        )
        try:
            bhashini = BhashiniClient()

            # Process ASR if audio provided
            if audio_data:
                node_input = asyncio.run(bhashini.asr(audio_data, source_language))

            # Process NMT if language is not English
            if source_language != "en" and node_input:
                node_input = asyncio.run(bhashini.nmt(node_input, source_language, "en"))

            # Call LLM extraction
            result = super().run(node_input=node_input, ctx=ctx, **kwargs)

            # Force source_language propagation into the state
            if ctx and getattr(ctx, "state", None) and getattr(ctx.state, "citizen_profile", None):
                ctx.state.citizen_profile.source_language = source_language

            logger.info(f"[{req_id}] IntakeAgent completed successfully.")
            return result
        except Exception:
            logger.error(f"[{req_id}] IntakeAgent failed.")
            raise
