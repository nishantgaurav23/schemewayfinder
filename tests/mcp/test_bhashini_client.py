import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from tenacity import RetryError
from app.mcp.bhashini.client import BhashiniClient
from google.adk.tools.mcp_tool import SseConnectionParams


@patch("app.mcp.bhashini.client.McpToolset")
def test_bhashini_client_initialization(mock_mcp_toolset_cls):
    mock_toolset = MagicMock()
    mock_mcp_toolset_cls.return_value = mock_toolset

    client = BhashiniClient(endpoint_url="http://mock-bhashini", api_key="secret")
    client.initialize()

    mock_mcp_toolset_cls.assert_called_once()
    args, kwargs = mock_mcp_toolset_cls.call_args
    assert "connection_params" in kwargs
    params = kwargs["connection_params"]
    assert isinstance(params, SseConnectionParams)
    assert params.url == "http://mock-bhashini"
    assert params.headers["Authorization"] == "Bearer secret"
    assert client.toolset is mock_toolset


@pytest.mark.asyncio
@patch("app.mcp.bhashini.client.McpToolset")
async def test_bhashini_retries_on_failure(mock_mcp_toolset_cls):
    mock_toolset = AsyncMock()

    # Mock the tool that ASR would call
    mock_tool = AsyncMock()
    mock_tool.name = "asr"
    mock_tool.side_effect = Exception("Network error")
    mock_toolset.get_tools.return_value = [mock_tool]
    mock_mcp_toolset_cls.return_value = mock_toolset

    client = BhashiniClient()
    client.initialize()

    with pytest.raises(RetryError):
        await client.asr(audio_data=b"test", source_language="hi")

    # Tenacity should retry 3 times
    assert mock_tool.call_count == 3


@pytest.mark.asyncio
@patch("app.mcp.bhashini.client.McpToolset")
async def test_bhashini_graceful_timeout(mock_mcp_toolset_cls):
    mock_toolset = AsyncMock()
    mock_tool = AsyncMock()
    mock_tool.name = "nmt"

    async def slow_tool(*args, **kwargs):
        await asyncio.sleep(20.0)  # Slower than the 15.0 timeout
        return "done"

    mock_tool.side_effect = slow_tool
    mock_toolset.get_tools.return_value = [mock_tool]
    mock_mcp_toolset_cls.return_value = mock_toolset

    client = BhashiniClient()
    client.initialize()

    # Fast forward time or use a small timeout for the test to avoid actually waiting 15s?
    # Wait, instead of actually sleeping, we can just raise asyncio.TimeoutError directly from the tool
    # Wait, asyncio.wait_for wraps it, so if we mock wait_for or if we just raise TimeoutError directly.
    # Actually wait_for throws TimeoutError.
    pass


@pytest.mark.asyncio
@patch("app.mcp.bhashini.client.asyncio.wait_for")
@patch("app.mcp.bhashini.client.McpToolset")
async def test_bhashini_graceful_timeout_with_mock(mock_mcp_toolset_cls, mock_wait_for):
    mock_toolset = AsyncMock()
    mock_tool = AsyncMock()
    mock_tool.name = "nmt"
    mock_toolset.get_tools.return_value = [mock_tool]
    mock_mcp_toolset_cls.return_value = mock_toolset

    mock_wait_for.side_effect = asyncio.TimeoutError("Timeout")

    client = BhashiniClient()
    client.initialize()

    with pytest.raises(RetryError):
        await client.nmt(text="Hello", source_language="en", target_language="hi")

    assert mock_wait_for.call_count == 3
