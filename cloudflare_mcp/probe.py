"""Probe the Cloudflare upstream tool list and report drift (exit 1 on drift).

Prints the upstream tool count, the typed-schema count and the SDK fingerprint.
With ``CLOUDFLARE_UPSTREAM_FINGERPRINT`` set, a different fingerprint exits 1.
Writes no file.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys

from fastmcp import Client
from scion_sdk.mcp.upstreams.drift import fingerprint_tools

from .upstreams import FINGERPRINT_SETTING, URL_SETTING


async def _tools(url: str) -> list:
    headers = {}
    token = os.environ.get("CLOUDFLARE_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    from fastmcp.client.transports import StreamableHttpTransport

    async with Client(StreamableHttpTransport(url, headers=headers)) as client:
        return await client.list_tools()


def main() -> int:
    url = os.environ.get(URL_SETTING, "")
    if not url:
        print(json.dumps({"refused": True, "code": "UPSTREAM_URL_UNSET"}))
        return 2
    tools = asyncio.run(_tools(url))
    fingerprint = fingerprint_tools(tools)
    typed = sum(1 for tool in tools if (tool.inputSchema or {}).get("type") == "object")
    expected = os.environ.get(FINGERPRINT_SETTING, "")
    print(json.dumps({"tools": len(tools), "typed": typed, "fingerprint": fingerprint}))
    return 1 if expected and expected != fingerprint else 0


if __name__ == "__main__":
    sys.exit(main())
