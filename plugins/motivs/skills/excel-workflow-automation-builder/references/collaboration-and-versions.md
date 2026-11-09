# Collaboration, source versions, and working pins

## Workspace and rights

Read `connection_status` first. Its organization includes `collaboration_enabled`; its scopes are OAuth limits, not authority to every resource. Use current capabilities from `get_automation` and `list_folders`.

In collaboration workspaces the workspace roles are Owner and Member. Every active Member can create a folder or an automation without a folder. An optional selected folder requires `access.can_create`. Creation in a folder does not grant access to another person's automations. `use` permits ordinary execution; `manage` permits source inspection, metadata/code changes, and validation. A workspace Owner has administrative management. The automation owner and workspace Owner can change the working pin when current `access.can_pin` permits it; delegated editing access alone does not grant this capability. Permission-management authority does not imply access to another person's protected inputs or outputs.

Search uses current rights and may include an automation created by a colleague when editing access is assigned. Legacy workspaces may still use owner-scoped discovery. Missing or forbidden resources do not prove absence. Do not switch workspace, create a replacement automation, elevate permissions, or request protected files to bypass a refusal. Workspace invitations and resource Access are managed in Motivs; there is no old Share tool to substitute for them.

When `access.can_manage` is false, stop an edit request before requesting source or submitting changes. Tell the user in their language: "You have permission to run this automation, but not to edit it. Ask its owner for editing access." Creating your own automation does not authorize changing this one. If an operation returns an access refusal after an earlier successful read, honor the new refusal immediately.

For an unavailable resource (404), say that the automation is unavailable to the current connection and access may have changed; do not claim it was deleted or that the whole account is disabled. For an authentication rejection (401), explain that the connection is no longer authorized and the user should check workspace membership with the Owner before reconnecting. Only describe an account as suspended when the server explicitly confirms that status. Never include an account email or other personal profile details in these messages.

## Optional folders

Preserve existing folder membership unless the user asks to move the automation. Do not create a default folder or move old unfiled resources. `create_automation` accepts no `folder_id`; a supplied folder must permit creation. `update_automation_metadata(clear_folder=true)` explicitly moves an editable automation to no folder. Never combine it with a destination `folder_id`. Use this only for a requested move.

## Select the exact source

A version number is local to one automation. Resolve it through that automation's version metadata, then call `get_automation` with its exact `version_id`. If the user specifies v6, do not substitute v7, the latest candidate, or the working pin. If the source is not specified and there are meaningful alternatives, ask which version to continue. Do not invent historical parents when metadata is missing.

Before editing an existing version, obtain its authorized source with `create_repair_package(automation_id, version_id=...)`. For a repair, also provide the exact failed `run_id`. The package may include code/manifest and approved metadata, never protected source rows, cell values, or generated report contents. Reuse only the selected source, not another candidate's implementation.

Save each change as a new immutable version. For an existing collaboration automation pass the selected `parent_version_id`, a short factual `change_summary`, and the committed current `contract_revision_id` when a protected contract exists. A genuinely empty draft has no parent. Validate the exact returned candidate ID, then poll that run. Parallel candidates may share a parent; neither automatically becomes the other's parent.

## Validation and working version

A passed validation is distinct from the working pin. In collaboration workspaces ordinary runs use only `pinned_version_id`. A new version, passing validation, a greater version number, or `latest_version_id` does not replace that pin. Do not try to change the pin through metadata fields. Direct a user with current `access.can_pin` (the automation owner or workspace Owner) to the explicit version selection in Motivs when a change to the working version is intended; do not pin on the user's behalf by implication.

Handoff states the candidate version and its source, summary, validation result, and the currently pinned version. Say clearly when the validated candidate is not yet used for runs. A missing or unvalidated pin, or an archived automation, blocks ordinary runs; never select a fallback automatically. Legacy auto-publication applies only when `collaboration_enabled` is false.

## Archive and revocation

Versions are immutable history and are not archived or restored individually. An active automation keeps all its versions available to authorized editors; its working pin remains an explicit choice by a user with current `access.can_pin`. Historical version archive markers do not make a version unavailable under this policy. An archived automation is unavailable as a whole, including through source/repair tools.

`list_archived_items` returns `automations` and `folders`, never an independent versions collection. It returns only authorized metadata. Current editors can restore an automation in Motivs; a folder's creator or a workspace Owner can restore that folder and its archive package. Folder lifecycle authority does not imply permission to read or edit every automation inside it.

Archiving a folder also archives its active automations without changing their IDs, versions, files, history, grants, ownership, or pins. Restoring one of those automations separately returns it to the root Automations list. Restoring the folder reunites the same automations, including those already restored to the root. If a user explicitly moved one into another folder, that new placement is preserved. Refresh metadata after restoration; do not guess the current folder or move a restored item automatically.

If discovery fails because an automation or folder is archived, explain the explicit restore action in Motivs. Never restore, recreate, select a different automation/version, or change folder placement to bypass an archive or access refusal. Source version IDs and parent relationships remain unchanged after restore.

A revoked grant or suspended membership stops affected queued/running jobs. `stopped` is terminal for that run, even if access is later restored. Do not treat it as validation failure to repair around, reuse an old token/link, retry execution without current authority, or retrieve the output by another route. Ask for the relevant access or a fresh connection when required. Other authorized resources and independently accepted delegations are not automatically revoked.

## Data boundary

Owner or manage rights do not grant the plugin permission to read protected input examples, raw logs, hashes, credentials, or finished reports. Keep those inside Motivs. Use metadata-only build context and structured run feedback; hand off the authenticated Motivs URL for report delivery. Changing folder, version, role, archive state, or pin never relaxes this boundary.
