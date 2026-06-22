from unittest.mock import patch
import pytest
import json
from app.mcp.scheme_search.server import mcp
from app.data.index import SchemeIndex


@pytest.mark.asyncio
@patch("app.data.index.generate_embeddings")
async def test_mcp_client_find_schemes_integration(mock_embed, tmp_path):
    # Mock generate_embeddings to handle both str and list of str offline
    def mock_emb(texts):
        if isinstance(texts, str):
            return [0.1] * 768
        return [[0.1] * 768 for _ in texts]

    mock_embed.side_effect = mock_emb

    # Override the cache path of SchemeIndex to a temp file
    temp_cache = tmp_path / "temp_embeddings_cache.json"
    original_init = SchemeIndex.__init__

    with patch.object(
        SchemeIndex,
        "__init__",
        lambda self, *args, **kwargs: original_init(self, cache_path=str(temp_cache)),
    ):
        tools = await mcp.list_tools()
        find_schemes_tool = [t for t in tools if t.name == "find_schemes"][0]

        profile = {
            "age": 30,
            "income": 50000.0,
            "state": "Karnataka",
            "category": "General",
            "disability": False,
            "occupation": "Farmer",
        }

        res_json = await find_schemes_tool.fn(profile)
        res = json.loads(res_json)

        assert len(res) > 0
        pm_kisan_result = None
        for item in res:
            if item["scheme_id"] == "1":
                pm_kisan_result = item
                break

        assert pm_kisan_result is not None
        assert pm_kisan_result["is_eligible"] is True
        assert pm_kisan_result["overall_score"] == 1.0


@pytest.mark.asyncio
async def test_mcp_client_get_scheme_integration():
    tools = await mcp.list_tools()
    get_scheme_tool = [t for t in tools if t.name == "get_scheme"][0]

    res_json = await get_scheme_tool.fn("1")
    res = json.loads(res_json)

    assert res["id"] == "1"
    assert "Pradhan Mantri" in res["name"] or "Kisan" in res["name"]
    assert res["level"] == "central"
    assert len(res["required_documents"]) > 0

    # Non-existent ID lookup
    res_err_json = await get_scheme_tool.fn("invalid-id")
    res_err = json.loads(res_err_json)
    assert "error" in res_err
