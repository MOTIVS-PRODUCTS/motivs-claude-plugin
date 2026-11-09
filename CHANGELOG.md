# Changelog

## 0.7.2 - 2026-11-09

- Synchronize the skill with the production 0.7.1 integration: current resource
  permissions, shared workspace discovery, exact parent versions, current contract
  revisions, immutable candidates, archives, and revoked or stopped access.
- Correct working-version instructions: the automation owner or workspace Owner
  may explicitly select a version when current `access.can_pin` permits it.
  Validation alone never changes the collaboration working pin.
- Stop asking the assistant to display authenticated account identities during
  discovery and access troubleshooting.
- Correct installation, helper descriptions and dependencies, privacy boundaries,
  and first-submission status in the README.
- Add package checks and a submission checklist. Production MCP URL and plugin
  identity remain unchanged. No platform deployment or server change is included.

## 0.5.0

- Initial standalone Claude plugin package with the production MCP connection,
  spreadsheet automation skill, optional Python helpers, and product icon.
