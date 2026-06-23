import pytest
from unittest.mock import patch
from app.agents.contracts import SessionState
from app.models.schemes import CitizenProfile, MatchResult
from app.agents.explainer import create_explainer_agent


@pytest.fixture
def mock_session():
    class MockContext:
        def __init__(self):
            self.state = SessionState()

    return MockContext()


@patch("app.agents.explainer.LlmAgent.run")
def test_explainer_success(mock_llm_call):
    # Mock LLM returning a plain language summary
    mock_llm_call.return_value = {
        "text": (
            "Based on your profile, you are eligible for the PM Kisan scheme. "
            "We have created a draft application for you."
        )
    }

    agent = create_explainer_agent()
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=30,
            income=50000.0,
            state="Maharashtra",
            category="General",
            disability=False,
            occupation="Farmer",
        ),
        matches=[
            MatchResult(
                scheme_id="pm_kisan",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            )
        ],
        checklist=["Aadhaar Card", "Bank Passbook"],
        application_draft="Draft application for PM Kisan: Name...",
        rejected_matches=[],
    )

    result_state = agent.run(state=state)

    # Explanation must be in state and must contain the disclaimer
    assert result_state.get("explanation") is not None
    assert "Based on your profile" in result_state["explanation"]
    assert "guidance only" in result_state["explanation"]
    assert "not constitute a formal eligibility determination" in result_state["explanation"]


@patch("app.agents.explainer.LlmAgent.run")
def test_explainer_no_matches(mock_llm_call):
    # Mock LLM returning a gentle response
    mock_llm_call.return_value = {
        "text": "I'm sorry, but we couldn't find any schemes matching your current profile."
    }

    agent = create_explainer_agent()
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=30, income=1500000.0, state="Maharashtra", category="General", disability=False
        ),
        matches=[],
        checklist=[],
        application_draft=None,
        rejected_matches=[],
    )

    result_state = agent.run(state=state)

    assert result_state.get("explanation") is not None
    assert "couldn't find any schemes" in result_state["explanation"]
    assert "guidance only" in result_state["explanation"]


def test_explainer_includes_disclaimer_callback():
    # Test the callback directly
    from app.agents.explainer import inject_disclaimer_callback

    class MockOutput:
        def __init__(self, text):
            self.text = text

    # Assuming output is dict
    output = {"text": "This is a summary."}
    result = inject_disclaimer_callback(None, output)

    assert "This is a summary." in result["text"]
    assert "Disclaimer:" in result["text"]
    assert "guidance only" in result["text"]
