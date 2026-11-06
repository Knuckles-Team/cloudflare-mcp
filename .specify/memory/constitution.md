# Cloudflare connector constitution

This connector inherits the [organization constitution](https://github.com/Knuckles-Team/pipelines/blob/main/.specify/memory/constitution.md) version 1.0.0. Every article of that constitution applies here. This file adds only the rules of this connector.

**Inherits**: organization constitution v1.0.0 | **Version**: 1.0.0 | **Ratified**: [date] | **Last amended**: [date]

## Organization standards

- [Spec standard](https://github.com/Knuckles-Team/pipelines/blob/main/reference/spec-standard.md): one owning spec per capability, computed states, `Spec:` trailers.
- [Ecosystem boundaries](https://github.com/Knuckles-Team/pipelines/blob/main/reference/ecosystem-boundaries.md): which repository owns which requirement.
- [Wording standard](https://github.com/Knuckles-Team/pipelines/blob/main/reference/ste.md): sentences of 20 words or fewer, with `must`, `should`, or `may`.

## Repository articles

### R-I. One external system

This connector wraps Cloudflare and nothing else. Shared helpers, domain maths and stores belong to their owners.

**Enforced by:** `connector-surface-audit` and `sdk-conformance` in pipelines.

**Plan check:** Does the change touch only the calls, mappings and tools of Cloudflare?

### R-II. One tool per API operation

Each API operation is one public method of `Api` and one served tool. No tool condenses operations behind an action or parameter dispatch.

**Enforced by:** `scripts/check_tool_parity.py` in the `mcp-builder` skill and `connector-surface-audit`.

**Plan check:** Does every new operation add exactly one method and one tool?

### R-III. The SDK is the only dependency

The connector depends on the connector SDK alone. Auth, TLS, paging, limits and optional dependencies come from SDK components and extras.

**Enforced by:** `sdk-conformance`, `connector-graphql` and `connector-standard` in pipelines.

**Plan check:** Does the change add no direct dependency and no copy of an SDK capability?

## Repository limits

This connector sets no numeric limit of its own. It follows the organization limits table.

Amend this file in a reviewed change. State the impact in the pull request. When the organization constitution changes its version, update the **Inherits** line in the same change.
