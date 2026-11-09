# Motivs

![Motivs](assets/logo.png)

Motivs is the product and company brand of MOTIVS OÜ, the publisher behind
[motivs.ai](https://motivs.ai).

Motivs builds and validates recurring Excel and CSV automations in Motivs Platform.
Describe the business outcome, confirm its rules, and validate an automation version
against protected examples uploaded directly to Motivs. Run it and receive its
reports in the platform.

## Install

In a current Claude Code session:

```text
/plugin install motivs --marketplace MOTIVS-PRODUCTS/motivs-claude-plugin
```

This repository is being prepared for its first Anthropic directory submission.
It is not yet an approved directory listing. Availability in claude.ai and Cowork
through the directory depends on Anthropic review and publication.

## Connect and build

1. Sign in to Motivs and select the intended workspace. Create a draft and upload
   protected examples in Motivs, not into the assistant conversation.
2. Authorize the production MCP connection through OAuth. Ask for
   `connection_status` to confirm the workspace, role, and scopes without displaying
   account emails or credentials. A browser workspace switch does not rebind an
   existing OAuth connection; authorize a new connection for another workspace.
3. Ask to build or repair the draft by its exact name. Confirm the business rules,
   output, and acceptance checks before building.
4. The skill reads approved metadata, submits code and a manifest, then validates
   the exact returned candidate version inside Motivs. Failures are repaired as
   new immutable candidates using structured feedback.
5. In collaboration workspaces, passing validation does not change the working
   version. A user with current `access.can_pin` (the automation owner or workspace
   Owner) must explicitly select it in Motivs. Ordinary editing access is not enough.
6. Open the returned Motivs URL to run the automation and receive the report.

## Access and data handling

The single remote MCP server uses Streamable HTTP at
`https://mcp.motivs.ai/mcp`. No development or drill endpoint is configured. OAuth
scopes limit the connection; current workspace membership and per-resource
capabilities decide which actions are allowed. Shared automations may be available
when the current user has the required rights. A missing result does not prove
that an automation was deleted.

Active Members can create root folders and automations. Creation in a selected
folder requires that folder's creation capability. Workspace Owner administration
does not grant access to another person's protected run inputs or outputs.

Protected source rows, cell values, raw run logs, and finished reports stay in
Motivs. The assistant receives approved structure, user-authored rules, code, and
structured validation feedback. Names, field labels, instructions, and code can
still contain personal information: do not put secrets or protected values in
those fields or directly into the conversation. See the privacy policy below for
service data handling and provider responsibilities.

If a password reset or revoked authorization requires sign-in again, use the
client's reconnect action. If that client action fails, remove the stale
connector and authorize a new production connection through the normal settings.
Confirm its workspace and current permissions before continuing. Do not paste
passwords or tokens into chat.

## Package contents

- One skill, `excel-workflow-automation-builder`, and its references.
- `scaffold_studio.py`: generates a starter automation module and manifest.
- `check_platform_adapter.py`: checks the automation's backend adapter. It imports
  the supplied module, so run it only on reviewed code in an appropriate environment.
- `intelligence_kernels.py`: optional calculation helpers requiring NumPy and pandas.
- A product icon, a proprietary license, and the production MCP configuration.

The helpers are optional and require a host that can execute Python. The scaffold
and adapter checker use Python's standard library, but the generated automation
may have additional runtime requirements. The skill keeps protected validation
inside Motivs; the helpers are not a request to download examples into a local
assistant environment. There are no hooks, slash commands, agents, local MCP
servers, or automatic dependency installation in this package.

## Package version

Package version: **0.7.3**. See the [changelog](CHANGELOG.md).
The repository's [submission guide](https://github.com/MOTIVS-PRODUCTS/motivs-claude-plugin/blob/main/PUBLISHING.md)
covers maintainer checks and the separate Anthropic review process.
Maintainer checks and CI configuration are not installed with this plugin.

## Links and license

- [Product](https://motivs.ai)
- [Support](https://motivs.ai/support)
- [Privacy](https://motivs.ai/privacy)
- [Terms](https://motivs.ai/terms)
- [License](LICENSE): proprietary Motivs plugin license, not an open-source license.
