import pytest
from unittest.mock import patch
from pydantic import ValidationError
from tenacity import RetryError

from app.agents.intake import IntakeAgent
from app.models.schemes import CitizenProfile
from app.agents.contracts import SessionState


@pytest.fixture
def mock_session():
    class MockContext:
        def __init__(self):
            self.state = SessionState()

    return MockContext()


@pytest.fixture
def intake_agent():
    return IntakeAgent()


def mock_super_run_success(profile):
    def side_effect(*args, ctx=None, **kwargs):
        if ctx:
            ctx.state.citizen_profile = profile
        return profile

    return side_effect


@patch("app.agents.intake.LlmAgent.run")
def test_intake_success(mock_llm_call, intake_agent, mock_session):
    profile = CitizenProfile(
        age=35,
        income=50000.0,
        state="Maharashtra",
        category="General",
        disability=False,
        occupation="Farmer",
    )
    mock_llm_call.side_effect = mock_super_run_success(profile)

    intake_agent.run(
        node_input="I am a 35 year old farmer from Maharashtra earning 50k", ctx=mock_session
    )

    assert mock_session.state.citizen_profile is not None
    assert mock_session.state.citizen_profile.age == 35
    assert mock_session.state.citizen_profile.occupation == "Farmer"


@patch("app.agents.intake.LlmAgent.run")
def test_intake_invalid_values(mock_llm_call, intake_agent, mock_session):
    mock_llm_call.side_effect = ValidationError.from_exception_data("age", [])

    with pytest.raises(Exception):
        intake_agent.run(node_input="I am -5 years old", ctx=mock_session)


@patch("app.agents.intake.LlmAgent.run")
def test_intake_missing_fields_defaults(mock_llm_call, intake_agent, mock_session):
    profile = CitizenProfile(
        age=20, income=0.0, state="Delhi", category="General", disability=False
    )
    mock_llm_call.side_effect = mock_super_run_success(profile)

    intake_agent.run(node_input="I'm a 20 year old from Delhi with no income", ctx=mock_session)

    assert mock_session.state.citizen_profile.disability is False
    assert mock_session.state.citizen_profile.category == "General"


@patch("app.agents.intake.LlmAgent.run")
def test_intake_retries_on_failure(mock_llm_call, intake_agent, mock_session):
    mock_llm_call.side_effect = Exception("API Error")

    with pytest.raises(RetryError):
        intake_agent.run(node_input="Will fail 3 times", ctx=mock_session)

    assert mock_llm_call.call_count == 3


def test_intake_logging_no_pii(caplog, intake_agent, mock_session):
    profile = CitizenProfile(
        age=35, income=50000.0, state="Maharashtra", category="General", disability=False
    )
    with patch("app.agents.intake.LlmAgent.run") as mock_llm_call:
        mock_llm_call.side_effect = mock_super_run_success(profile)

        secret_pii = "My name is John Doe and my phone is 555-1234"
        intake_agent.run(node_input=secret_pii, ctx=mock_session)

        for record in caplog.records:
            assert secret_pii not in record.message
