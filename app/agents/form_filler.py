import json
import uuid
from typing import Any
from loguru import logger
from google.adk.agents import BaseAgent
from app.agents.contracts import MATCHES_KEY, DRAFT_KEY, PROFILE_KEY


def get_scheme_impl(scheme_id: str) -> str:
    from app.mcp.scheme_search.tools import get_scheme
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(get_scheme(scheme_id))
    except RuntimeError:
        return asyncio.run(get_scheme(scheme_id))


class FormFillerAgent(BaseAgent):
    def __init__(self, **data: Any):
        super().__init__(name="FormFillerAgent", **data)

    def run(self, state: dict, *args, **kwargs) -> dict:
        req_id = str(uuid.uuid4())
        logger.info(f"[{req_id}] Invoking FormFillerAgent.")

        matches = state.get(MATCHES_KEY, [])
        if not matches:
            logger.info(f"[{req_id}] No matches found. Returning empty draft.")
            state[DRAFT_KEY] = "No applications to fill."
            return state

        # We will safely access dict or pydantic model for profile
        raw_profile = state.get(PROFILE_KEY, {})
        profile = (
            raw_profile
            if isinstance(raw_profile, dict)
            else (raw_profile.model_dump() if hasattr(raw_profile, "model_dump") else {})
        )

        draft_parts = []
        for match in matches:
            scheme_id = (
                match.get("scheme_id")
                if isinstance(match, dict)
                else getattr(match, "scheme_id", None)
            )
            if not scheme_id:
                continue

            try:
                scheme_data_str = get_scheme_impl(scheme_id)
                scheme_data = json.loads(scheme_data_str)
                if "error" in scheme_data:
                    logger.warning(
                        f"[{req_id}] Error fetching scheme {scheme_id}: {scheme_data['error']}"
                    )
                    continue

                scheme_name = scheme_data.get("name", "Unknown Scheme")
                apply_url = scheme_data.get("apply_url") or "No apply URL available"

                form_lines = [
                    f"--- Application Draft: {scheme_name} ---",
                    f"Apply URL: {apply_url}",
                    "Applicant Details:",
                ]

                # We populate from profile, falling back to placeholders
                fields_to_fill = ["age", "income", "state", "category", "occupation"]
                for field in fields_to_fill:
                    val = profile.get(field)
                    display_val = (
                        str(val) if val is not None and str(val).strip() else "[To be filled]"
                    )
                    form_lines.append(f"  - {field.capitalize()}: {display_val}")

                draft_parts.append("\n".join(form_lines))

            except Exception as e:
                logger.error(f"[{req_id}] Failed to generate draft for {scheme_id}: {e}")

        if not draft_parts:
            state[DRAFT_KEY] = "No applications to fill."
        else:
            state[DRAFT_KEY] = "\n\n".join(draft_parts)

        logger.info(
            f"[{req_id}] FormFillerAgent completed. Drafted {len(draft_parts)} applications."
        )
        return state


def create_form_filler_agent() -> BaseAgent:
    return FormFillerAgent()
