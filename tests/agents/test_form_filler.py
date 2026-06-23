import json
import pytest
from app.agents.contracts import SessionState, DRAFT_KEY
from app.models.schemes import CitizenProfile, MatchResult
from app.agents.form_filler import create_form_filler_agent


@pytest.fixture
def mock_get_scheme(monkeypatch):
    def _mock_get_scheme(scheme_id: str):
        if scheme_id == "scheme_1":
            return json.dumps(
                {
                    "id": "scheme_1",
                    "name": "PM Kisan Samman Nidhi",
                    "apply_url": "https://pmkisan.gov.in/",
                }
            )
        elif scheme_id == "scheme_2":
            return json.dumps(
                {
                    "id": "scheme_2",
                    "name": "State Pension",
                    "apply_url": "https://pension.state.gov.in/",
                }
            )
        return json.dumps({"error": "Unknown"})

    monkeypatch.setattr("app.agents.form_filler.get_scheme_impl", _mock_get_scheme)


def test_form_filler_success(mock_get_scheme):
    agent = create_form_filler_agent()
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
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            )
        ],
    )

    result_state = agent.run(state.model_dump())

    assert DRAFT_KEY in result_state
    draft = result_state[DRAFT_KEY]

    assert "PM Kisan Samman Nidhi" in draft
    assert "30" in draft
    assert "150000" in draft
    assert "Karnataka" in draft
    assert "OBC" in draft
    assert "Farmer" in draft
    assert "https://pmkisan.gov.in/" in draft


def test_form_filler_empty_matches(mock_get_scheme):
    agent = create_form_filler_agent()
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=30, income=200000.0, state="Karnataka", category="General", disability=False
        ),
        matches=[],
    )

    result_state = agent.run(state.model_dump())

    assert DRAFT_KEY in result_state
    draft = result_state[DRAFT_KEY]
    assert draft == "" or "No applications" in draft or len(draft.strip()) == 0


def test_form_filler_missing_fields(mock_get_scheme):
    agent = create_form_filler_agent()
    # Missing occupation and category
    state = SessionState(
        citizen_profile=CitizenProfile(
            age=25, income=50000.0, state="Bihar", category="SC", disability=True
        ),
        matches=[
            MatchResult(
                scheme_id="scheme_2",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            )
        ],
    )

    result_state = agent.run(state.model_dump())

    assert DRAFT_KEY in result_state
    draft = result_state[DRAFT_KEY]

    assert "State Pension" in draft
    assert "25" in draft
    assert "50000" in draft
    assert "Bihar" in draft
    assert "occupation" in draft.lower() or "category" in draft.lower()
    assert "https://pension.state.gov.in/" in draft
