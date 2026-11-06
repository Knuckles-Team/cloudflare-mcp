"""The probe reports the upstream fingerprint and exits 1 on drift."""

from types import SimpleNamespace

from cloudflare_mcp import probe


def _tool(name):
    return SimpleNamespace(
        name=name,
        inputSchema={"type": "object", "properties": {"zone_id": {"type": "string"}}},
        outputSchema=None,
    )


def test_probe_reports_drift(monkeypatch, capsys):
    async def tools(url):
        return [_tool("get_zones"), _tool("get_zones_zone_id_dns_records")]

    monkeypatch.setattr(probe, "_tools", tools)
    monkeypatch.setenv(probe.URL_SETTING, "https://upstream.invalid/mcp")
    monkeypatch.delenv(probe.FINGERPRINT_SETTING, raising=False)
    assert probe.main() == 0
    assert '"tools": 2' in capsys.readouterr().out
    monkeypatch.setenv(probe.FINGERPRINT_SETTING, "0" * 64)
    assert probe.main() == 1
