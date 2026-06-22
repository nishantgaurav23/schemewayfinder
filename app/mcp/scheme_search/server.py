import os
from fastmcp import FastMCP

mcp = FastMCP("scheme-search")

# Register tools
import app.mcp.scheme_search.tools  # noqa: F401, E402


@mcp.tool()
def status() -> str:
    """Check the health status of the Scheme-Search MCP server."""
    cache_exists = os.path.exists("app/data/corpus/embeddings_cache.json")
    status_msg = (
        f"Server: Healthy. Embeddings Cache: {'Initialized' if cache_exists else 'Not Found'}."
    )
    return status_msg


if __name__ == "__main__":
    mcp.run()
