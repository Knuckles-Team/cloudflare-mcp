# CONN-CLOUDFLARE-MCP — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Level | Setup and input | Expected observation | Evidence |
|---|---|---|---|---|---|
| T-001 | `CONN-CLOUDFLARE-MCP-R001` | Contract | `tests/test_upstreams.py::test_upstream_declared_without_host` | Declare the provider upstream holds. |  |
| T-002 | `CONN-CLOUDFLARE-MCP-R002` | Contract | `tests/test_probe.py::test_probe_reports_drift` | Probe the upstream tool list holds. |  |
| T-003 | `CONN-CLOUDFLARE-MCP-R003` | Contract | `tests/test_zone_tools.py::test_zone_reads_are_typed_reads` | Zone tools holds. |  |
| T-004 | `CONN-CLOUDFLARE-MCP-R004` | Contract | `tests/test_dns_record_tools.py::test_one_tool_per_record_operation` | DNS record tools holds. |  |
| T-005 | `CONN-CLOUDFLARE-MCP-R005` | Contract | `tests/test_dns_record_tools.py::test_proxied_flag_and_unproxiable_refusal` | Proxy flag holds. |  |
| T-006 | `CONN-CLOUDFLARE-MCP-R006` | Contract | `tests/test_tls_tools.py::test_tls_mode_closed_set` | TLS mode holds. |  |
| T-007 | `CONN-CLOUDFLARE-MCP-R007` | Contract | `tests/test_email_routing_tools.py::test_routing_enable_rules_destinations` | Email Routing holds. |  |
| T-008 | `CONN-CLOUDFLARE-MCP-R008` | Contract | `tests/test_mail_auth_tools.py::test_dkim_spf_dmarc_publish_and_verify` | Mail authentication records holds. |  |
| T-009 | `CONN-CLOUDFLARE-MCP-R009` | Contract | `tests/test_governance.py::test_unapproved_write_sends_nothing_upstream` | Write approval for DNS changes holds. |  |
| T-010 | `CONN-CLOUDFLARE-MCP-R010` | Contract | `tests/test_governance.py::test_each_failure_has_a_typed_code` | Typed refusals holds. |  |
| T-011 | `CONN-CLOUDFLARE-MCP-R011` | Contract | `tests/test_governance.py::test_foreign_scope_refused_before_upstream` | Zone allow list holds. |  |
| T-012 | `CONN-CLOUDFLARE-MCP-R012` | Contract | `tests/test_governance.py::test_audit_record_redacts_secrets` | Audit holds. |  |
| T-013 | `CONN-CLOUDFLARE-MCP-R012.1` | Contract | `tests/test_audit.py::test_write_audit_record_has_old_and_new_value` | Audit old and new values holds. |  |
| T-014 | `CONN-CLOUDFLARE-MCP-R013` | Contract | `tests/integration/test_fleet_coverage.py::test_single_entry_passes_coverage_gate` | Fleet onboarding holds. |  |
| T-015 | `CONN-CLOUDFLARE-MCP-R014` | Contract | `tests/integration/test_edge_journey_served.py::test_record_tls_and_mail_auth_journey` | Hot-path proof holds. |  |
| T-016 | `CONN-CLOUDFLARE-MCP-R015` | Contract | `tests/test_coverage.py::test_served_tools_cover_upstream_with_typed_schemas` | Served coverage holds. |  |
| T-017 | `CONN-CLOUDFLARE-MCP-R016` | Contract | `tests/test_declared_surface.py::test_declared_upstream_tools_match_the_published_list` | The declared upstream surface holds. |  |

## Negative and boundary cases

Refusals and denials are proved by the bound tests of `CONN-CLOUDFLARE-MCP-R001` and its siblings.

## Quality and release proof

The shared `tests-fast`, `spec` and `connector-standard` hooks pass on the pull request.
