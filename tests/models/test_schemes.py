import pytest
from pydantic import ValidationError
from app.models.schemes import EligibilityRule, Scheme, CitizenProfile, MatchResult


def test_eligibility_rule_validation():
    # Valid operators should work
    for op in [">=", "<=", "==", "in", "contains"]:
        rule = EligibilityRule(
            field="age", operator=op, value=18, explanation=f"Age must be {op} 18"
        )
        assert rule.operator == op

    # Invalid operator should raise ValidationError
    with pytest.raises(ValidationError):
        EligibilityRule(
            field="age", operator="invalid_operator", value=18, explanation="This should fail"
        )


def test_scheme_state_validation():
    # Central scheme with no state should pass
    central = Scheme(
        id="pm-kisan",
        name="PM Kisan",
        description="Central landholder scheme",
        level="central",
        eligibility_rules=[],
        required_documents=[],
        apply_url="https://pmkisan.gov.in",
    )
    assert central.level == "central"
    assert central.state is None

    # State scheme with a state should pass
    state_scheme = Scheme(
        id="rythu-bandhu",
        name="Rythu Bandhu",
        description="Telangana scheme",
        level="state",
        state="Telangana",
        eligibility_rules=[],
        required_documents=[],
        apply_url=None,
    )
    assert state_scheme.level == "state"
    assert state_scheme.state == "Telangana"

    # State scheme missing state should raise ValidationError
    with pytest.raises(ValidationError):
        Scheme(
            id="rythu-bandhu",
            name="Rythu Bandhu",
            description="Telangana scheme",
            level="state",
            state=None,
            eligibility_rules=[],
            required_documents=[],
        )

    # Central scheme with state should raise ValidationError
    with pytest.raises(ValidationError):
        Scheme(
            id="pm-kisan",
            name="PM Kisan",
            description="Central scheme with state",
            level="central",
            state="Telangana",
            eligibility_rules=[],
            required_documents=[],
        )


def test_citizen_profile_bounds():
    # Valid profile should pass
    profile = CitizenProfile(
        age=25,
        income=50000.0,
        state="Karnataka",
        category="General",
        disability=False,
        occupation="Farmer",
    )
    assert profile.age == 25
    assert profile.income == 50000.0

    # Age <= 0 should raise ValidationError
    with pytest.raises(ValidationError):
        CitizenProfile(
            age=0, income=50000.0, state="Karnataka", category="General", disability=False
        )

    with pytest.raises(ValidationError):
        CitizenProfile(
            age=-5, income=50000.0, state="Karnataka", category="General", disability=False
        )

    # Income < 0 should raise ValidationError
    with pytest.raises(ValidationError):
        CitizenProfile(age=25, income=-1.0, state="Karnataka", category="General", disability=False)


def test_match_result_score_bounds():
    # Valid match result should pass
    match = MatchResult(
        scheme_id="pm-kisan",
        is_eligible=True,
        matched_rules=[],
        failed_rules=[],
        overall_score=0.85,
    )
    assert match.overall_score == 0.85

    # overall_score < 0 should raise ValidationError
    with pytest.raises(ValidationError):
        MatchResult(
            scheme_id="pm-kisan",
            is_eligible=True,
            matched_rules=[],
            failed_rules=[],
            overall_score=-0.1,
        )

    # overall_score > 1 should raise ValidationError
    with pytest.raises(ValidationError):
        MatchResult(
            scheme_id="pm-kisan",
            is_eligible=True,
            matched_rules=[],
            failed_rules=[],
            overall_score=1.05,
        )
