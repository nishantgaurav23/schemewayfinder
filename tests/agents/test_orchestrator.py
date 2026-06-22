import pytest
from unittest.mock import patch

from app.agents.orchestrator import create_orchestrator
from app.agents.contracts import SessionState
from app.models.schemes import CitizenProfile


@pytest.fixture
def mock_session():
    class MockContext:
        def __init__(self):
            self.state = SessionState()

    return MockContext()


@pytest.fixture
def orchestrator():
    return create_orchestrator()


@patch("app.agents.orchestrator.LlmAgent.run")
def test_orchestrator_delegates_to_intake_when_profile_empty(mock_run, orchestrator, mock_session):
    # Set up empty session
    mock_session.state.citizen_profile = None

    def mock_routing_logic(*args, ctx=None, **kwargs):
        # Simulate LLM deciding to call IntakeAgent when profile is missing
        if ctx.state.citizen_profile is None:
            # Simulate the tool call
            from app.agents.intake import IntakeAgent

            IntakeAgent().run("user input", ctx=ctx)

    mock_run.side_effect = mock_routing_logic

    # Mock IntakeAgent's LlmAgent.run to populate profile
    with patch("app.agents.intake.LlmAgent.run") as mock_intake_run:

        def mock_intake_side_effect(*args, ctx=None, **kwargs):
            ctx.state.citizen_profile = CitizenProfile(
                age=30,
                income=50000.0,
                state="Maharashtra",
                category="General",
                disability=False,
                occupation="Farmer",
            )

        mock_intake_run.side_effect = mock_intake_side_effect

        orchestrator.run(node_input="Hello", ctx=mock_session)

        # Verify routing populated the profile by routing to IntakeAgent
        assert mock_session.state.citizen_profile is not None


@patch("app.agents.orchestrator.LlmAgent.run")
def test_orchestrator_delegates_to_matcher_when_profile_ready(mock_run, orchestrator, mock_session):
    # Set up complete profile
    mock_session.state.citizen_profile = CitizenProfile(
        age=30,
        income=50000.0,
        state="Maharashtra",
        category="General",
        disability=False,
        occupation="Farmer",
    )

    def mock_routing_logic(*args, ctx=None, **kwargs):
        # Simulate LLM deciding to call EligibilityMatcherAgent when profile is ready
        if ctx.state.citizen_profile is not None:
            from app.agents.matcher import EligibilityMatcherAgent

            EligibilityMatcherAgent().run(node_input=None, ctx=ctx)

    mock_run.side_effect = mock_routing_logic

    with patch("app.agents.matcher.EligibilityMatcherAgent.run") as mock_matcher_run:

        def mock_matcher_side_effect(*args, ctx=None, **kwargs):
            from app.models.schemes import MatchResult

            ctx.state.matches = [
                MatchResult(
                    scheme_id="s1",
                    is_eligible=True,
                    matched_rules=[],
                    failed_rules=[],
                    overall_score=1.0,
                )
            ]

        mock_matcher_run.side_effect = mock_matcher_side_effect

        orchestrator.run(node_input="Check schemes", ctx=mock_session)

        # Verify matcher was invoked and updated matches
        assert len(mock_session.state.matches) == 1
        assert mock_session.state.matches[0].scheme_id == "s1"


@patch("app.agents.orchestrator.LlmAgent.run")
def test_orchestrator_handles_subagent_errors(mock_run, orchestrator, mock_session):
    mock_run.side_effect = Exception("Sub-agent failure")

    with pytest.raises(Exception) as exc_info:
        orchestrator.run(node_input="Fail now", ctx=mock_session)

    assert "Sub-agent failure" in str(exc_info.value)
