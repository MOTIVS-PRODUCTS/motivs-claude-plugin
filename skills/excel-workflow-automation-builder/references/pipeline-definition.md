# In-Notebook Pipeline Definition

Use this reference when defining data contracts, rules, and transformations.

## Configuration Lives In The Notebook

Represent workflow behavior with Python objects inside the notebook:

- Constants for automation name, version, output folder, and supported file types.
- Dictionaries/dataclasses/Pydantic models for input contracts.
- Alias maps for column names.
- Lists of validation and reconciliation controls.
- Plain-language rule descriptions near the functions that implement them.
- A small `USER_DECISIONS` or `APPROVED_RULES` structure for confirmed decisions.

Do not create separate YAML, JSON, TOML, or config folders by default.

## Runtime Capabilities

At the top of the notebook, detect and display runtime capabilities:

- Required: `marimo`, `pandas`, `openpyxl`.
- Preferred optional: `duckdb`, `pandera`, `pyarrow`.
- Workflow-specific optional: `xlsxwriter`, Microsoft Excel, LibreOffice. `python-calamine` belongs to the platform's read-only fallback and should not be added to automation runner requirements.

The notebook should continue with deterministic fallbacks when possible. If a missing optional dependency materially reduces validation or scalability, show a warning in the UI and record it in the audit log. Ask before installing dependencies.

## Data Contracts

For each input dataset, define in the notebook:

- Business purpose.
- Required and optional fields.
- Accepted aliases.
- Types and parsing rules.
- Key fields and uniqueness rules.
- Nullable/default behavior.
- Sensitivity notes.
- Validation controls.

Never force ambiguous data into a role without confirmation.

Use Pandera schemas when available for serious DataFrame contracts. Keep a plain-Python fallback for required columns, key uniqueness, nullable behavior, and type parsing so the notebook remains runnable without extra installation.

## Pipeline Shape

Define the pipeline as a short list or dictionary of stages in the notebook. Each stage should include a plain-language name, function, inputs, outputs, validations, exception behavior, and row-count/control reporting.

Use local helper functions for:

- File detection.
- Header detection.
- Column normalization and alias mapping.
- Type parsing.
- Cleaning/filtering/deduplication.
- Joins/lookups.
- Aggregation/pivoting/reshaping.
- Template population or report writing.
- Reconciliation and output validation.

Prefer obvious, boring functions over generic engines. A single clear function is better than a framework.

Use DuckDB when installed for:

- Large CSV scans and row counts.
- Multi-file unions and reconciliations.
- SQL-style joins/lookups that need explicit matched/unmatched counts.
- Aggregations and control totals that can be expressed more clearly in SQL than pandas.

Keep DuckDB usage inside notebook helper functions. Use explicit local connections, register DataFrames or query local files, close connections, and avoid hidden persistent databases unless the user explicitly asks for one.

## Large Data

For large CSVs, prefer DuckDB when installed, then `pandas.read_csv(..., chunksize=...)` when needed. Read only required columns where safe. For large Excel files, inspect workbook structure first and load only relevant sheets/ranges. Prefer local path/file-browser inputs over browser uploads for very large files. If local memory is insufficient, fail clearly and propose a bounded local strategy before adding dependencies.
