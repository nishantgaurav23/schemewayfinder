from google.adk.agents import LlmAgent
from app.agents.intake import IntakeAgent
from app.agents.matcher import EligibilityMatcherAgent


def create_orchestrator() -> LlmAgent:
    intake = IntakeAgent()
    matcher = EligibilityMatcherAgent()

    # The Orchestrator uses LLM-driven delegation to route the session.
    instruction = """You are the SchemeWayfinder Orchestrator. 
Your job is to route the user's request to the appropriate agent.
1. If the user's citizen profile is missing or incomplete, invoke the IntakeAgent.
2. If the user's citizen profile is fully collected and ready, invoke the EligibilityMatcherAgent.
Do not attempt to answer questions directly; always delegate to your sub-agents."""

    return LlmAgent(
        name="SchemeWayfinderOrchestrator",
        description="Main orchestrator for SchemeWayfinder using LLM delegation",
        instruction=instruction,
        sub_agents=[intake, matcher],
    )
