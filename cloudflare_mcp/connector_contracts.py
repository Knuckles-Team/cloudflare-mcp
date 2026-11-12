"""Surface contracts of the Cloudflare connector (SCION-CONNECTOR-CONTROL-R916).

The connector proxies the provider's own MCP server, so it registers no tool
offline. ``UPSTREAM_TOOLS`` declares the tools that server publishes, served
as ``cloudflare_<tool>``.

Source of the tool list: the provider's public repository for its MCP server
(``cloudflare/mcp``, README, section "Tools") and the provider's developer
documentation page "Cloudflare's own MCP servers", which list ``search``,
``execute``, ``docs`` and ``whoami`` on ``https://mcp.cloudflare.com/mcp``.
Names, descriptions and the ``code``, ``truncate`` and ``account_id``
parameters are quoted from those pages. The provider publishes no formal JSON
Schema; ``docs`` documents no parameter, so its schema declares none.
``execute`` calls the provider API with any method and is therefore the only
tool declared destructive. Re-check the list with ``cloudflare-mcp-probe``
when the upstream fingerprint changes.
"""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
    UpstreamTool,
)

_CODE = {"type": "string", "description": "JavaScript async function to run."}
_TRUNCATE = {"type": "boolean", "description": "Set false to return the whole result."}

UPSTREAM_TOOLS = (
    UpstreamTool(
        "cloudflare",
        "search",
        "Write JavaScript to query spec.paths and find endpoints",
        {"type": "object", "properties": {"code": _CODE, "truncate": _TRUNCATE}, "required": ["code"]},
        False,
    ),
    UpstreamTool(
        "cloudflare",
        "execute",
        "Write JavaScript to call cloudflare.request() with the discovered endpoints",
        {
            "type": "object",
            "properties": {
                "code": _CODE,
                "account_id": {"type": "string", "description": "Account id; omitted with an account token."},
                "truncate": _TRUNCATE,
            },
            "required": ["code"],
        },
        True,
    ),
    UpstreamTool(
        "cloudflare",
        "docs",
        "Search Cloudflare developer documentation",
        {"type": "object", "properties": {}},
        False,
    ),
    UpstreamTool(
        "cloudflare",
        "whoami",
        "Return the Cloudflare user or account this connection is authenticated as",
        {"type": "object", "properties": {}},
        False,
    ),
)

CONTRACTS = (
    ToolUseContract(
        "operate-cloudflare",
        (
            ToolStep("cloudflare_whoami", (), ("id", "name")),
            ToolStep("cloudflare_search", ("code",), ("endpoints",)),
            ToolStep(
                "cloudflare_execute",
                ("code", "account_id"),
                ("result",),
                (
                    Refusal("WRITE_NOT_APPROVED", "a write was not approved"),
                    Refusal("SCOPE_NOT_ALLOWED", "the zone is outside the allow list"),
                    Refusal("CREDENTIAL_UNSET", "no credential is configured"),
                    Refusal("RATE_LIMITED", "the provider rate limit was reached"),
                    Refusal("UPSTREAM_ERROR", "the provider returned an error"),
                ),
            ),
        ),
        "Identify the connection, find the endpoint, then call it with approval for writes.",
    ),
    ToolUseContract(
        "read-cloudflare-docs",
        (ToolStep("cloudflare_docs", (), ("results",)),),
        "Look up provider documentation before choosing an endpoint.",
    ),
)

LINKS = (
    SurfaceLink(
        "operate-cloudflare",
        tools=("cloudflare_whoami", "cloudflare_search", "cloudflare_execute"),
        prompts=("cloudflare-operator", "cloudflare-zone-administrator"),
        skills=("cloudflare-operations",),
    ),
    SurfaceLink(
        "read-cloudflare-docs",
        tools=("cloudflare_docs",),
        prompts=("cloudflare-operator",),
        skills=("cloudflare-operations",),
    ),
)

LOCATIONS = (
    DataLocation(
        "cloudflare-identity",
        ("CloudflareOperation",),
        "CLOUDFLARE_UPSTREAM_URL",
        "cloudflare_whoami",
        federation_key="id",
    ),
)

ROLES = (BusinessRole("zone-administrator", ("operate-cloudflare",), "Runs DNS, TLS and email routing for public zones."),)
