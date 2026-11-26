# Cloudflare Mcp
## CLI or API | MCP

![PyPI - Version](https://img.shields.io/pypi/v/cloudflare-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/cloudflare-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/cloudflare-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/cloudflare-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/cloudflare-mcp)
![PyPI - License](https://img.shields.io/pypi/l/cloudflare-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/cloudflare-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/cloudflare-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/cloudflare-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/cloudflare-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/cloudflare-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/cloudflare-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/cloudflare-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/cloudflare-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/cloudflare-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/cloudflare-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/cloudflare-mcp)

> **Documentation** — Installation, deployment, and usage across the API, CLI, MCP,
> and A2A agent interfaces are maintained in the
> [official documentation](https://knuckles-team.github.io/cloudflare-mcp/).

---

## Overview

MCP connector for Cloudflare. The SDK serves everything over MCP: tools, prompts,
skills, ontology resources and the data-source declaration (`connector://resources`).

    pip install cloudflare-mcp
    cloudflare-mcp --transport stdio

Wraps the provider's MCP server. Settings: `CLOUDFLARE_UPSTREAM_URL`, `CLOUDFLARE_TOKEN`, `CLOUDFLARE_ALLOWED_SCOPES`.

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/cloudflare-mcp/) and is
the recommended reference for installation, deployment, and day-to-day operation.

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by running local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Run test suites using `pytest`
