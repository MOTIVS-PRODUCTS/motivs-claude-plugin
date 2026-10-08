# Motivs

![Motivs](assets/logo.png)

Motivs turns recurring Excel and CSV work into validated automations. You describe
the outcome in plain language, Motivs builds the pipeline, runs it against examples
you upload to the platform, and returns the report, plan, or decision output you
asked for.

Source rows and cell values stay inside Motivs. The skill reads structure, column
names, and validation verdicts, not the contents of your workbook, so protected
examples are never pasted into the conversation.

## What this package contains

- One skill, `excel-workflow-automation-builder`, with its reference set.
- Three optional Python helpers under `skills/excel-workflow-automation-builder/scripts/`.
  They profile a workbook, scaffold a studio layout, and compare a workbook against
  an expected result. The skill tells Claude when to run them. They are plain
  standard library scripts with no third party imports.
- The product mark shown above, used by the listing.

There are no hooks, commands, agents, or background processes in this package.

## What it connects to

`.mcp.json` declares one remote server over Streamable HTTP:

`https://mcp.motivs.ai/mcp`

The server requires OAuth. On first use Claude opens the Motivs authorization page,
and every tool call runs as the account that authorized it. Discovery is scoped to
that account, so automations owned by a colleague are absent from the answer rather
than refused.

The server exposes automation and run tools: create and version an automation,
commit a build brief, validate a version, read run outputs and artifacts, and build
a repair package after a failure. Nothing in this package sends data anywhere else,
and no credential is read from your machine.

## Install

In Claude Code:

```
/plugin install motivs
```

The plugin also loads on claude.ai and in Cowork once the listing is published.
The skill and its references load on every surface. The Python helpers run only
where a host can execute them, which today means Claude Code.

## One account owns the intake and the plugin

Whoever uploads the protected examples must be the same account that authorizes the
plugin. If an automation cannot be found by name, check the account first:
`connection_status` names the authenticated user.

## Links

- Product: https://motivs.ai
- Support: https://motivs.ai/support
- Privacy: https://motivs.ai/privacy
- Terms: https://motivs.ai/terms
