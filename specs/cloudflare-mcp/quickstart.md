# CONN-CLOUDFLARE-MCP — Quickstart

## Scenario: read zones and DNS records through the served connector

1. Set `CLOUDFLARE_UPSTREAM_URL` to the provider's MCP endpoint in typed mode, `CLOUDFLARE_TOKEN` to a scoped API token and `CLOUDFLARE_ALLOWED_SCOPES` to the allowed zone IDs.
2. Start the server: `cloudflare-mcp --transport streamable-http --port 8000`.
3. List tools, then call the zone list tool and the DNS record list tool for one allowed zone.
4. Call a DNS write without approval and observe the `WRITE_NOT_APPROVED` refusal.

## Test command

`uv run pytest tests -q`
