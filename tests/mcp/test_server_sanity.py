from fastmcp import FastMCP
import pytest


def test_mcp_instance_creation():
    from app.mcp.scheme_search.server import mcp

    assert isinstance(mcp, FastMCP)
    assert mcp.name == "scheme-search"


@pytest.mark.asyncio
async def test_status_tool_registration():
    from app.mcp.scheme_search.server import mcp

    tools = await mcp.list_tools()
    tool_names = [tool.name for tool in tools]

    assert "status" in tool_names, "Tool 'status' not found on FastMCP server"
    assert "find_schemes" in tool_names, "Tool 'find_schemes' not found on FastMCP server"
    assert "get_scheme" in tool_names, "Tool 'get_scheme' not found on FastMCP server"

    # Call status tool handler directly
    status_tool = [t for t in tools if t.name == "status"][0]
    res = status_tool.fn()
    if hasattr(res, "__await__"):
        res = await res

    assert "healthy" in res.lower() or "health" in res.lower()
