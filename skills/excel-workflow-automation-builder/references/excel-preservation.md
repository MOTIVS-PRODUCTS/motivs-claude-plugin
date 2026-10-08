# Excel Preservation

Use this reference when reading, writing, comparing, or preserving workbooks and templates.

## Preservation Requirements

Never modify original input or template files. Work on copies.

Use Motivs' normalized Parquet regions for data transformation when available. Use the raw workbook path only for structural inspection or an explicitly required structure-preserving copy. `python-calamine` is a read-only fallback; never use a fallback read as evidence that charts, macros, links, pivots, styles, or other workbook features can be safely written back.

Do not open and save a customer workbook merely to normalize it. `openpyxl` does not preserve every Excel feature. When unsupported or preservation-sensitive features are detected, generate a separate output workbook or block the output with a clear limitation unless the confirmed specification defines a verified preservation path.

Preserve, as far as technically possible:

- Workbook type, sheet order, sheet names, and workbook properties.
- Formulas, styles, fonts, fills, borders, number formats, alignment, merged cells, row heights, and column widths.
- Hidden sheets, rows, and columns.
- Print areas, page setup, named ranges, Excel tables, freeze panes, conditional formatting, and data validation.
- Charts, pivot-table structures, workbook protection, cell protection, and macros where supported.

Prefer named ranges, Excel tables, labeled sections, and stable identifiers over hardcoded coordinates. Store unavoidable coordinates in versioned output mappings.

Identify cells and ranges that must never be overwritten.

Do not introduce new styles, sheets, formulas, decorative formatting, or AI-style layouts unless the workflow explicitly requires them.

## Output Template Changes

When a template changes, compare workbook type, sheet names/order, named ranges, Excel tables, headers, formulas, merged cells, hidden rows/sheets/columns, row heights, column widths, number formats, print areas, page setup, charts, pivots, conditional formatting, data validation, frozen panes, external links, formulas referring to other sheets, macros, workbook protection, inserted objects, output cells, protected cells, and cells that must never change.

Create a new template version, preserve the previous mapping, run historical reproduction tests, and block release if the new template cannot be populated safely.

## Formula Handling

Many Python Excel libraries do not calculate formulas. For each workflow, define whether formulas should be:

- Preserved only.
- Written but not recalculated.
- Calculated in Python.
- Recalculated using installed Microsoft Excel.
- Replaced with values.
- Validated against known control cells.

Never assume that writing a formula means the displayed value has been recalculated. `openpyxl` can inspect formula text and cached values saved by Excel, but it does not guarantee live Excel calculation. When recalculation is required, test the selected method on the target Mac using Microsoft Excel, LibreOffice, or another verified calculation engine. If no verified recalculation path exists, mark formula recalculation as `not verified` and block success when the workflow depends on it.

## Macro Handling

Detect macros in XLSM files. Default behavior is to preserve macros where technically possible, not execute them, warn the user, verify the output remains XLSM, and compare macro-presence metadata before and after processing.

Execute a macro only in Excel-assisted mode when the macro is specifically identified, trusted, approved, logged, and required for safe completion.

## External Links And Queries

Detect external workbook links, data connections, Power Query, linked pivot sources, and linked charts. Do not refresh external connections silently. Explain whether the workflow preserves, refreshes, replaces, or cannot safely support the connection.

## Output Validation

After writing outputs, reopen them and verify that files open, required sheets/tables/named ranges exist, row counts and control values are present, protected areas remain intact, formulas and macros remain where required, filenames are correct, and output hashes are recorded. Record whether formulas were preserved only, recalculated externally, calculated in Python, replaced with values, or not applicable.
