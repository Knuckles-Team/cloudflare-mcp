---
name: cloudflare-mcp-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the cloudflare-mcp connector. Use when changing
  its API mappings, MCP tools, packaging, documentation, or repository gates.
license: MIT
tags: [cloudflare-mcp, development, connector, test, gates]
tier: repository
metadata:
  author: Repository Maintainers
  version: '0.1.0'
---

# cloudflare-mcp development

This repository owns the Cloudflare transport, mappings, MCP tools and package
content. Shared connector contracts, authentication and transports belong to
`scion-sdk`; admission, serving and durable graph state belong to
their owning repositories. Keep provider credentials, endpoints and raw data
out of source, logs and skill content.

## Rapid delivery: the 5-minute contract

Specs are designed before implementation. Deliver small, reviewable slices and
cite the owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend that
  spec before adding new requirement text.
- Reuse existing SDK clients, transport policies and tool factories. Do not
  create a second implementation of a connector capability.
- Keep changes scoped to this connector. A change owned by the SDK, Arbora or
  the knowledge graph belongs in that repository instead.
- Every delivered requirement needs a bound test. Spec status is computed by
  `pipelines-hook spec-status` at read time; `status.json` is never committed.
- One logical change per commit, with `Spec: <ID>` and the assisting agent
  trailer adjacent in the final paragraph.

## Setup and gates

On the first checkout, create the lockfile before using locked commands:

```bash
uv lock
uv sync --locked
```

Run the repository gate from the checkout root:

```bash
uvx pre-commit run --all-files
```

For focused feedback, run the relevant tests with the repository's pinned
environment. The canonical `.pre-commit-config.yaml` delegates
`connector-standard`, `secrets`, `spec`, `tests-fast` and
`dependency-readiness` to `Knuckles-Team/pipelines` at `rev: main`; do not
replace those shared hooks with local copies or bypass a failing check.
The generated starter test is `tests/test_api_client.py::test_each_operation_calls_its_endpoint`;
keep that path and test name in sync when changing the starter operations.

## Connector-specific checks

- Keep the MCP surface aligned with `scion-sdk`.
- Validate environment and TLS settings before provider calls.
- Mock external provider calls in tests; never use live credentials in a local gate.
- Keep `cloudflare_mcp/skills/` package data intact when adding skills.
- Documentation lives under `pages/` and is published by the shared Pages
  workflow; source status records live under `specs/`.
- The scaffold leaves `shared_theme_enabled: false` because the shared Pages
  workflow requires canonical theme outputs in the content tree. If this
  connector adopts the shared theme, use the pinned pipelines checkout and its
  `scripts/sync_mkdocs_theme.py sync` command to generate the assets, review
  them, commit them, and only then enable the caller flag. Never hand-copy or
  reimplement the provider assets.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths and verify `git status --short` after every gate. Do
not use `git stash`, `git add -A` or `git add .`; do not claim Pages publication
until a successful exact-source workflow run and the public page are both
observed.
