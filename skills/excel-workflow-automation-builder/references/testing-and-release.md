# Testing And Release

Use this reference before declaring the notebook ready.

## In-Notebook Tests

Put tests inside the notebook, not in separate files by default.

Include a `run_self_checks()` function that verifies:

- Runtime capability detection works and warnings are visible.
- Required inputs can be detected.
- Required fields and aliases work.
- Type parsers preserve identifiers, dates, currency, percentages, and leading zeros.
- Duplicate and join controls behave as expected.
- DuckDB-backed reconciliation helpers work when DuckDB is installed.
- Pandera-backed validation helpers work when Pandera is installed, and plain-Python checks work when it is missing.
- Reconciliation controls catch failures.
- Report generation writes a valid output file.
- Generated output can be reopened and required sheets/control rows are present.
- Formula recalculation status is correctly reported as verified, not verified, not required, or externally required.
- Synthetic expected output matches within approved tolerances for the embedded self-check fixture.
- Ordinary reporting stays on `clean + reconcile` without advanced questions, methods, or controls.
- Selected planning methods satisfy every hard constraint or return an explicit infeasibility result.
- Selected prediction methods preserve time order, compare with required baselines, return a range, and fall back or refuse when their gate fails.
- Selected scenario methods reproduce with a fixed seed and demonstrate whether the action is stable or sensitive.
- Selected comparison methods preserve hard disqualifiers, confirmed directions, weights, missing-value rules, and deterministic ties.
- `analysis_summary`, when returned, uses `minimum-intelligence-v1` categorical values only.

Expose a `Run self-checks` control or run checks automatically before final output generation.

## External Checks

Run what the environment supports:

```bash
python -m marimo check --strict automation.py
python -m marimo run automation.py --headless --host 127.0.0.1 --port <free-port>
```

Also open generated Excel files with Python to confirm they are readable. For formula-dependent reports, verify recalculation with Microsoft Excel, LibreOffice, or a documented external method; otherwise mark recalculation as not verified.

## Platform Upload Checks

Before release:

- Create `automation.py`.
- Create `manifest.json`.
- Create `requirements.txt`.
- Create `profile.json` only for agent-owned synthetic or deliberately shared inputs; never reconstruct protected platform profiles.
- Create `validation_report.json` with checks run, checks skipped, blockers, and formula recalculation status.
- Commit the confirmed build brief, upload artifacts through `add_automation_version` with that exact `contract_revision_id`, then queue protected isolated validation and poll the durable run record. The upload is only a candidate; report publication only after the platform promotes a passing newest/current-contract version.
- Confirm the response includes automation ID, version ID, contract revision ID, platform URL, and validation status.
- Confirm protected-example execution passes and protected finished-report comparison passes when an example exists.
- Confirm the platform version validation status is `passed`, or report blockers and do not claim readiness.
- Confirm ordinary reporting validation omits `analysis_summary` and retains its previous response shape.
- For advanced workflows, confirm connected-tool validation includes only the platform-sanitized categorical `analysis_summary`; attempt numeric, free-text, field-name, path, and nested-object leakage before release.

Do not create or validate zip files, `Run.command`, `Run.bat`, desktop launchers, or local bundle folders as the handoff.

## Ready Definition

The automation is ready only when it is one contract-bound platform automation version with one notebook source file, uploaded to Motivs Platform, static checks pass, capability checks are reported, self-checks pass where runnable, protected-example execution passes, protected expected-output comparison passes when available, outputs reopen successfully, original files are untouched, critical issues block output, formula recalculation status is honest, and the platform URL is returned to the user.
