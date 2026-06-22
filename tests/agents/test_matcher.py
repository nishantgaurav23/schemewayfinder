import pytest
from unittest.mock import patch

from app.agents.matcher import EligibilityMatcherAgent
from app.models.schemes import CitizenProfile, MatchResult
from app.agents.contracts import SessionState


@pytest.fixture
def mock_session():
    class MockContext:
        def __init__(self):
            self.state = SessionState()

    return MockContext()


@pytest.fixture
def citizen_profile():
    return CitizenProfile(
        age=30,
        income=40000,
        state="Karnataka",
        category="General",
        disability=False,
        occupation="Farmer",
    )


def dummy_match_result(scheme_id: str, score: float) -> MatchResult:
    return MatchResult(
        scheme_id=scheme_id,
        is_eligible=(score == 1.0),
        matched_rules=[],
        failed_rules=[],
        overall_score=score,
    )


@patch("app.agents.matcher.CentralMatcherAgent.run")
@patch("app.agents.matcher.StateMatcherAgent.run")
def test_matcher_success_parallel(mock_state_run, mock_central_run, mock_session, citizen_profile):
    mock_session.state.citizen_profile = citizen_profile

    # Mock return values for sub-agents
    mock_central_run.return_value = [dummy_match_result("c1", 1.0), dummy_match_result("c2", 0.8)]
    mock_state_run.return_value = [
        dummy_match_result("s1", 1.0),
        dummy_match_result(
            "c2", 0.9
        ),  # Duplicate scheme but higher score from state (unlikely but possible)
    ]

    agent = EligibilityMatcherAgent()
    agent.run(node_input=None, ctx=mock_session)

    matches = mock_session.state.matches
    assert len(matches) == 3
    # Check deduplication and ranking by overall_score descending
    assert matches[0].scheme_id in ["c1", "s1"]
    assert matches[1].scheme_id in ["c1", "s1"]
    assert matches[2].scheme_id == "c2"
    assert matches[2].overall_score == 0.9  # Took the higher score


@patch("app.agents.matcher.CentralMatcherAgent.run")
@patch("app.agents.matcher.StateMatcherAgent.run")
def test_matcher_no_state_provided(mock_state_run, mock_central_run, mock_session):
    # State is practically required by CitizenProfile, but hypothetically if not provided or empty string
    profile = CitizenProfile(age=30, income=40000, state="", category="General", disability=False)
    mock_session.state.citizen_profile = profile

    mock_central_run.return_value = [dummy_match_result("c1", 1.0)]
    mock_state_run.return_value = []

    agent = EligibilityMatcherAgent()
    agent.run(node_input=None, ctx=mock_session)

    matches = mock_session.state.matches
    assert len(matches) == 1
    assert matches[0].scheme_id == "c1"
    # The state agent shouldn't have been called or should return early
    # (Implementation detail: we'll handle this in StateMatcherAgent run wrapper or instructions)


@patch("app.agents.matcher.CentralMatcherAgent.run")
@patch("app.agents.matcher.StateMatcherAgent.run")
def test_matcher_empty_results(mock_state_run, mock_central_run, mock_session, citizen_profile):
    mock_session.state.citizen_profile = citizen_profile
    mock_central_run.return_value = []
    mock_state_run.return_value = []

    agent = EligibilityMatcherAgent()
    agent.run(node_input=None, ctx=mock_session)

    matches = mock_session.state.matches
    assert len(matches) == 0


@patch("app.agents.matcher.CentralMatcherAgent.run")
@patch("app.agents.matcher.StateMatcherAgent.run")
def test_matcher_tool_failure_handling(
    mock_state_run, mock_central_run, mock_session, citizen_profile
):
    mock_session.state.citizen_profile = citizen_profile

    # Simulate one failing completely despite retries
    mock_central_run.side_effect = Exception("API completely failed")
    mock_state_run.return_value = [dummy_match_result("s1", 1.0)]

    agent = EligibilityMatcherAgent()

    # ParallelAgent usually bubbles up exceptions unless caught. Let's assume our matcher catches or lets it bubble?
    # Spec says "Handling of sub-agent or tool execution errors gracefully (e.g., retries or returning partial results)."
    # We will implement graceful degradation where if one fails, we at least return the other's matches.
    agent.run(node_input=None, ctx=mock_session)

    matches = mock_session.state.matches
    assert len(matches) == 1
    assert matches[0].scheme_id == "s1"
