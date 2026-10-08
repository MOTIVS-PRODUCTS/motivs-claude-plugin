# Platform Notebook Architecture

Use this reference when building the final automation.

## Default Deliverable

Produce one **Motivs Platform automation version**. Motivs Platform is the runtime, storage layer, sharing layer, run history, and repair surface.

The automation version contains:

```text
automation.py
manifest.json
requirements.txt
profile.json              optional but preferred
validation_report.json    required when checks were run
```

The only source/logic file is `automation.py`, a self-contained Marimo notebook. It is the app, pipeline, validation harness, report generator, and maintainer handoff.

Do not create zip files, `Run.command`, `Run.bat`, desktop launchers, local output folders as the handoff, project folders, page modules, engine packages, transformation packages, YAML configs, separate test files, or workflow registries.

If Motivs Platform cannot be reached, stop and report the blocker. Do not substitute a local bundle.

## Notebook Responsibilities

Keep these sections in the same notebook:

- Required platform backend adapter and an optional maintainer-only Marimo view.
- Contract-bound file handling for platform runtime sessions.
- Artifact profiling and classification.
- Runtime dependency/capability checks.
- In-notebook contracts and aliases.
- Transformations as local functions.
- Optional DuckDB helper functions for large data and reconciliation.
- Validation and reconciliation functions.
- Optional Pandera schemas for serious validation when installed.
- Excel/template handling.
- Output generation.
- Output-file reopening and verification.
- In-notebook self-tests.
- Audit summary and maintenance notes.
- Outcome/evidence contracts, minimum capability selection, and optional privacy-safe `analysis_summary` for advanced workflows.

Use section headings and Marimo cells for organization instead of folders.

## Platform Storage

The platform stores:

- Immutable automation versions.
- Immutable metadata-only automation contract revisions and version-to-contract lineage.
- Protected intake snapshots containing source and finished-report examples.
- Notebook, manifest, requirements, profile, and validation artifacts.
- Run records and logs.
- Output files created by runtime sessions.
- Repair packages for failed runs.

The agent reads only the current automation contract through MCP. Motivs maps contract source IDs to protected object-store files during build validation, runs the notebook in the isolated runner, compares expected outputs inside the platform, and returns structured metadata-safe feedback.

The notebook should write outputs and logs relative to the runtime workspace provided by Motivs Platform. Do not assume a user-owned desktop folder, local launcher, or local Python installation.

## Release Gate

Do not call the automation ready until:

- `marimo check --strict` passes.
- The notebook can launch through Motivs Platform runtime or the local platform smoke runner.
- Runtime capabilities are reported honestly.
- Ordinary reporting preserves the existing deterministic path; every advanced capability passes its routing and method-specific gate.
- Advanced protected validation returns only allowlisted categorical analysis diagnostics to the connected AI tool.
- Self-checks exist and pass where they can be run.
- Generated outputs from protected source examples are produced inside Motivs validation.
- Generated outputs reopen successfully.
- Output row/control counts are validated.
- Formula recalculation status is honest.
- The version is uploaded to Motivs Platform.
- The platform returns an automation ID, version ID, platform URL, and validation status.
- The version references the exact contract revision used to build it.
- Protected-example execution passes, and protected finished-report comparison passes when examples exist.
