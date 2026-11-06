"""The one declared Cloudflare upstream MCP server (SCION-CONNECTOR-CONTROL-R914).

The SDK owns the transport, the pool, the health and the drift check. This
module adds data only. The repository ships no host: the URL, the credential
and the expected fingerprint are deployment settings.
"""

from __future__ import annotations

from scion_sdk.config import setting
from scion_sdk.mcp.upstreams import UpstreamDecl

__all__ = ["CREDENTIAL", "NAMESPACE", "UPSTREAMS", "URL_SETTING", "build_upstreams"]

#: Tools are served as ``<NAMESPACE>_<upstream tool>``.
NAMESPACE = "cloudflare"
URL_SETTING = "CLOUDFLARE_UPSTREAM_URL"
FINGERPRINT_SETTING = "CLOUDFLARE_UPSTREAM_FINGERPRINT"
#: A TLS profile from the SDK catalog; unset uses the system trust store.
TLS_PROFILE_SETTING = "CLOUDFLARE_TLS_PROFILE"
#: The credential is a reference; the SDK resolves it per call.
CREDENTIAL = "env://CLOUDFLARE_TOKEN"


def build_upstreams() -> tuple[UpstreamDecl, ...]:
    """The upstream declaration, or none while the URL setting is unset."""
    url = setting(URL_SETTING, "")
    if not url:
        return ()
    return (
        UpstreamDecl(
            name=NAMESPACE,
            kind="http",
            url=url,
            credential=CREDENTIAL,
            tls_profile=setting(TLS_PROFILE_SETTING, "") or None,
            activation="active",
            expected_fingerprint=setting(FINGERPRINT_SETTING, "") or None,
            on_drift="refuse",
        ),
    )


UPSTREAMS: tuple[UpstreamDecl, ...] = build_upstreams()
