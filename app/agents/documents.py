import json
import uuid
from typing import Any
from loguru import logger
from google.adk.agents import BaseAgent
from app.agents.contracts import CHECKLIST_KEY, MATCHES_KEY


def get_scheme_impl(scheme_id: str) -> str:
    from app.mcp.scheme_search.tools import get_scheme
    import asyncio

    try:
        # get_scheme is an async tool function (FastMCP)
        # We need to run it synchronously here
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(get_scheme(scheme_id))
    except RuntimeError:
        # If there's no event loop, run it
        return asyncio.run(get_scheme(scheme_id))


class DocumentChecklistAgent(BaseAgent):
    def __init__(self, **data: Any):
        super().__init__(name="DocumentChecklistAgent", **data)

    def run(self, state: dict, *args, **kwargs) -> dict:
        req_id = str(uuid.uuid4())
        logger.info(f"[{req_id}] Invoking DocumentChecklistAgent.")

        matches = state.get(MATCHES_KEY, [])
        if not matches:
            logger.info(f"[{req_id}] No matches found. Returning empty checklist.")
            state[CHECKLIST_KEY] = []
            return state

        docs_set = set()
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

                req_docs = scheme_data.get("required_documents", [])
                for doc in req_docs:
                    docs_set.add(doc)
            except Exception as e:
                logger.error(f"[{req_id}] Failed to fetch documents for {scheme_id}: {e}")

        checklist = list(docs_set)
        state[CHECKLIST_KEY] = checklist
        logger.info(
            f"[{req_id}] DocumentChecklistAgent completed. Collected {len(checklist)} docs."
        )
        return state


def create_document_agent() -> BaseAgent:
    return DocumentChecklistAgent()
