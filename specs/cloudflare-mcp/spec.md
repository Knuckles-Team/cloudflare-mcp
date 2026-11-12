# CONN-CLOUDFLARE-MCP — Cloudflare connector

Owner: cloudflare-mcp.

## Delivery mapping

Rows live in [requirements.md](requirements.md). Design: [plan.md](plan.md). Tests: [test-spec.md](test-spec.md).

## User Scenarios & Testing

### User Story 1 - Declare the provider upstream (Priority: P1)

One `UpstreamDecl` declares the provider MCP server with `kind` `http`, a URL setting, a credential reference and a TLS profile setting. The repository must ship no host name.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_upstreams.py::test_upstream_declared_without_host`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** declare the provider upstream holds as `CONN-CLOUDFLARE-MCP-R001` states.

### User Story 2 - Probe the upstream tool list (Priority: P2)

The `cloudflare-mcp-probe` script must list the upstream tools, count typed schemas and print the SDK fingerprint. It must exit non-zero when the fingerprint differs from `CLOUDFLARE_UPSTREAM_FINGERPRINT`.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_probe.py::test_probe_reports_drift`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** probe the upstream tool list holds as `CONN-CLOUDFLARE-MCP-R002` states.

### User Story 3 - Zone tools (Priority: P3)

The connector must serve typed tools to list zones, read one zone and read zone settings. Each is a read.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_zone_tools.py::test_zone_reads_are_typed_reads`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** zone tools holds as `CONN-CLOUDFLARE-MCP-R003` states.

### User Story 4 - DNS record tools (Priority: P3)

The connector must serve one typed tool per operation to list, get, create, update and delete records of kind A, AAAA, CNAME, TXT and MX. Create, update and delete are writes.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_dns_record_tools.py::test_one_tool_per_record_operation`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** dns record tools holds as `CONN-CLOUDFLARE-MCP-R004` states.

### User Story 5 - Proxy flag (Priority: P3)

Record create and update tools must take a typed `proxied` boolean. A record type that cannot be proxied must return a typed refusal.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_dns_record_tools.py::test_proxied_flag_and_unproxiable_refusal`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** proxy flag holds as `CONN-CLOUDFLARE-MCP-R005` states.

### User Story 6 - TLS mode (Priority: P3)

Typed tools must read and set the zone TLS mode. The set tool must accept only `off`, `flexible`, `full` and `strict`. Another value must return a typed refusal.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_tls_tools.py::test_tls_mode_closed_set`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** tls mode holds as `CONN-CLOUDFLARE-MCP-R006` states.

### User Story 7 - Email Routing (Priority: P3)

Typed tools must enable and disable routing for a zone and manage routing rules and destination addresses.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_email_routing_tools.py::test_routing_enable_rules_destinations`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** email routing holds as `CONN-CLOUDFLARE-MCP-R007` states.

### User Story 8 - Mail authentication records (Priority: P3)

A typed tool must return the provider-generated DKIM, SPF and DMARC records for a zone. A second tool must publish missing ones. A read-back tool must report `pass`, `missing` or `mismatch` for each record.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_mail_auth_tools.py::test_dkim_spf_dmarc_publish_and_verify`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** mail authentication records holds as `CONN-CLOUDFLARE-MCP-R008` states.

### User Story 9 - Write approval for DNS changes (Priority: P3)

Every write tool must apply the SDK destructive-write confirmation. A write without approval must return a typed refusal and send nothing upstream.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_governance.py::test_unapproved_write_sends_nothing_upstream`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** write approval for dns changes holds as `CONN-CLOUDFLARE-MCP-R009` states.

### User Story 10 - Typed refusals (Priority: P3)

An unset credential, a rate limit and an upstream error must each return a typed code, not a raw exception.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_governance.py::test_each_failure_has_a_typed_code`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** typed refusals holds as `CONN-CLOUDFLARE-MCP-R010` states.

### User Story 11 - Zone allow list (Priority: P3)

`CLOUDFLARE_ALLOWED_SCOPES` lists the zones the connector may touch. A call that names another `zone_id` must be refused before any upstream request.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_governance.py::test_foreign_scope_refused_before_upstream`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** zone allow list holds as `CONN-CLOUDFLARE-MCP-R011` states.

### User Story 12 - Audit (Priority: P3)

Every write must record the tool, the arguments, the caller and the approval. The record must hold no credential.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_governance.py::test_audit_record_redacts_secrets`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** audit holds as `CONN-CLOUDFLARE-MCP-R012` states.

### User Story 13 - Audit old and new values (Priority: P3)

The audit record of a DNS write must also hold the zone, record name, type, old value and new value.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_audit.py::test_write_audit_record_has_old_and_new_value`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** audit old and new values holds as `CONN-CLOUDFLARE-MCP-R012.1` states.

### User Story 14 - Fleet onboarding (Priority: P3)

One fleet entry, lazy namespaces and a passing coverage gate under arbora.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/integration/test_fleet_coverage.py::test_single_entry_passes_coverage_gate`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** fleet onboarding holds as `CONN-CLOUDFLARE-MCP-R013` states.

### User Story 15 - Hot-path proof (Priority: P3)

Against a fixture upstream, a client must create a proxied record, set TLS mode, enable Email Routing and verify mail authentication over the served connector.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/integration/test_edge_journey_served.py::test_record_tls_and_mail_auth_journey`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** hot-path proof holds as `CONN-CLOUDFLARE-MCP-R014` states.

### User Story 16 - Served coverage (Priority: P3)

The connector must serve at least as many tools as the upstream lists, each with a typed input schema.

**Why this priority**: the connector is not usable without it.

**Independent Test**: `tests/test_coverage.py::test_served_tools_cover_upstream_with_typed_schemas`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** a client uses it, **Then** served coverage holds as `CONN-CLOUDFLARE-MCP-R015` states.

### User Story 17 - Declared upstream surface (Priority: P3)

The connector must declare the tools the provider's MCP server publishes, so the surface gate checks them offline.

**Why this priority**: the connector registers no tool without a live upstream.

**Independent Test**: `tests/test_declared_surface.py::test_declared_upstream_tools_match_the_published_list`.

**Acceptance Scenarios**:

1. **Given** the connector is installed, **When** the surface gate runs offline, **Then** the declared surface holds as `CONN-CLOUDFLARE-MCP-R016` states.

### Edge Cases

- An unset setting or credential returns a typed refusal and sends nothing to the provider.

## Requirements

The connector serves the provider's own MCP server in its typed mode, one tool per API operation, as `cloudflare_<tool>`, behind write approval, a zone allow list, typed refusals and audit. Scope: public zones, DNS records, TLS mode and email routing. Depends on: `SCION-CONNECTOR-CONTROL-R914`, `ARBORA-FLEET-R059`, `ARBORA-FLEET-R060`.

## Success Criteria

- Every row in requirements.md has a passing bound test.

## Assumptions

- The SDK serves the connector; this repository owns only the Cloudflare calls, mappings and tools.

## Why a new spec

No spec in this repository owns the Cloudflare operations.

## Scope and interfaces

In scope: the operations, prompts, skills and ontology of Cloudflare. Out of scope: server start, SDK
behavior, version files, container files and gates; the SDK and pipelines own them.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-CLOUDFLARE-MCP-R001` | plan.md#phase-1-design | T-001 |  |
| FR-002 | `CONN-CLOUDFLARE-MCP-R002` | plan.md#phase-1-design | T-002 |  |
| FR-003 | `CONN-CLOUDFLARE-MCP-R003` | plan.md#phase-1-design | T-003 |  |
| FR-004 | `CONN-CLOUDFLARE-MCP-R004` | plan.md#phase-1-design | T-004 |  |
| FR-005 | `CONN-CLOUDFLARE-MCP-R005` | plan.md#phase-1-design | T-005 |  |
| FR-006 | `CONN-CLOUDFLARE-MCP-R006` | plan.md#phase-1-design | T-006 |  |
| FR-007 | `CONN-CLOUDFLARE-MCP-R007` | plan.md#phase-1-design | T-007 |  |
| FR-008 | `CONN-CLOUDFLARE-MCP-R008` | plan.md#phase-1-design | T-008 |  |
| FR-009 | `CONN-CLOUDFLARE-MCP-R009` | plan.md#phase-1-design | T-009 |  |
| FR-010 | `CONN-CLOUDFLARE-MCP-R010` | plan.md#phase-1-design | T-010 |  |
| FR-011 | `CONN-CLOUDFLARE-MCP-R011` | plan.md#phase-1-design | T-011 |  |
| FR-012 | `CONN-CLOUDFLARE-MCP-R012` | plan.md#phase-1-design | T-012 |  |
| FR-013 | `CONN-CLOUDFLARE-MCP-R012.1` | plan.md#phase-1-design | T-013 |  |
| FR-014 | `CONN-CLOUDFLARE-MCP-R013` | plan.md#phase-1-design | T-014 |  |
| FR-015 | `CONN-CLOUDFLARE-MCP-R014` | plan.md#phase-1-design | T-015 |  |
| FR-016 | `CONN-CLOUDFLARE-MCP-R015` | plan.md#phase-1-design | T-016 |  |
| FR-017 | `CONN-CLOUDFLARE-MCP-R016` | plan.md#phase-1-design | T-017 |  |
