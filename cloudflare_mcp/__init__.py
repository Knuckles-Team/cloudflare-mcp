"""MCP connector for Cloudflare: the provider's MCP server behind our governance."""

from scion_sdk.connector import Connector

from .governance import register_governance
from .upstreams import UPSTREAMS

connector = Connector(
    instructions=(
        "Operate Cloudflare through its provider tools, served as cloudflare_<tool>. "
        "Read before you change. Every write asks for approval first."
    ),
    upstreams=UPSTREAMS,
    extra_registrations=(register_governance,),
)
