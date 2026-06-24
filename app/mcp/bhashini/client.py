import os
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool import SseConnectionParams


class BhashiniClient:
    def __init__(self, endpoint_url: str = None, api_key: str = None):
        self.endpoint_url = endpoint_url or os.getenv(
            "BHASHINI_ENDPOINT_URL", "http://mock-bhashini"
        )
        self.api_key = api_key or os.getenv("BHASHINI_API_KEY", "mock-key")
        self.toolset = None

    def initialize(self):
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        params = SseConnectionParams(url=self.endpoint_url, headers=headers)
        self.toolset = McpToolset(connection_params=params)

    async def _get_tool(self, name: str):
        if not self.toolset:
            self.initialize()
        tools = await self.toolset.get_tools()
        for t in tools:
            if t.name == name:
                return t
        raise ValueError(f"Tool {name} not found in Bhashini MCP toolset")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def asr(self, audio_data: bytes, source_language: str):
        tool = await self._get_tool("asr")
        return await asyncio.wait_for(
            tool(audio_data=audio_data, source_language=source_language), timeout=30.0
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def nmt(self, text: str, source_language: str, target_language: str):
        tool = await self._get_tool("nmt")
        return await asyncio.wait_for(
            tool(text=text, source_language=source_language, target_language=target_language),
            timeout=15.0,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def tts(self, text: str, target_language: str):
        tool = await self._get_tool("tts")
        return await asyncio.wait_for(
            tool(text=text, target_language=target_language), timeout=30.0
        )
