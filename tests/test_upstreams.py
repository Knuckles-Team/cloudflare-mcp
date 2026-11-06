"""The upstream declaration ships no host and holds a credential reference only."""

import importlib

from cloudflare_mcp import upstreams


def test_upstream_declared_without_host(monkeypatch):
    monkeypatch.delenv(upstreams.URL_SETTING, raising=False)
    assert importlib.reload(upstreams).UPSTREAMS == ()
    monkeypatch.setenv(upstreams.URL_SETTING, "https://upstream.invalid/mcp")
    (decl,) = importlib.reload(upstreams).UPSTREAMS
    assert decl.name == upstreams.NAMESPACE
    assert decl.credential == upstreams.CREDENTIAL
    assert upstreams.CREDENTIAL.startswith("env://")
    monkeypatch.setenv(upstreams.TLS_PROFILE_SETTING, "edge")
    (decl,) = importlib.reload(upstreams).UPSTREAMS
    assert decl.tls_profile == "edge"
