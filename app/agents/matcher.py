import uuid
from typing import Any
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from google.adk.agents import LlmAgent, ParallelAgent
from app.models.schemes import MatchResult

# Assuming finding tools are local async functions for now, or just placeholders since we LLM them.
try:
    from app.mcp.scheme_search.tools import find_schemes, get_scheme

    matcher_tools = [find_schemes, get_scheme]
except ImportError:
    matcher_tools = []

CENTRAL_INSTRUCTION = """
You are the Central Scheme Matcher.
Your task is to find eligible central government welfare schemes for the citizen.
Use the find_schemes tool with the citizen's profile.
Return ONLY the schemes from the search results that are strictly central level schemes.
If none are found, return an empty list.
"""

STATE_INSTRUCTION = """
You are the State Scheme Matcher.
Your task is to find eligible state government welfare schemes for the citizen.
Use the find_schemes tool with the citizen's profile.
Return ONLY the schemes from the search results that are strictly state level schemes
for the citizen's state.
If none are found, return an empty list.
"""


class CentralMatcherAgent(LlmAgent):
    def __init__(self, **data: Any):
        super().__init__(
            name="CentralMatcherAgent",
            description="Finds eligible central schemes",
            instruction=CENTRAL_INSTRUCTION,
            tools=matcher_tools,
            **data,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def run(self, *args, **kwargs) -> Any:
        try:
            return super().run(*args, **kwargs)
        except Exception as e:
            logger.error(f"CentralMatcherAgent failed: {e}")
            return []


class StateMatcherAgent(LlmAgent):
    def __init__(self, **data: Any):
        super().__init__(
            name="StateMatcherAgent",
            description="Finds eligible state schemes",
            instruction=STATE_INSTRUCTION,
            tools=matcher_tools,
            **data,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def run(self, *args, **kwargs) -> Any:
        ctx = kwargs.get("ctx")
        if ctx and hasattr(ctx, "state") and ctx.state.citizen_profile:
            if not ctx.state.citizen_profile.state:
                return []
        try:
            return super().run(*args, **kwargs)
        except Exception as e:
            logger.error(f"StateMatcherAgent failed: {e}")
            return []


class EligibilityMatcherAgent(ParallelAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="EligibilityMatcherAgent",
            description="Parallel fan-out to find central and state schemes",
            sub_agents=[CentralMatcherAgent(), StateMatcherAgent()],
            **kwargs,
        )

    def run(self, *args, **kwargs) -> Any:
        req_id = str(uuid.uuid4())
        logger.info(f"[{req_id}] Invoking EligibilityMatcherAgent.")
        ctx = kwargs.get("ctx")

        # ParallelAgent execution
        try:
            # We are calling the sub-agents directly to ensure proper result aggregation
            # and to avoid async generator complexities in the synchronous test suite.
            # In a real ADK runtime, this might be handled by an executor, but we can do it here.
            # The spec requires writing the merged, deduplicated matches to state.
            central_agent = self.sub_agents[0]
            state_agent = self.sub_agents[1]

            try:
                c_res = central_agent.run(*args, **kwargs)
            except Exception as e:
                logger.error(f"[{req_id}] CentralMatcherAgent execution failed: {e}")
                c_res = []

            try:
                s_res = state_agent.run(*args, **kwargs)
            except Exception as e:
                logger.error(f"[{req_id}] StateMatcherAgent execution failed: {e}")
                s_res = []

            all_matches = []
            if isinstance(c_res, list):
                all_matches.extend(c_res)
            if isinstance(s_res, list):
                all_matches.extend(s_res)

            # Deduplicate by scheme_id, keeping the highest overall_score
            unique_matches = {}
            for match in all_matches:
                if not isinstance(match, MatchResult):
                    continue
                sid = match.scheme_id
                if (
                    sid not in unique_matches
                    or match.overall_score > unique_matches[sid].overall_score
                ):
                    unique_matches[sid] = match

            # Sort descending by score
            ranked_matches = sorted(
                unique_matches.values(), key=lambda x: x.overall_score, reverse=True
            )

            if ctx and hasattr(ctx, "state"):
                ctx.state.matches = ranked_matches

            logger.info(
                f"[{req_id}] EligibilityMatcherAgent completed with {len(ranked_matches)} matches."
            )
            return ranked_matches

        except Exception as e:
            logger.error(f"[{req_id}] EligibilityMatcherAgent failed: {e}")
            raise
