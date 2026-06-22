import uuid
from typing import Any
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from google.adk.agents import LlmAgent
from app.models.schemes import CitizenProfile
from app.agents.contracts import PROFILE_KEY

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
    def run(self, *args, **kwargs) -> Any:
        req_id = str(uuid.uuid4())
        # We only log metadata, NEVER the raw text input or outputs
        logger.info(f"[{req_id}] Invoking IntakeAgent.")
        try:
            result = super().run(*args, **kwargs)
            logger.info(f"[{req_id}] IntakeAgent completed successfully.")
            return result
        except Exception:
            logger.error(f"[{req_id}] IntakeAgent failed.")
            raise
