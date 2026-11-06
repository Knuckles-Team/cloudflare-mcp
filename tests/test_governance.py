"""Governance of the wrapped upstream: approval, scope, refusals, audit."""

import asyncio
from types import SimpleNamespace

from cloudflare_mcp import governance
from cloudflare_mcp.upstreams import NAMESPACE


class _Message(SimpleNamespace):
    pass


def _context(name, arguments=None):
    return SimpleNamespace(
        message=_Message(name=name, arguments=arguments or {}),
        fastmcp_context=None,
    )


def test_write_verbs_and_read_only_annotation():
    assert governance.is_write(f"{NAMESPACE}_post_items")
    assert governance.is_write(f"{NAMESPACE}_delete_items_id")
    assert not governance.is_write(f"{NAMESPACE}_get_items")
    assert not governance.is_write(
        f"{NAMESPACE}_post_x", SimpleNamespace(readOnlyHint=True)
    )


async def _test_unapproved_write_sends_nothing_upstream(monkeypatch):
    monkeypatch.setenv(governance.TOKEN_ENV, "unit-test")
    sent = []

    async def upstream(context):
        sent.append(context)

    result = await governance.GovernanceMiddleware().on_call_tool(
        _context(f"{NAMESPACE}_post_items"), upstream
    )
    assert result.structured_content["code"] == governance.WRITE_NOT_APPROVED
    assert sent == []


async def _test_each_failure_has_a_typed_code(monkeypatch):
    middleware = governance.GovernanceMiddleware()
    monkeypatch.delenv(governance.TOKEN_ENV, raising=False)
    unset = await middleware.on_call_tool(_context(f"{NAMESPACE}_get_items"), None)
    assert unset.structured_content["code"] == governance.CREDENTIAL_UNSET
    monkeypatch.setenv(governance.TOKEN_ENV, "unit-test")

    async def limited(context):
        raise RuntimeError("HTTP 429 rate limit")

    async def broken(context):
        raise RuntimeError("boom")

    rate = await middleware.on_call_tool(_context(f"{NAMESPACE}_get_items"), limited)
    fail = await middleware.on_call_tool(_context(f"{NAMESPACE}_get_items"), broken)
    assert rate.structured_content["code"] == governance.RATE_LIMITED
    assert fail.structured_content["code"] == governance.UPSTREAM_ERROR


async def _test_foreign_scope_refused_before_upstream(monkeypatch):
    monkeypatch.setenv(governance.TOKEN_ENV, "unit-test")
    monkeypatch.setenv(governance.ALLOWED_SCOPES_SETTING, "allowed")
    argument = "scope_under_test"
    monkeypatch.setattr(governance, "SCOPE_ARGUMENTS", (argument,))
    sent = []

    async def upstream(context):
        sent.append(context)

    result = await governance.GovernanceMiddleware().on_call_tool(
        _context(f"{NAMESPACE}_get_items", {argument: "other"}), upstream
    )
    assert result.structured_content["code"] == governance.SCOPE_NOT_ALLOWED
    assert sent == []


def test_audit_record_redacts_secrets():
    record = governance._redacted({"name": "a", "api_token": "s3cret"})
    assert record == {"api_token": "<redacted>", "name": "a"}


def test_unapproved_write_sends_nothing_upstream(monkeypatch):
    asyncio.run(_test_unapproved_write_sends_nothing_upstream(monkeypatch))


def test_each_failure_has_a_typed_code(monkeypatch):
    asyncio.run(_test_each_failure_has_a_typed_code(monkeypatch))


def test_foreign_scope_refused_before_upstream(monkeypatch):
    asyncio.run(_test_foreign_scope_refused_before_upstream(monkeypatch))
