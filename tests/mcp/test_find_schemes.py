from unittest.mock import MagicMock, patch
import pytest
from app.models.schemes import Scheme, EligibilityRule


@pytest.mark.asyncio
@patch("app.mcp.scheme_search.tools.SchemeIndex")
async def test_find_schemes_fully_eligible(mock_index_class):
    # Setup mock index
    mock_index = MagicMock()
    mock_index_class.return_value = mock_index

    # Setup candidate schemes
    rule1 = EligibilityRule(field="age", operator=">=", value=18, explanation="Must be 18 or older")
    rule2 = EligibilityRule(
        field="income", operator="<=", value=100000.0, explanation="Income must be 1 Lakh or less"
    )
    scheme = Scheme(
        id="pm-kisan",
        name="PM Kisan",
        description="Farming support",
        level="central",
        eligibility_rules=[rule1, rule2],
        required_documents=["Aadhaar", "Land Records"],
    )

    # Mock search result to return candidate schemes with score
    mock_index.search.return_value = [(scheme, 0.9)]

    # Import the tool handler from tools.py
    from app.mcp.scheme_search.tools import find_schemes

    profile_dict = {
        "age": 25,
        "income": 50000.0,
        "state": "Karnataka",
        "category": "General",
        "disability": False,
        "occupation": "Farmer",
    }

    # Run tool handler
    results_json = await find_schemes(profile_dict)

    # Parse back the return string (since MCP tools return string representations, usually JSON or text)
    # Let's ensure the tool returns a JSON list of MatchResult dicts or raw Pydantic representations
    import json

    results = json.loads(results_json)

    assert len(results) == 1
    res = results[0]
    assert res["scheme_id"] == "pm-kisan"
    assert res["is_eligible"] is True
    assert res["overall_score"] == 1.0
    assert len(res["matched_rules"]) == 2
    assert len(res["failed_rules"]) == 0


@pytest.mark.asyncio
@patch("app.mcp.scheme_search.tools.SchemeIndex")
async def test_find_schemes_ineligible_rule(mock_index_class):
    mock_index = MagicMock()
    mock_index_class.return_value = mock_index

    rule1 = EligibilityRule(field="age", operator=">=", value=18, explanation="Must be 18 or older")
    scheme = Scheme(
        id="pm-kisan",
        name="PM Kisan",
        description="Farming support",
        level="central",
        eligibility_rules=[rule1],
        required_documents=[],
    )

    mock_index.search.return_value = [(scheme, 0.95)]

    from app.mcp.scheme_search.tools import find_schemes

    # Profile age is 16 (fails >= 18)
    profile_dict = {
        "age": 16,
        "income": 50000.0,
        "state": "Karnataka",
        "category": "General",
        "disability": False,
    }

    results_json = await find_schemes(profile_dict)

    import json

    results = json.loads(results_json)

    assert len(results) == 1
    res = results[0]
    assert res["scheme_id"] == "pm-kisan"
    assert res["is_eligible"] is False
    assert res["overall_score"] == 0.0
    assert len(res["matched_rules"]) == 0
    assert len(res["failed_rules"]) == 1
    assert res["failed_rules"][0]["field"] == "age"
