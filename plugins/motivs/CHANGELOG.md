# Changelog

## 0.7.4 - 2026-11-09

- Remove the three local executable helpers from the installable directory package
  to comply with the file policy applied to non-Verified publishers.
- Replace helper-dependent instructions with direct notebook authoring and exact
  candidate validation inside Motivs. Do not fetch omitted helpers or execute
  generated automation code in the assistant host.
- Keep original helper source in the separate maintainer development folder.
- Enforce allowed file types, UTF-8 text, no NUL bytes or shebangs, no executable
  permission bits, and no package-manager configuration in the installed package.
- Preserve Motivs branding, the production OAuth/MCP endpoint, data boundaries,
  explicit pin authority and protected platform validation requirements.

## 0.7.3 - 2026-11-09

- Ship only the plugin folder, excluding the maintainer package checker, CI
  configuration and submission instructions from the installed distribution.
- Keep the plugin identifier and display name Motivs; identify its publisher as
  MOTIVS OÜ and link the product website for directory reviewer context.
- Keep the same production MCP connection, skill, optional Python helpers, icon,
  license and access rules. No platform or authentication behavior changes.

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
