# Platform UI Contract

Use this reference when defining the employee-visible behavior of a Motivs automation. Motivs Platform owns the interface. The generated notebook owns backend logic, validation evidence, and output metadata.

## Ownership Boundary

The automation must provide:

- `manifest.json` definitions for inputs, parameters, actions, steps, and outputs.
- A top-level `run_automation(input_paths, output_dir, parameters)` adapter.
- Plain-language status, warnings, validation facts, and output metadata.
- Technical diagnostics suitable for the platform's Show work area.

The automation must not provide:

- Custom employee-facing Marimo layouts.
- Custom CSS or workflow-specific frontend shells.
- Local upload widgets, local filesystem selectors, or desktop paths.
- A replacement navigation, tab system, results page, or download experience.

## Default Information Architecture

The platform should render every automation with the same sequence:

1. Automation name, short purpose, version, and current status.
2. Compact workflow steps such as `Add files`, `Check files`, `Review issues`, `Create output`, and `Download results`.
3. Employee inputs and parameters generated from the manifest.
4. A primary action using business language such as `Generate report` or `Build reconciliation`.
5. Readiness and validation status with the exact next action.
6. Results with prominent authenticated downloads.
7. Show work with profiles, rules, checks, logs, and maintainer diagnostics.

Do not turn this into a landing page, decorative dashboard, or raw notebook. Routine users need a controlled work surface for repeated execution.

## Manifest Requirements

- Use `ui.mode = "platform-rendered"`.
- Keep labels concise and business-friendly.
- Declare accepted file extensions, multiplicity, and required state for every file input.
- Use explicit parameter types and defaults.
- Expose one clear primary run action unless the workflow genuinely has separate operations.
- Declare every expected downloadable output with a stable ID, label, and file type.
- Keep internal paths, object keys, dependency details, and tracebacks out of employee-visible fields.

## The Layout of the Finished Report

Each entry in `expected_output_blueprints` carries a `layout`: the shape Motivs compares the generated report against. Build to it rather than guessing, because validation checks formatting as well as values, and the protected example itself is never visible.

For a workbook, each sheet states:

| Field | Meaning |
|---|---|
| `header_row`, `data_start_row` | which row holds the column names, and where records begin |
| `dimensions` | rows and columns the finished example occupies |
| `columns[]` | `position`, `letter`, `name`, `number_format`, and `width` where one is set |
| `merged_ranges`, `freeze_panes` | merged areas and the frozen pane, as refs |
| `header_style` | bold, italic, size, fill pattern, alignment, and whether the whole header row shares one style |
| `rows_above_header[]` | one entry per row above the table |
| `record_count` | rows of data in the example |

A CSV layout carries `columns[]` and `row_count`.

`rows_above_header` describes a preamble without quoting it: `occupied_cells`, `merged_ranges`, `first_occupied_column`, `content_kind` (`text` or `value`) and `style`. That tells you a title belongs in row 1, merged across the table, bold at 14pt — and you write the wording yourself from the task. The text is withheld deliberately: a report title routinely carries the customer's own name, and disclosing it would put source content in the agent's hands.

Reproduce a preamble row by count and position. When it holds more than one occupied cell, `occupied_columns` lists the letter of every one — a row with `occupied_cells: 2` at `["A", "B"]` is a caption cell in A and a value cell in B, and writing only B leaves a missing cell that validation charges to the sheet. The row-level `style` is the first occupied cell's; when the cells differ in style, `columns` carries a per-cell `{letter, style}` list, the same shape `header_style` uses.

When `described` is `false`, the example is a format Motivs cannot describe. Say so in your report rather than inventing a layout.

## Declaring What the Result Means

Declare `verification.grain` at the top level of the manifest, next to `ui`. State it
from the task description, **before writing the automation code**. It is what the
platform checks the finished result against, so deriving it from a finished output
would check the code against itself.

```json
{
  "verification": {
    "grain": {
      "columns": ["product", "month"],
      "phrase": "product and month"
    }
  }
}
```

- `columns` names the result columns whose combination must not repeat. A join that
  multiplied rows, or an aggregation that lost groups, is caught here and nowhere else.
- `phrase` is a noun phrase naming what one result row stands for. It is printed to the
  person reading the result as "Each *product and month* appears exactly once", so write
  it to fit that sentence. English only.

Pick the grain from what the report is about:

| Automation | Grain columns |
|---|---|
| sales summary by product per month | product, month |
| list of active customers | customer id |
| payroll per employee for a period | employee id |
| stock levels per warehouse on a date | warehouse, item, date |
| pass-through export of payments | payment id |

When duplicates are legitimate, for example concatenating two files without
aggregating, omit `verification` entirely. The result then gets the standard frame
report, capped at yellow: identifiers and coverage are still traced, duplicates and
arithmetic are not. Never invent a grain to make the check appear.

### A result of several sheets

A bare `grain` describes a result of one table. When the automation writes a workbook
of several sheets, each sheet stands for something different and declares its own
grain under `verification.sheets`:

```json
{
  "verification": {
    "sheets": [
      { "name": "Top 10", "grain": { "columns": ["item"], "phrase": "product" } },
      { "name": "Daily trend", "grain": { "columns": ["date"], "phrase": "day" } }
    ]
  }
}
```

- `name` must match the worksheet title exactly, including case and spacing.
- Declare **every** sheet the automation writes. A sheet nobody declared is reported
  as unchecked and holds the verdict below green, because checking four sheets of five
  and calling the result verified is the one answer this must never give.
- A sheet that genuinely has no row grain, a chart sheet or a heat map, has nothing to
  declare. Leave it out and accept the lower verdict rather than inventing a grain for
  it.

Use `sheets` or a bare `grain`, never both. A bare grain against a workbook of several
sheets matches nothing and the result is reported as not checked.

### When the report renames the identifier

Tracing works by column name: the identifier in the result must exist in the input
under the same name. A report often speaks the reader's language while the export
speaks the vendor's, so the grain can declare where a renamed identifier comes from:

```json
{ "grain": { "columns": ["Позиция"], "phrase": "inventory item",
             "sources": { "Позиция": "Item name" } } }
```

Each `sources` key must be one of the grain columns; the value is the input column it
is traced from. Columns without an entry trace by their own name, as before. Declare a
source only for a genuine rename of the same identifier, never to point one entity at
a different one.

The declaration is refused at upload if `columns` is empty, repeats a name, or `phrase`
is missing, and no automation version is created.

### Declaring arithmetic

A grain says a result has the right shape. It says nothing about whether the numbers
in it were added up correctly, which is why a result with only a grain is reported as
`Shape only` and never reaches green. A reconciliation is what carries a verdict to
green: the platform recomputes the measure from the input itself and compares.

```json
{
  "verification": {
    "grain": { "columns": ["Category"], "phrase": "product category" },
    "reconciliations": [
      {
        "measure": "Net Sales",
        "equals": "net_sales",
        "columns": { "net_sales": "Net Sales" },
        "phrase": "net sales recomputed from the line entries",
        "tolerance": 0.05
      }
    ]
  }
}
```

- `measure` is the **result** column whose values are summed. Write it exactly as the
  result spells it, spaces and all.
- `equals` is an expression computed over every **input** row. Columns, numbers, `+`,
  `-`, `*` and a leading minus, nothing else. No function calls, no conditionals: a
  richer language would put you back to writing the code the check is meant to check.
- `columns` maps each name in the expression to the input column it stands for. The
  expression is parsed as Python, so a column named `Net Sales` cannot be written in
  one — the alias bridges that. Real column names are untouched everywhere else.
- `phrase` is printed next to the numbers: "*net sales recomputed from the line
  entries*: 17.95, recomputed 17.95, difference 0". English only.
- `tolerance` is an absolute amount, defaulting to 0.01. Money summed over thousands of
  rows rounds; see `references/verification-catalogue.md` for what to use per form.

Both routes have to reach the same number. The first is the sum of `measure` over the
result; the second is `equals` evaluated over the input by the platform, never by your
code. A check whose columns are missing from the run's file is reported as a blind
spot rather than silently skipped.

In a workbook, a sheet declares its own checks beside its own grain:

```json
{ "name": "Summary", "grain": { "columns": ["Category"], "phrase": "product category" },
  "reconciliations": [ { "measure": "Net Sales", "equals": "net_sales",
                         "columns": { "net_sales": "Net Sales" },
                         "phrase": "net sales recomputed from the line entries" } ] }
```

### When the report splits a flow into parts

A sales report keeps refunds in their own column. Summing the sales column alone comes
up short by exactly the refunds, and the certificate reports that as a difference the
automation never made. The expression deliberately has no conditionals, so it cannot
say "rows that are not refunds" — it does not need to, because the report already
separated the parts and the check can add them back:

```json
{ "measure": "Net Sales",
  "measure_parts": ["Net Sales", "Refund Amount"],
  "equals": "net_sales",
  "columns": { "net_sales": "Net Sales" },
  "phrase": "sales and refunds together check out against the line entries" }
```

`measure_parts` lists **result** columns that add up to the whole. Not an expression:
you name the columns the report divided the flow into, and the platform builds the sum.
Leaving a part out still fails, by exactly what was left out.

### A sheet of totals rather than rows

A summary sheet is usually a card: one line per metric, the name on the left and the
number on the right. It is not a table and has no grain, so read as one it yields a
header made of the first metric and its value — which names nothing and can be checked
against nothing. Declare it for what it is:

```json
{ "name": "Summary", "shape": "card",
  "reconciliations": [
    { "measure": "Net Sales",
      "measure_parts": ["Net Sales", "Refund amount"],
      "equals": "net_sales",
      "columns": { "net_sales": "Net Sales" },
      "phrase": "the reported totals together match every line entry" } ] }
```

- A card declares no `grain`: it holds one row, so uniqueness says nothing.
- A card must declare at least one check. Without one it is held to nothing, and that
  is refused at upload.
- The metric names on the left become the column names. Write them exactly as the sheet
  spells them, including case: `Refund amount` and `Refund Amount` are different names.
- Reading stops where the card does. A small table below the metrics is reported as
  unchecked rather than folded in, and the certificate says so.

Everything else stays a `table`, which is the default and needs no `shape`.

**Write values, not formulas, into any column a check measures.** A formula written by
a library carries no computed value beside it, so the platform reads the cell as empty
while a spreadsheet shows a number. Rather than report a difference your automation
never made, the check stands down and the certificate says the arithmetic was not
checked. Formulas elsewhere in the workbook are fine.

Declare a check only when it is genuinely true of the task. Never weaken a tolerance
until a wrong result passes: a green verdict that was bought is worse than a yellow
one that was honest.

## Run and Readiness States

The backend result must let the platform distinguish:

- Waiting for required files.
- Ready to run.
- Running checks.
- Creating output.
- Passed with downloads.
- Passed with warnings.
- Failed with a user-correctable issue.
- Failed with maintainer intervention required.

Return stable status values and structured facts rather than asking the platform to parse prose.

Useful facts include files received, rows detected, rows written, issues found, checks passed, warnings, formula recalculation state, output hashes, and output IDs.

For planning, prediction, scenario, or decision workflows, keep analytical methods internal. The main result may add one outcome sentence, feasibility or suitability state, the next action, and material warnings. Never add an employee-facing method selector. Put method family, baseline, sensitivity, and diagnostic bands in Show work.

## Results and Downloads

After success, the employee-facing result should show:

- Output filename and type.
- Creation time.
- Rows or records processed when meaningful.
- Required checks passed and warnings remaining.
- Formula recalculation status when Excel formulas exist.
- One obvious download action per declared output.

Return output paths only in the structured `outputs` map used by the platform. The platform must convert them into authenticated downloads. Never present a local path, container path, storage key, or presigned URL as the primary result text.

## Show Work

The Show work area should make the automation inspectable without overwhelming routine users. Supply structured evidence for:

- Input file classification and bounded profiles.
- Confirmed and inferred business rules.
- Schema, type, key, duplicate, and join checks.
- Reconciliation controls and tolerances.
- Workbook preservation and formula findings.
- Stage logs and elapsed times.
- Output verification and hashes.
- Warnings, unsupported features, and maintenance notes.

Code snippets may be shown when they help an engineer repair the workflow, but the main result must remain outcome-focused.

## Error Contract

Return plain-language errors with a stable error code and structured details. Explain what the user can do next.

Examples:

- Missing column: name the required field and likely source aliases.
- Type mismatch: summarize the values or rows that could not be parsed.
- Workbook failure: identify password protection, corruption, encryption, or an unsupported feature.
- Reconciliation failure: name the failed control, expected value, actual value, and difference.
- Dependency limitation: identify the missing capability and whether the platform runner can supply it.

Keep raw tracebacks and internal exception text in maintainer diagnostics only.

## Visual and Workflow QA

Platform UI changes must be checked at desktop and mobile widths. Reject a release if controls overlap, labels fragment, result downloads are hard to find, long filenames break layout, developer noise dominates the page, or empty space hides the next action.

Automation validation must confirm that its manifest renders with the standard platform shell and that every declared input, action, and output maps to real backend behavior.
