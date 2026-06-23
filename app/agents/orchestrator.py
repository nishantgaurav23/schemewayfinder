from google.adk.agents import LlmAgent
from app.agents.intake import IntakeAgent
from app.agents.matcher import EligibilityMatcherAgent
from app.agents.auditor import create_auditor_agent
from app.agents.documents import create_document_agent
from app.agents.form_filler import create_form_filler_agent
from app.agents.explainer import create_explainer_agent


def create_orchestrator() -> LlmAgent:
    intake = IntakeAgent()
    matcher = EligibilityMatcherAgent()
    auditor = create_auditor_agent()
    documents = create_document_agent()
    form_filler = create_form_filler_agent()
    explainer = create_explainer_agent()

    instruction = (
        "You are the central orchestrator of SchemeWayfinder.\n\n"
        "1. If the user's citizen profile is missing or incomplete, invoke the IntakeAgent.\n"
        "2. If the user's citizen profile is fully collected and ready, invoke the "
        "EligibilityMatcherAgent.\n"
        "3. After the EligibilityMatcherAgent finds matches, invoke the "
        "RejectionRiskAuditorAgent to verify them.\n"
        "4. Once verified matches have been found and you need to gather required documents, "
        "invoke the DocumentChecklistAgent.\n"
        "5. After the DocumentChecklistAgent completes, invoke the FormFillerAgent to draft "
        "the application.\n"
        "6. Finally, after the FormFillerAgent completes, invoke the ExplainerAgent to generate a "
        "plain-language summary for the user.\n\n"
        "Always use the state to decide the next step."
    )

    return LlmAgent(
        name="SchemeWayfinderOrchestrator",
        description="Main orchestrator for SchemeWayfinder using LLM delegation",
        instruction=instruction,
        sub_agents=[intake, matcher, auditor, documents, form_filler, explainer],
    )
