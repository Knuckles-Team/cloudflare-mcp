# cloudflare-mcp

## Spec-driven development

Every feature starts with a spec, in this order. Read `.specify/memory/constitution.md` first; it inherits the [organization constitution](https://github.com/Knuckles-Team/pipelines/blob/main/.specify/memory/constitution.md). Route the feature with the [ecosystem boundaries](https://github.com/Knuckles-Team/pipelines/blob/main/reference/ecosystem-boundaries.md) and file each part in its owner's `specs/`. Run the flow with the skills in the table (universal-skills). Rules: [spec standard](https://github.com/Knuckles-Team/pipelines/blob/main/reference/spec-standard.md); templates: `.specify/templates/`, vended by pipelines.

| Step | Skill | Writes | Checked by |
|---|---|---|---|
| Constitution | `speckit-constitution` | `.specify/memory/constitution.md` | spec-standard constitution check |
| Specify | `speckit-specify` | `specs/<id>/spec.md`, `requirements.md` | spec-standard |
| Clarify | `speckit-clarify` | resolves each `[NEEDS CLARIFICATION: ...]` marker | spec-standard clarification check |
| Plan | `speckit-plan` | `plan.md` (upstream sections, Build contract, Production caller chain, Cross-repo seams) | spec-standard plan check |
| Tasks | `speckit-tasks` | `tasks.md`: `- [ ] T001 [P] [US1] <ROW-ID> ...` | spec-standard task-line check |
| Analyze | `speckit-analyze`, `speckit-checklist` | `checklists/requirements.md`, gap fixes | spec-standard analysis and checklist |
| Implement | `speckit-implement` | code and bound tests (`mark.spec("ID")` or `// spec: ID`) | `pipelines-hook spec-trailers` |
| Land | repository development skill | commit with `Spec: <IDs>` directly above `Co-Authored-By` | `spec-status` computes SPECIFIED, LANDED, VERIFIED, RETIRED |
| Release | repository development skill | pipelines `releases/*.yml` bundles (the PIPE-RELEASE bundle rows) | `release-standard` |

Never write code for a row that is not SPECIFIED in this repository's `specs/`. If no row owns the behavior, extend the owning spec first. Never write `status.json` or a `Status:` line; the state is computed.

## Connector

Cloudflare connector. The operations are the methods of `cloudflare_mcp/api_client.py`; the SDK
serves one tool per method. `cloudflare_mcp/auth.py` builds the client, `cloudflare_mcp/connector_sources.py`
declares the data sources. Everything else is an SDK component or a shared pipelines file.

## Release

Bump first, tag last. A tag whose commit still carries the previous version rebuilds the
old version under the new tag and PyPI refuses it; the shared `python_pipeline.yml` guard
fails when the tag differs from the package version or the version is already on PyPI.

1. Bump the version first: it lives in `pyproject.toml` (and `.bumpversion.cfg` when the
   repo has one; then use `bump2version --config-file .bumpversion.cfg --allow-dirty --no-commit --no-tag <part>`).
   Refresh the lock and any recorded fixture that embeds the version in the same PR.
2. Merge the bump PR.
3. At the merged commit, check `git show <commit>:pyproject.toml` carries the intended
   version and that it is unpublished:
   `curl -s -o /dev/null -w '%{http_code}' https://pypi.org/pypi/cloudflare-mcp/X.Y.Z/json` must print `404`.
4. Only then push the tag `vX.Y.Z` on that commit.
5. Confirm the wheel and sdist are on PyPI.
6. Tag on the wrong commit and nothing published: delete the tag and re-tag. Anything
   published: cut the next patch; never move a published tag.
