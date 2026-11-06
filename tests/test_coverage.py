"""Coverage: the connector serves every upstream tool with a typed schema.

Starts a fixture upstream over streamable HTTP, points the connector at it and
lists the served tools. Set ``CLOUDFLARE_COVERAGE_LIVE_URL`` to run the same check
against a live upstream.
"""

import asyncio
import os
import socket

from fastmcp import Client, FastMCP


def _fixture_upstream() -> FastMCP:
    upstream = FastMCP("fixture")

    @upstream.tool
    def get_items(item_id: str) -> dict:
        """Read one item."""
        return {"id": item_id}

    @upstream.tool
    def post_items(name: str) -> dict:
        """Create an item."""
        return {"name": name}

    return upstream


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _typed(schema: dict) -> bool:
    if schema.get("type") != "object":
        return False
    return all(
        any(key in prop for key in ("type", "anyOf", "oneOf", "$ref", "enum"))
        for prop in (schema.get("properties") or {}).values()
    )


async def _served_tools(url: str):
    import importlib

    build_server = importlib.import_module("scion_sdk.connector").build_server
    upstreams = importlib.import_module("cloudflare_mcp.upstreams")

    os.environ[upstreams.URL_SETTING] = url
    importlib.reload(upstreams)
    import cloudflare_mcp

    importlib.reload(cloudflare_mcp)
    _, server = build_server("cloudflare_mcp", command_args=[])
    async with Client(server) as client:
        return await client.list_tools()


async def _test_served_tools_cover_upstream_with_typed_schemas(monkeypatch):
    monkeypatch.setenv("CLOUDFLARE_TOKEN", "unit-test")
    live = os.environ.get("CLOUDFLARE_COVERAGE_LIVE_URL")
    if live:
        url, upstream_count, task = live, None, None
    else:
        port = _free_port()
        upstream = _fixture_upstream()
        task = asyncio.create_task(
            upstream.run_http_async(host="127.0.0.1", port=port, show_banner=False)
        )
        await asyncio.sleep(1.5)
        url, upstream_count = f"http://127.0.0.1:{port}/mcp", 2
    try:
        from cloudflare_mcp.upstreams import NAMESPACE

        served = [
            t for t in await _served_tools(url) if t.name.startswith(f"{NAMESPACE}_")
        ]
        if upstream_count is not None:
            assert len(served) >= upstream_count
        assert served
        assert all(_typed(tool.inputSchema) for tool in served)
    finally:
        if task is not None:
            task.cancel()


def test_served_tools_cover_upstream_with_typed_schemas(monkeypatch):
    asyncio.run(_test_served_tools_cover_upstream_with_typed_schemas(monkeypatch))
