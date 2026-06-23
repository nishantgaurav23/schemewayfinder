import json
import pytest
from app.agents.contracts import SessionState, CHECKLIST_KEY
from app.models.schemes import MatchResult
from app.agents.documents import create_document_agent


@pytest.fixture
def mock_get_scheme(monkeypatch):
    """Mock the get_scheme MCP tool or local lookup."""

    def _mock_get_scheme(scheme_id: str):
        if scheme_id == "scheme_1":
            return json.dumps(
                {
                    "id": "scheme_1",
                    "name": "Scheme 1",
                    "level": "central",
                    "eligibility_rules": [],
                    "required_documents": [
                        "Aadhaar Card",
                        "Income Certificate",
                        "Passport Size Photo",
                    ],
                }
            )
        elif scheme_id == "scheme_2":
            return json.dumps(
                {
                    "id": "scheme_2",
                    "name": "Scheme 2",
                    "level": "state",
                    "eligibility_rules": [],
                    "required_documents": ["Aadhaar Card", "Bank Passbook"],
                }
            )
        elif scheme_id == "scheme_fail":
            return json.dumps({"error": "Not found"})
        return json.dumps({"error": "Unknown"})

    monkeypatch.setattr("app.agents.documents.get_scheme_impl", _mock_get_scheme)


def test_document_checklist_success(mock_get_scheme):
    agent = create_document_agent()
    state = SessionState(
        matches=[
            MatchResult(
                scheme_id="scheme_1",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            ),
            MatchResult(
                scheme_id="scheme_2",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            ),
        ]
    )

    result_state = agent.run(state.model_dump())

    assert CHECKLIST_KEY in result_state
    checklist = result_state[CHECKLIST_KEY]

    # Check deduplication
    assert len(checklist) == 4
    assert "Aadhaar Card" in checklist
    assert "Income Certificate" in checklist
    assert "Passport Size Photo" in checklist
    assert "Bank Passbook" in checklist


def test_document_checklist_empty_matches():
    agent = create_document_agent()
    state = SessionState(matches=[])

    result_state = agent.run(state.model_dump())

    assert CHECKLIST_KEY in result_state
    assert result_state[CHECKLIST_KEY] == []


def test_document_checklist_handles_tool_failure(mock_get_scheme):
    agent = create_document_agent()
    state = SessionState(
        matches=[
            MatchResult(
                scheme_id="scheme_1",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            ),
            MatchResult(
                scheme_id="scheme_fail",
                is_eligible=True,
                matched_rules=[],
                failed_rules=[],
                overall_score=1.0,
            ),
        ]
    )

    result_state = agent.run(state.model_dump())

    assert CHECKLIST_KEY in result_state
    checklist = result_state[CHECKLIST_KEY]

    # Should contain only scheme_1 documents and gracefully handle scheme_fail
    assert len(checklist) == 3
    assert "Aadhaar Card" in checklist
    assert "Income Certificate" in checklist
    assert "Passport Size Photo" in checklist
