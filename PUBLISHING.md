# Anthropic submission and release

## Status

This repository is prepared for a first submission, not a published directory
listing. Local checks cover package structure and selected invariants only. They
do not establish live workflow success, legal compliance, or Anthropic approval.
No reviewer account, compliance attestation, or demo evidence is supplied here.

## Source and identity

- Repository: `MOTIVS-PRODUCTS/motivs-claude-plugin`.
- Plugin path: `plugins/motivs`. Enter it explicitly in the portal.
- Publisher: **MOTIVS OÜ**, the company behind [motivs.ai](https://motivs.ai).
  Motivs is the product and company brand; keep the identifier and display name.
- Plugin and marketplace name: `motivs`. Preserve this identity for updates.
- Current package version: `0.7.4`; increase it for every shipped package change.
- First source candidate: merge the reviewed release PR, then validate the exact
  resulting commit on `main`. Record that commit and version with the submission.
- The skill baseline is the production 0.7.1 integration, with the pin-authority
  wording corrected here to include the workspace Owner. Future synchronization
  must preserve this correction until the upstream skill also includes it.
- The public repository contains no review credentials. Provide any required
  access through the portal's intended private process, never through Git.

## Local preflight

Run from the repository root:

```sh
python3 scripts/check_package.py
claude plugin validate . --strict
claude plugin validate plugins/motivs --strict
```

The first validator command covers the marketplace manifest; the second checks
the installable plugin manifest explicitly. Use a current Claude Code version that recognizes
the directory listing fields.
Review the diff, license, README, public support and policy links, and runtime
instructions. Keep private notes, credentials, OS metadata, generated ZIPs,
dependency folders, and build artifacts out of the source repository.

The Python checker uses tracked files plus non-ignored untracked files inside
`plugins/motivs`, so stage all intended files before release. It also checks that
the root marketplace resolves to that folder. Maintainer tooling, CI and this guide
stay outside the installed package. Original Python helpers stay in
`development/helpers` for maintainers only and are not referenced or fetched by
the installed skill. It checks structure, endpoint identity, paths,
file limits, icon format, reference existence, allowed text/image types and selected access
and privacy rules. It does not perform a security audit or the portal's full scan.

## Live acceptance checklist

These are required manual checks for this release, not claims of tests already
performed. Use isolated test resources and synthetic examples in Motivs. Record
host version, package version, exact source commit, expected result, actual result,
and evidence for each case. Keep credentials and protected contents out of evidence.

- [ ] Clean install and OAuth on each intended host: confirm workspace, role, and
      scopes without exposing profile details. Check the expected skill is loaded.
- [ ] Find an editable draft by exact name, confirm its brief, build a candidate,
      validate it, and deliver its authenticated Motivs URL.
- [ ] Repair a failed candidate from its exact source and failed run; the working
      version stays unchanged until explicitly selected by an authorized user.
- [ ] Owner and shared editor discovery use current capabilities. A run-only
      member is refused editing and no unauthorized source is retrieved.
- [ ] Automation owner and workspace Owner can explicitly select a validated
      working version when `access.can_pin` is true. A delegated editor cannot.
- [ ] Two edits from the same parent produce independent candidates. Validating
      either does not implicitly publish, overwrite, or reparent the other.
- [ ] An archived or inaccessible resource is described as unavailable. The skill
      does not create a substitute, restore it, or change workspace to bypass access.
- [ ] A revoked grant or stopped run cannot be bypassed through old links, retries,
      another version, or repair output. Current authorized resources still work.
- [ ] Owner administration does not expose another person's protected results.
- [ ] Protected examples, raw logs, cell values, and finished reports are never
      requested in the assistant conversation. Reports are delivered in Motivs.
- [ ] Password reset/revocation requires normal reauthorization when rejected.
      Reconnect through client settings, verify the workspace, and repeat a read.

## First submission

1. Use the intended publisher organization at
   [the developer portal](https://claude.ai/directory/manage). The first
   organization to submit this repository folder owns its directory listing.
2. Connect a GitHub account with push access. Choose **Plugin bundle**, the
   repository above, the plugin path `plugins/motivs`, and the reviewed branch or tag. If using
   `main`, confirm the merged commit is the intended release.
3. Run portal **Validate**. Resolve blocking findings and revalidate the new
   commit. A local pass does not replace portal validation or its security scan.
4. Submit the owned remote MCP server separately as an **MCP connector**, using
   `https://mcp.motivs.ai/mcp` and the same publisher organization. Check for an
   existing connector listing first; do not create a duplicate.
5. Review the listing fields from `plugin.json`. The responsible owner supplies
   the compliance contact, truthful data handling answers, required attestations,
   and any reviewer instructions requested by the portal. Do not invent evidence.
6. Review the publication/update setting before submission. Record portal status,
   exact source commit, package version, and all remaining findings. Publish only
   after the responsible owner approves the concrete listing and review result.

## Current portal findings

The first validation of 0.7.2 passed structure checks and reported policy holds.
The maintainer checker was then inside the installable root and read the manifest
and icon for preflight checks. In 0.7.3 that checker and CI stay outside the plugin
folder. The logo is still declared by the manifest and displayed with normal
Markdown image syntax. No plugin code executes the logo.

The name Motivs is intentional: it is the product and company brand of MOTIVS OÜ,
whose public product website is https://motivs.ai. If the directory flags a similar
name, provide this publisher context through its review process. Do not rename
the brand, claim registered trademark rights, or claim organization verification
without supporting evidence. Manual approval may still be required.

Directory listing URLs and the icon are intentional metadata, even if a released
Claude Code build ignores them at load time. Keep them.

The portal subsequently refused local executable files for the current
non-Verified publisher. Version 0.7.4 removes the three Python helpers from the
installed package and replaces their workflow dependencies with platform-side
validation. They are not renamed to text, embedded as complete runnable programs,
or fetched from another location by the skill. Original maintainer utilities live
outside the submitted plugin folder. No Verified-organization status is claimed.

Only supported Markdown, text, JSON, YAML and image files belong in the plugin
folder. Text must be UTF-8, contain no NUL bytes and not start with a shebang. Do
not include package-manager configuration, dependency installers or executable
permission bits. The source checker rejects these regressions before CI passes.
The portal result remains authoritative; a local pass is not clearance.

After merge, confirm the source path in the existing form to `plugins/motivs` and
choose Re-validate. A local check cannot establish that either hold disappeared.
Do not submit a second listing or mark the package approved based on this change.

## Updates and rollback

A listing follows its configured branch or tag. New commits can trigger scans
and, depending on its publication setting, publication. Review that setting before
merging future changes. Revalidate the exact commit; earlier validation does not
cover later edits.

For a package rollback, revert the package content in a reviewed PR and assign a
new higher version so clients can receive the correction. Record both source
commits. Restoring this plugin does not roll back the hosted platform, its
migrations, users, automations, or reports; those have a separate release process.

## Official references

- [Submission](https://claude.com/docs/plugins/submit)
- [Pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist)
- [Manifest reference](https://code.claude.com/docs/en/plugins-reference)

Requirements and portal results can change; check these references again when
submitting. This checklist does not promise acceptance or a review deadline.
