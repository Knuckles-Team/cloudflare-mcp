"""The declared upstream surface lists the provider's published tools (CONN-CLOUDFLARE-MCP-R016)."""

import pytest

from cloudflare_mcp.connector_contracts import CONTRACTS, LINKS, UPSTREAM_TOOLS

pytestmark = pytest.mark.spec("CONN-CLOUDFLARE-MCP-R016")


def test_declared_upstream_tools_match_the_published_list() -> None:
    assert {t.name for t in UPSTREAM_TOOLS} == {
        "cloudflare_search",
        "cloudflare_execute",
        "cloudflare_docs",
        "cloudflare_whoami",
    }
    assert {t.name for t in UPSTREAM_TOOLS if t.destructive} == {"cloudflare_execute"}
    for tool in UPSTREAM_TOOLS:
        assert tool.description and tool.input_schema["type"] == "object"


def test_every_declared_tool_is_called_by_a_contract_and_linked() -> None:
    declared = {t.name for t in UPSTREAM_TOOLS}
    called = {s.tool for c in CONTRACTS for s in c.steps}
    linked = {t for link in LINKS for t in link.tools}
    assert declared == called == linked
