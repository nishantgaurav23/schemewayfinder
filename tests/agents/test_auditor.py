import pytest
from unittest.mock import patch
from app.agents.contracts import SessionState, MATCHES_KEY, REJECTED_MATCHES_KEY
from app.models.schemes import CitizenProfile, MatchResult, EligibilityRule
from app.agents.auditor import create_auditor_agent, AuditorOutput


@pytest.fixture
def mock_session():
    class MockContext:
        def __init__(self):
            self.state = SessionState()

    return MockContext()


@patch("app.agents.auditor.LlmAgent.run")
def test_auditor_pass(mock_llm_call):
    mock_llm_call.return_value = {
        "structured_output": AuditorOutput(rejected_scheme_ids=[], reasons={}, continue_loop=False)
    }

    agent = create_auditor_agent()
    # A valid profile and a match that perfectly aligns
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=30,
            income=150000.0,
            state="Karnataka",
            category="OBC",
            disability=False,
            occupation="Farmer",
        ),
        matches=[
            MatchResult(
                scheme_id="scheme_1",
                is_eligible=True,
                matched_rules=[
                    EligibilityRule(
                        field="occupation", operator="==", value="Farmer", explanation=""
                    )
                ],
                failed_rules=[],
                overall_score=1.0,
            )
        ],
    )

    result_state = agent.run(state=state)

    # Match should survive
    assert len(result_state[MATCHES_KEY]) == 1
    assert len(result_state.get(REJECTED_MATCHES_KEY, [])) == 0


@patch("app.agents.auditor.LlmAgent.run")
def test_auditor_reject_hallucination(mock_llm_call):
    mock_llm_call.return_value = {
        "structured_output": AuditorOutput(
            rejected_scheme_ids=["scheme_2"],
            reasons={"scheme_2": "Violates age constraint"},
            continue_loop=False,
        )
    }

    agent = create_auditor_agent()
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=25, income=50000.0, state="Bihar", category="General", disability=False
        ),
        matches=[
            MatchResult(
                scheme_id="scheme_2",
                is_eligible=True,  # Erroneously marked as eligible
                matched_rules=[
                    EligibilityRule(field="age", operator=">=", value=60, explanation="")
                ],
                failed_rules=[],
                overall_score=1.0,
            )
        ],
    )

    result_state = agent.run(state=state)

    # Match should be removed and added to rejected matches
    assert len(result_state[MATCHES_KEY]) == 0
    assert len(result_state[REJECTED_MATCHES_KEY]) == 1
    rejected = result_state[REJECTED_MATCHES_KEY][0]
    assert rejected["scheme_id"] == "scheme_2"
    assert "reason" in rejected


@patch("app.agents.auditor.LlmAgent.run")
def test_auditor_max_iterations(mock_llm_call):
    # Make the agent infinitely want to continue
    mock_llm_call.return_value = {
        "structured_output": AuditorOutput(
            rejected_scheme_ids=["scheme_invalid"],
            reasons={"scheme_invalid": "Invalid match"},
            continue_loop=True,
        )
    }

    agent = create_auditor_agent()
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=25, income=50000.0, state="Bihar", category="General", disability=False
        ),
        matches=[
            MatchResult(
                scheme_id="scheme_valid",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            ),
            MatchResult(
                scheme_id="scheme_invalid",
                is_eligible=True,
                matched_rules=[
                    EligibilityRule(field="age", operator=">=", value=60, explanation="")
                ],
                failed_rules=[],
                overall_score=1.0,
            ),
        ],
    )

    result_state = agent.run(state=state)

    # It should have looped max_iterations times (2)
    assert mock_llm_call.call_count == 2
    assert len(result_state[MATCHES_KEY]) == 1
    assert result_state[MATCHES_KEY][0]["scheme_id"] == "scheme_valid"
    assert len(result_state[REJECTED_MATCHES_KEY]) == 1
    assert result_state[REJECTED_MATCHES_KEY][0]["scheme_id"] == "scheme_invalid"
