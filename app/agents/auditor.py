import json
from loguru import logger
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List, Any
from app.agents.contracts import MATCHES_KEY, REJECTED_MATCHES_KEY
from tenacity import retry, stop_after_attempt, wait_exponential


class AuditorOutput(BaseModel):
    rejected_scheme_ids: List[str] = Field(
        description="List of scheme IDs that should be rejected "
        "because the match is hallucinated or weak based on eligibility rules."
    )
    reasons: dict[str, str] = Field(
        description="A dictionary mapping rejected scheme IDs to the reason for rejection."
    )
    continue_loop: bool = Field(
        description="Whether the loop should continue for further inspection."
    )


class RejectionRiskAuditorAgent(LlmAgent):
    """
    Evaluates MatchResults against the CitizenProfile to filter out
    hallucinations or weak matches.
    """

    max_iterations: int = 2

    def __init__(self, max_iterations: int = 2, **kwargs):
        super().__init__(
            name="RejectionRiskAuditorAgent",
            description=(
                "Evaluates MatchResults against the CitizenProfile "
                "to filter out hallucinations or weak matches."
            ),
            instruction=(
                "You are an expert policy auditor validating scheme eligibility matches. Be strict."
            ),
            output_schema=AuditorOutput,
            **kwargs,
        )
        self.max_iterations = max_iterations

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def run(self, *args, **kwargs) -> Any:
        ctx = kwargs.get("ctx")
        state = kwargs.get("state", {})

        # If the first positional argument is the state
        if not state and args:
            state = args[0]
        elif ctx and hasattr(ctx, "state"):
            state = ctx.state

        # Convert to dict if it's a Pydantic model
        if hasattr(state, "model_dump"):
            state = state.model_dump()

        profile_data = state.get("citizen_profile", {}) if isinstance(state, dict) else {}
        matches_data = state.get(MATCHES_KEY, []) if isinstance(state, dict) else []

        if not profile_data or not matches_data:
            return state

        iterations = 0
        while iterations < self.max_iterations:
            iterations += 1

            prompt = f"""
            You are a strict quality guardrail agent. Review the following scheme matches against
            the citizen's profile.
            If a match clearly violates an eligibility rule based on the profile, it is a
            hallucination and must be rejected.

            Citizen Profile:
            {json.dumps(profile_data, indent=2)}

            Matches:
            {json.dumps(matches_data, indent=2)}
            """

            # Use LlmAgent's core processing by treating prompt as standard LLM input.
            llm_result = super().run(node_input=prompt, ctx=ctx)
            output: AuditorOutput = (
                llm_result.get("structured_output") if isinstance(llm_result, dict) else llm_result
            )

            if not output:
                break

            rejected_scheme_ids = output.rejected_scheme_ids
            reasons = output.reasons

            if not rejected_scheme_ids:
                break

            valid_matches = []
            rejected_matches = state.get(REJECTED_MATCHES_KEY, [])
            if rejected_matches is None:
                rejected_matches = []

            for match in matches_data:
                if match["scheme_id"] in rejected_scheme_ids:
                    match["reason"] = reasons.get(match["scheme_id"], "Violated eligibility rules")
                    rejected_matches.append(match)
                    logger.info(f"Auditor rejected match {match['scheme_id']}: {match['reason']}")
                else:
                    valid_matches.append(match)

            state[MATCHES_KEY] = valid_matches
            state[REJECTED_MATCHES_KEY] = rejected_matches
            matches_data = valid_matches

            if not output.continue_loop:
                break

        # If running in an ADK Context flow, update it.
        if ctx and hasattr(ctx, "state"):
            ctx.state.matches = matches_data
            if hasattr(ctx.state, "rejected_matches"):
                ctx.state.rejected_matches = state[REJECTED_MATCHES_KEY]

        return state


def create_auditor_agent() -> LlmAgent:
    return RejectionRiskAuditorAgent()
