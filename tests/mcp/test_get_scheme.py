from unittest.mock import patch
import pytest
import json
from app.models.schemes import Scheme, EligibilityRule


@pytest.mark.asyncio
@patch("app.mcp.scheme_search.tools.get_all_schemes")
async def test_get_scheme_success(mock_get_all_schemes):
    # Setup mock scheme
    rule = EligibilityRule(field="age", operator=">=", value=18, explanation="Must be 18 or older")
    scheme = Scheme(
        id="pm-kisan",
        name="PM Kisan",
        description="Farming support",
        level="central",
        eligibility_rules=[rule],
        required_documents=["Aadhaar"],
        apply_url="https://pmkisan.gov.in",
    )
    mock_get_all_schemes.return_value = [scheme]

    from app.mcp.scheme_search.tools import get_scheme

    # Run tool handler
    res_json = await get_scheme("pm-kisan")
    res = json.loads(res_json)

    assert res["id"] == "pm-kisan"
    assert res["name"] == "PM Kisan"
    assert res["description"] == "Farming support"
    assert len(res["eligibility_rules"]) == 1
    assert res["eligibility_rules"][0]["field"] == "age"
    assert res["required_documents"] == ["Aadhaar"]
    assert res["apply_url"] == "https://pmkisan.gov.in"


@pytest.mark.asyncio
@patch("app.mcp.scheme_search.tools.get_all_schemes")
async def test_get_scheme_not_found(mock_get_all_schemes):
    mock_get_all_schemes.return_value = []

    from app.mcp.scheme_search.tools import get_scheme

    # Run tool handler with non-existent ID
    res_json = await get_scheme("invalid-id")
    res = json.loads(res_json)

    assert "error" in res
    assert "not found" in res["error"].lower()
