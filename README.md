# cloudflare-mcp

MCP connector for Cloudflare. The SDK serves everything over MCP: tools, prompts,
skills, ontology resources and the data-source declaration (`connector://resources`).

    pip install cloudflare-mcp
    cloudflare-mcp --transport stdio

Wraps the provider's MCP server. Settings: `CLOUDFLARE_UPSTREAM_URL`, `CLOUDFLARE_TOKEN`, `CLOUDFLARE_ALLOWED_SCOPES`.
