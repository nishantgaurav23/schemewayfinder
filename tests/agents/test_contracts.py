import pytest
from pydantic import ValidationError


def test_session_state_defaults():
    from app.agents.contracts import SessionState

    state = SessionState()
    assert state.citizen_profile is None
    assert state.matches == []
    assert state.checklist == []
    assert state.application_draft is None
    assert state.rejection_risk_audit is None
    assert state.explanation is None


def test_session_state_validation():
    from app.agents.contracts import SessionState

    # If we pass an invalid type, Pydantic should raise ValidationError
    with pytest.raises(ValidationError):
        SessionState(citizen_profile="invalid_profile_type")
