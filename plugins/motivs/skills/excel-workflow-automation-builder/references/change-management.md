# Change Management

Use this reference when the automation needs repair or updates.

## Edit The Same Notebook

Maintenance means updating the single Marimo notebook. Do not create a new project, new workflow folder, migration system, or separate config layer by default.

When inputs, templates, or rules change:

1. Reproduce the issue in the notebook.
2. Identify the first failing section: file detection, contract, parser, transform, validation, reconciliation, or output generation.
3. Show the evidence in business language.
4. Update the smallest relevant in-notebook contract, rule, function, or UI element.
5. Add or update an in-notebook self-check for the failure.
6. Run `marimo check --strict`.
7. Run the notebook or affected self-checks.
8. Record the change in the notebook maintenance notes.

## Report To User

Explain exactly what changed, what was retested, whether historical outputs still match, and whether any manual decision remains.

## Immutable platform versions

Use `collaboration-and-versions.md` to select the exact parent, preserve its source identity, and record a factual change summary. Upload a new immutable candidate rather than editing an existing platform version. Validation and the working pin are separate in collaboration workspaces; archive restoration and pin changes are explicit actions in Motivs.
