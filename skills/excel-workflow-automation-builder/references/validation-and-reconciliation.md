# Validation And Reconciliation

Use this reference when defining in-notebook checks, issue severity, audit records, or lineage.

## File Validation

Before processing, check required inputs, optional inputs, supported formats, openability, non-empty files, required sheets/tables/named ranges, required columns or mappings, header rows, duplicate uploads, correct template, password protection, macros, external links, and file hashes.

## Schema And Data-Type Validation

Detect required fields, optional fields, unexpected fields, renamed fields, removed fields, changed types, changed formats, changed sheet/table/header positions, key uniqueness changes, and nullable behavior changes.

Check that numbers, dates, datetimes, currencies, percentages, booleans, and identifiers parse safely. Preserve leading zeros where required. Apply configured blank-value and locale rules.

Prefer Pandera when installed for formal DataFrame schema validation, lazy error reports, range/category checks, and reusable contract checks. If Pandera is missing, implement explicit plain-Python/pandas checks for the same critical rules and show a runtime capability warning.

## Business Rules, Duplicates, And Joins

Validate workflow-specific statuses, exclusions, thresholds, effective dates, mappings, valid combinations, lookup completeness, approvals, sequence rules, balance rules, allocation rules, and period rules.

Do not remove uncertain duplicates automatically. Show them for review.

For every join or lookup, report rows before and after, matched rows, unmatched left rows, unmatched right rows, duplicate keys, one-to-many expansions, many-to-many joins, and unexpected row multiplication. Block unexpected multiplication unless approved by workflow governance.

Use DuckDB when installed for join/reconciliation checks that are clearer or safer in SQL. Keep counts explicit and compare DuckDB outputs against expected pandas row/control totals when the workflow is high-risk.

## Reconciliation Controls

Every notebook automation must define explicit success controls. Examples:

- Imported, processed, excluded, and output row counts.
- Input versus output totals.
- Category, period, sheet, and control-cell totals.
- Debit-credit balance.
- Beginning balance plus movements equals ending balance.
- Source records equal matched plus unmatched records.
- Allocation totals equal original totals.
- Lookup coverage.
- Exception counts.
- Expected file and output counts.

An automation is not successful until its controls pass or remaining differences are explicitly approved and documented.

## Severity System

Classify findings as:

- Information: visible but no action required.
- Warning: visible but may not block execution.
- Review required: human decision required before continuing.
- Critical: blocks final output generation.

Critical issues must never be bypassed with a generic `Continue anyway`. Overrides must be specific, justified, approved, recorded, associated with exact affected records or controls, and allowed by governance rules.

## Audit Logging

Create an in-notebook and optional local JSON audit record for every run with run ID, timestamp, notebook version, parameters, input filenames and hashes, classifications, schema/template/rule versions when applicable, validation findings, employee decisions, row counts by stage, control values, output paths and hashes, execution mode, and success/failure status.

Include dependency/capability status in the audit record: DuckDB available/used, Pandera available/used, formula recalculation method, Excel/LibreOffice availability when tested, and any fallback mode.

Do not log passwords, full card details, tokens, API keys, secrets, or unnecessary personal data.

## Lineage

Preserve traceability from outputs back to inputs. Where practical, normalized records include source file, source sheet, source row number, source record ID, transformation history, inclusion status, exclusion reason, and output destination. For aggregates, preserve a way to identify contributing records.
