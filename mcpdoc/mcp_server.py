"""A server for just MCP docs from modelcontextprotocol.io.

This is used as a way to test the doc functionality via MCP.
"""

# /usr/bin/env python3
import httpx
from markdownify import markdownify
from mcp.server.fastmcp import FastMCP

server = FastMCP(name="mcp-docs")

ALLOWED_PREFIX = "https://modelcontextprotocol.io/"

HTTPX_CLIENT = httpx.AsyncClient(follow_redirects=False)


@server.tool()
async def get_docs(url: str = "overview") -> str:
    """Get MCP docs.

    Always fetch the `overview` prior to fetching any other URLs as it will provide a
    list of available URLs.

    Args:
        url: The URL to fetch. Must start with https://modelcontextprotocol.io/
        or be "overview".
    """
    if url == "overview":
        url = "https://modelcontextprotocol.io/llms.txt"

    if not url.startswith(ALLOWED_PREFIX):
        return (
            "Error: Invalid url. Must start with https://modelcontextprotocol.io/ "
            'or be "overview"'
        )

    response = await HTTPX_CLIENT.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        # Convert HTML to markdown
        markdown_content = markdownify(response.text)
        return markdown_content
    else:
        return "Encountered an error while fetching the URL."


if __name__ == "__main__":
    server.run(transport="stdio")
