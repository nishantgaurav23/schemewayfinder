import json
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Any
from app.agents.contracts import EXPLANATION_KEY
from tenacity import retry, stop_after_attempt, wait_exponential


class ExplainerOutput(BaseModel):
    text: str = Field(
        description=(
            "The plain-language summary addressing the citizen, summarizing "
            "their eligibility, next steps, and rejected matches."
        )
    )


def inject_disclaimer_callback(agent: Any, output: Any) -> Any:
    disclaimer = (
        "\n\n*Disclaimer: This information is provided for guidance only and "
        "does not constitute a formal eligibility determination.*"
    )
    if hasattr(output, "text"):
        output.text += disclaimer
    elif isinstance(output, dict) and "text" in output:
        output["text"] += disclaimer
    return output


class ExplainerAgent(LlmAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="ExplainerAgent",
            description=(
                "Generates a plain-language summary of scheme matches and "
                "next steps for the citizen."
            ),
            instruction=(
                "You are an empathetic public servant helping citizens understand "
                "which government schemes they qualify for. "
                "Read the citizen profile, the matched schemes, the required document checklist, "
                "and any rejected matches. "
                "Synthesize this into a clear, plain-language summary. "
                "Address the citizen directly (e.g., 'Based on your profile, ...'). "
                "If there are no matches, kindly inform them."
            ),
            output_schema=ExplainerOutput,
            after_model_callback=inject_disclaimer_callback,
            **kwargs,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def run(self, *args, **kwargs) -> Any:
        ctx = kwargs.get("ctx")
        state = kwargs.get("state", {})

        if not state and args:
            state = args[0]
        elif ctx and hasattr(ctx, "state"):
            state = ctx.state

        if hasattr(state, "model_dump"):
            state = state.model_dump()

        prompt = f"""
        Please provide a plain-language explanation of the results for the citizen.

        Citizen Profile:
        {json.dumps(state.get("citizen_profile", {}), indent=2)}

        Matches:
        {json.dumps(state.get("matches", []), indent=2)}

        Checklist:
        {json.dumps(state.get("checklist", []), indent=2)}

        Rejected Matches (if any):
        {json.dumps(state.get("rejected_matches", []), indent=2)}
        """

        llm_result = super().run(node_input=prompt, ctx=ctx)

        output = (
            llm_result.get("structured_output", llm_result)
            if isinstance(llm_result, dict)
            else llm_result
        )
        output_text = (
            getattr(output, "text", "")
            if hasattr(output, "text")
            else (output.get("text", "") if isinstance(output, dict) else str(output))
        )

        disclaimer = (
            "\n\n*Disclaimer: This information is provided for guidance only and "
            "does not constitute a formal eligibility determination.*"
        )
        if disclaimer not in output_text:
            output_text += disclaimer

        state[EXPLANATION_KEY] = output_text

        if ctx and hasattr(ctx, "state"):
            setattr(ctx.state, EXPLANATION_KEY, output_text)

        return state


def create_explainer_agent() -> LlmAgent:
    return ExplainerAgent()
