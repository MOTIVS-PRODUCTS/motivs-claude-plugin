# Workflow Discovery

Use this reference when creating a workflow from historical spreadsheets or employee descriptions.

## Required Evidence

Require at least one complete example run inside Motivs Platform. Prefer two or more protected historical runs when the platform supports additional intake revisions.

Ask the user to protect any available evidence in Motivs Platform:

- Raw inputs.
- Intermediate files.
- Completed outputs.
- Blank templates.
- Written process notes.
- Screenshots of manual steps.
- Lookup, reference, or mapping files.
- Exception examples.
- Expected totals or control figures.

In the privacy-first workflow, inspect the current metadata-only automation contract before writing production logic. Motivs inspects protected examples internally and validates the generated version against them after upload. Do not request or inspect protected rows or cell values through the AI host.

Only inspect files directly when the user deliberately supplied them to the AI host and confirms that their organization permits that data path.

## Artifact Classification

For each contract source, inspect its disclosed filename, format, logical workbook regions, sheet visibility, field names, type and presence classifications, scale bands, formula/cache status, preservation risks, and candidate relationships. Classify it as input, lookup, intermediate, explicit runtime template, expected-output example, notes, mapping file, or unknown. An expected-output example is never a runtime template unless the committed specification explicitly reclassifies it.

Show classification and confidence. Ask the employee to correct uncertain classifications.

## Interview Style

Ask business questions, not programming questions.

Use questions like:

- What starts this workflow?
- How often does it run?
- Which files are required and where do they come from?
- What uniquely identifies one record?
- When the same record appears in two files, which value should win?
- When this amount is blank, should it be treated as zero, left blank, or sent for review?
- Which totals do you check before trusting the workbook?
- Which workbook areas must never be changed?

Ask one logical group of questions at a time. Use multiple-choice answers when possible. Explain why each question matters. Avoid asking for information that can be reliably inferred from examples.

Label inferred rules exactly:

```text
Proposed rule - needs confirmation
```

Do not begin final production implementation until material rules have been confirmed.

## Manual Workflow Decomposition

Decompose the process into explicit stages. Common stages:

1. Input acquisition.
2. File identification.
3. Workbook and sheet selection.
4. Header detection.
5. Data extraction.
6. Type parsing.
7. Field renaming.
8. Standardization and cleaning.
9. Filtering.
10. Deduplication.
11. Lookup enrichment and joins.
12. Appending or splitting.
13. Calculations.
14. Classification.
15. Grouping and aggregation.
16. Pivoting or unpivoting.
17. Sorting.
18. Allocation.
19. Exception detection.
20. Reconciliation.
21. Output mapping.
22. Workbook population.
23. Formula recalculation.
24. Final validation.
25. File naming, archiving, and audit logging.

For every stage, record stage ID, plain-language name, purpose, input dataset, output dataset, transformation type, business rule, validation rule, exception behavior, lineage behavior, whether it is configuration-driven, and whether custom Python is required.

## Historical Reverse Engineering

Use the contract and protected-validation feedback to infer candidate steps, mappings, filters, formulas, lookups, and exception rules. Treat every inferred material rule as unconfirmed until the employee approves it.

Never treat structural similarity as proof of correctness. Motivs must compare protected values, formulas, row counts, controls, and formatting internally when a finished-report example exists; the agent uses the resulting issue codes and never receives those protected values.
