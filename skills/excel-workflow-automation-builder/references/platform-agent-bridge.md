# Platform Agent Bridge

Motivs agents connect only through the plugin-provided Streamable HTTP MCP server. The MCP host discovers the protected-resource and authorization-server metadata, dynamically registers a public client, uses authorization code with S256 PKCE, and opens Motivs consent in the user's browser.

## Authentication Rules

- Never ask for or accept a shared agent token.
- Never place access tokens, refresh tokens, cookies, object-store credentials, or database credentials in automation source or artifacts.
- Never call Motivs internal HTTP endpoints directly when MCP tools are available.
- Treat a missing or expired OAuth connection as a blocker and ask the user to reconnect the Motivs plugin.
- Keep automation and context IDs tenant-scoped; a not-found response may intentionally hide another organization's record.

## Privacy-First Flow

1. Call `connection_status` and confirm the selected organization and scopes.
2. Call `search_automations` with the user-provided name. Use `list_folders` to disambiguate. Confirm before editing when more than one match remains.
3. Call `get_automation_build_context` with the selected automation ID.
4. Resolve only material questions surfaced by `workbook_interpretation`, `business_meaning`, and `automation_spec`. Never request protected source rows or cell values.
5. Call `commit_build_brief` with the confirmed objective, source/region selections, material business entity and row grain when relevant, rules, output requirements, acceptance checks, and `confirmation_provenance.source` describing where the confirmation came from. Continue from the new contract revision it returns.
6. Build one self-contained `automation.py` plus a platform-rendered manifest. Bind each file input to `source_contract_ids`, set `runtime_contract` to `workbook-interpretation-v1`, and consume normalized region paths from `parameters["_motivs"]` when present.
7. Follow `collaboration-and-versions.md`: select the exact available source ID, then call `add_automation_version` with that `parent_version_id`, a factual `change_summary`, and the exact committed `contract_revision_id`. An empty draft has no parent. This creates a candidate and does not change the working pin.
8. Call `validate_automation` with the returned automation/version IDs.
9. Poll `get_run` until `passed`, `failed`, or `stopped`. This tool returns structured, metadata-safe feedback rather than raw logs. In collaboration workspaces a passed candidate leaves the working pin unchanged; a user with current `access.can_pin` (the automation owner or workspace Owner) must explicitly select the version used for runs in Motivs. Legacy publication behavior applies only when the connection flag is false.
10. On failure, the prior working version remains unchanged. Call `create_repair_package`, correct the source, and upload a new candidate. Never mutate an existing version.

## Tool Scope

- Read operations require the corresponding `automations:read`, `runs:read`, or `artifacts:read` scope.
- Source and metadata writes require `automations:write` and current manage access to that automation in collaboration workspaces. Legacy role checks remain server-side.
- Validation requires `runs:write` and current manage access; ordinary use and folder creation do not grant validation authority.
- Reading metadata-only contracts requires `context:read`; creating protected intake snapshots requires `context:write`.

## Data Boundary

- `get_automation_build_context` may disclose file names, sheet names, field names, type/presence classifications, scale bands, formula function names, and candidate relationships.
- It never returns source rows, cell values, exact source totals, object-store paths, source hashes, credentials, or raw execution logs.
- `get_run` returns structured stages and safe issue codes. Full technical logs remain visible only inside the authenticated Motivs platform.
- The contract revision is immutable. `commit_build_brief` creates a new revision; a version must reference that exact revision, and stale revisions cannot be promoted.

OAuth tokens are resource-bound to the configured MCP URL. A token issued for a local MCP resource cannot be replayed against production, and vice versa.
