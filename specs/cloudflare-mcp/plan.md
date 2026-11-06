# CONN-CLOUDFLARE-MCP — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

The connector serves the provider's own MCP server in its typed mode, one tool per API operation, as `cloudflare_<tool>`, behind write approval, a zone allow list, typed refusals and audit. Scope: public zones, DNS records, TLS mode and email routing. Depends on: `SCION-CONNECTOR-CONTROL-R914`, `ARBORA-FLEET-R059`, `ARBORA-FLEET-R060`.

## Technical Context

- **Language/Version**: Python 3.14, floor 3.12
- **Primary Dependencies**: `scion-sdk[mcp]` only
- **Storage**: N/A
- **Testing**: pytest, run by the shared `tests-fast` hook; contract-level proofs
- **Target Platform**: Linux container, streamable HTTP or stdio
- **Project Type**: connector
- **Performance Goals**: N/A
- **Constraints**: no host, credential or endpoint in the repository
- **Scale/Scope**: one external system

## Constitution Check

One external system, one tool per operation, the SDK as the only dependency: see `.specify/memory/constitution.md`.

## Project Structure

`cloudflare_mcp/` holds the connector; `tests/` holds the bound tests; `specs/cloudflare-mcp/` holds this spec.

## Phase 0: Research

No unknowns. The SDK and the shared pipelines own the server, transports, gates and release.

## Phase 1: Design

`cloudflare_mcp/upstreams.py` declares the provider MCP server; the SDK registry mounts it. `cloudflare_mcp/governance.py` is a fastmcp middleware on every call. Rows R003 to R008 are served by the provider's typed tools; their facade checks and bound tests are the next slices.

## Phase 2: Task approach

One task per row in [tasks.md](tasks.md); each lands with its bound test.

## Complexity Tracking

No deviation from the constitution.

## Build contract

`uv sync`, then `uvx pre-commit run --all-files`. The release workflow builds and publishes on a version tag.

## Production caller chain

`cloudflare-mcp` console script → `scion_sdk.cli:serve` → entry point `cloudflare-mcp = "cloudflare_mcp:connector"` → served tools.

## Cross-repo seams

None. The SDK and arbora are used through their published interfaces only.
