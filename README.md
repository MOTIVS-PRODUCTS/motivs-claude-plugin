# Motivs plugin repository

This repository contains the Motivs plugin published by **MOTIVS OÜ**, the company
behind [motivs.ai](https://motivs.ai). Motivs is our product and company brand.
The plugin identifier remains `motivs`; its display name remains **Motivs**.

The installable package is [plugins/motivs](plugins/motivs). Its
[README](plugins/motivs/README.md) describes the production MCP connection, OAuth,
automation workflow, data boundary and optional Python helpers. This repository is
being prepared for its first Anthropic directory submission; it is not yet an
approved listing.

## Install

In a current Claude Code session:

```text
/plugin install motivs --marketplace MOTIVS-PRODUCTS/motivs-claude-plugin
```

The root marketplace manifest resolves that name to `./plugins/motivs`.
For directory validation, set **Plugin path** to `plugins/motivs`.

## Repository layout

- `plugins/motivs/`: the complete installable plugin, version **0.7.3**.
- `.claude-plugin/marketplace.json`: repository marketplace manifest.
- `scripts/check_package.py`: maintainer-only package checks, never installed.
- `.github/workflows/package.yml`: read-only CI, never installed.
- [PUBLISHING.md](PUBLISHING.md): submission steps and manual acceptance checks.
- [Changelog](plugins/motivs/CHANGELOG.md): package changes.
- [License](LICENSE): the same proprietary license included in the plugin.

## Validate

Run from the repository root:

```sh
python3 scripts/check_package.py
claude plugin validate . --strict
claude plugin validate plugins/motivs --strict
```

The checker inspects files without executing automation helper code. The first
native validation covers the marketplace; the second covers the installed plugin.
Local success does not establish live acceptance or Anthropic portal approval.

## Directory review

Use the intended publisher organization and the existing submission form. After
merging an update, change its source path to `plugins/motivs` and revalidate the
exact commit. Do not validate the repository root as a plugin bundle.

The legal publisher name **MOTIVS OÜ** and product website identify the real company.
A similarly named directory listing may still trigger manual review; this package
does not claim that the reviewer has approved the name or verified the organization.
