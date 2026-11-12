"""Declared data sources. A wrapped upstream declares only the read it exposes for identity."""

from __future__ import annotations

from scion_sdk.ingest.live_declaration import source_meta

SCHEMA_VERSION = 1

SOURCES = (
    source_meta(
        tool="cloudflare_whoami",
        source_id="cloudflare-identity",
        record_type="identity",
        id_field="id",
    ),
)
