---
name: cloudflare-operations
skill_type: skill
domain: connector
description: Operate Cloudflare through its provider tools served as cloudflare_<tool>. Use when reading or changing Cloudflare state.
---

# Cloudflare operations

1. Find the operation with the fleet search; every provider tool is served as `cloudflare_<tool>`.
2. Read first with the read tools.
3. A write returns a confirmation request: approve it, or it is refused with `WRITE_NOT_APPROVED`.
4. Refusal codes: `WRITE_NOT_APPROVED`, `SCOPE_NOT_ALLOWED`, `CREDENTIAL_UNSET`, `RATE_LIMITED`, `UPSTREAM_ERROR`.
