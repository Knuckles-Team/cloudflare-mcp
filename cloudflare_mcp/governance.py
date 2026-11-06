"""Governance on every served Cloudflare tool: refusals, approval, scope and audit.

Every call passes this middleware before the upstream. A write needs approval
through the SDK confirmation; an unapproved write sends nothing upstream. A
call that names a scope outside the allow list is refused before any request.
Failures return a typed code, never a raw exception. Every write is audited
without the credential.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools import ToolResult
from scion_sdk.config import setting
from scion_sdk.mcp.confirmation import ctx_confirm_destructive

from .upstreams import NAMESPACE

__all__ = [
    "REFUSAL_CODES",
    "SCOPE_ARGUMENTS",
    "GovernanceMiddleware",
    "is_write",
    "register_governance",
]

AUDIT = logging.getLogger("cloudflare_mcp.audit")

WRITE_NOT_APPROVED = "WRITE_NOT_APPROVED"
SCOPE_NOT_ALLOWED = "SCOPE_NOT_ALLOWED"
CREDENTIAL_UNSET = "CREDENTIAL_UNSET"
RATE_LIMITED = "RATE_LIMITED"
UPSTREAM_ERROR = "UPSTREAM_ERROR"
REFUSAL_CODES = (
    WRITE_NOT_APPROVED,
    SCOPE_NOT_ALLOWED,
    CREDENTIAL_UNSET,
    RATE_LIMITED,
    UPSTREAM_ERROR,
)

#: Upstream tool-name verbs that change state.
WRITE_VERBS = (
    "post",
    "put",
    "patch",
    "delete",
    "create",
    "update",
    "set",
    "remove",
    "enable",
    "disable",
)
#: Arguments that name a scope checked against the allow list.
SCOPE_ARGUMENTS: tuple[str, ...] = ("zone_id",)
ALLOWED_SCOPES_SETTING = "CLOUDFLARE_ALLOWED_SCOPES"
TOKEN_ENV = "CLOUDFLARE_TOKEN"
_SECRET_WORDS = ("token", "secret", "password", "key", "authorization")


def is_write(name: str, annotations: Any = None) -> bool:
    """A tool writes unless it is annotated read-only or its verb reads."""
    if annotations is not None and getattr(annotations, "readOnlyHint", None) is True:
        return False
    bare = name.removeprefix(f"{NAMESPACE}_")
    return bare.split("_", 1)[0] in WRITE_VERBS


def _refusal(code: str, detail: str) -> ToolResult:
    payload = {"refused": True, "code": code, "detail": detail}
    return ToolResult(content=json.dumps(payload), structured_content=payload)


def _allowed_scopes() -> frozenset[str]:
    raw = setting(ALLOWED_SCOPES_SETTING, "")
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def _redacted(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        key: (
            "<redacted>"
            if any(word in key.lower() for word in _SECRET_WORDS)
            else value
        )
        for key, value in sorted(arguments.items())
    }


def _failure_code(error: Exception) -> str:
    text = str(error).lower()
    if "429" in text or "rate limit" in text:
        return RATE_LIMITED
    return getattr(error, "code", None) or UPSTREAM_ERROR


class GovernanceMiddleware(Middleware):
    """Typed refusals, write approval, scope allow list and audit."""

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        name = context.message.name
        arguments = dict(context.message.arguments or {})
        if not name.startswith(f"{NAMESPACE}_"):
            return await call_next(context)
        if not os.environ.get(TOKEN_ENV):
            return _refusal(CREDENTIAL_UNSET, f"{TOKEN_ENV} is not set")
        allowed = _allowed_scopes()
        for argument in SCOPE_ARGUMENTS:
            value = arguments.get(argument)
            if value is not None and str(value) not in allowed:
                return _refusal(
                    SCOPE_NOT_ALLOWED, f"{argument} is outside {ALLOWED_SCOPES_SETTING}"
                )
        tool = None
        if context.fastmcp_context is not None:
            tool = await context.fastmcp_context.fastmcp.get_tool(name)
        write = is_write(name, getattr(tool, "annotations", None))
        approval = None
        if write:
            approved = await ctx_confirm_destructive(
                context.fastmcp_context,
                f"{name} changes Cloudflare state",
                confirmation_arguments=arguments,
            )
            if approved is not True:
                if approved is not False:
                    return approved
                return _refusal(WRITE_NOT_APPROVED, f"{name} needs approval")
            approval = "confirmed"
        try:
            result = await call_next(context)
        except Exception as error:  # noqa: BLE001 - every upstream failure becomes a typed code
            return _refusal(_failure_code(error), type(error).__name__)
        if write:
            caller = getattr(context.fastmcp_context, "client_id", None)
            AUDIT.info(
                json.dumps(
                    {
                        "tool": name,
                        "arguments": _redacted(arguments),
                        "caller": caller,
                        "approval": approval,
                    },
                    sort_keys=True,
                    default=str,
                )
            )
        return result


def register_governance(ctx: Any) -> None:
    """Install the governance middleware on the connector's server."""
    ctx.server.add_middleware(GovernanceMiddleware())
