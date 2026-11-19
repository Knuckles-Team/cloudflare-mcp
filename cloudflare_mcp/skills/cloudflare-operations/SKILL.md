---
name: cloudflare-operations
skill_type: skill
domain: connector
description: Operate Cloudflare through its provider tools served as cloudflare_<tool>. Use when reading or changing Cloudflare state.
---

# Cloudflare operations

1. Call `cloudflare_whoami` to see which account the connection acts as. Find the operation with `cloudflare_search`, or read `cloudflare_docs`; every provider tool is served as `cloudflare_<tool>`.
2. Read first: `cloudflare_search`, `cloudflare_docs` and `cloudflare_whoami` change nothing.
3. `cloudflare_execute` calls the provider API. A write returns a confirmation request: approve it, or it is refused with `WRITE_NOT_APPROVED`.
4. Refusal codes: `WRITE_NOT_APPROVED`, `SCOPE_NOT_ALLOWED`, `CREDENTIAL_UNSET`, `RATE_LIMITED`, `UPSTREAM_ERROR`.
