# Scenario And Sensitivity Analysis

Use this reference only when uncertainty or interacting assumptions could materially change the requested action. Do not simulate merely to make a workflow appear sophisticated.

## Scenario Contract

Confirm:

- Decision or plan being stress-tested.
- Inputs allowed to vary and inputs fixed by policy or contract.
- Base values and the source of each assumption.
- Plausible lower and upper bounds.
- Relationships or dependencies between inputs.
- Output or threshold that would change the action.
- Required reproducibility and approval policy.

Never invent probability distributions from minimum, maximum, and most-likely values without approval. Never imply a scenario probability when the inputs are only illustrative.

## Escalation Ladder

Use the first method that answers the question:

1. Single explicit what-if calculation.
2. Base, upside, and downside cases.
3. One-variable sensitivity table.
4. Small multi-variable grid for interacting assumptions.
5. Break-even analysis for the threshold that changes the action.
6. Empirical bootstrap from relevant historical residuals.
7. Bounded Monte Carlo only when distributions and dependencies are defensible.

Stop when additional sophistication does not change or clarify the decision.

## Bounded Monte Carlo

When Monte Carlo is justified:

- Use an explicit seed for reproducibility.
- Cap draws to the smallest number that stabilizes the requested percentiles within runtime limits.
- Prefer empirical resampling when relevant history exists.
- Preserve correlations through joint row or residual-vector resampling when independence is not defensible.
- Apply confirmed physical and business bounds.
- Report percentiles or threshold frequencies, not false probabilities of success.
- Record assumptions and seed in maintainer diagnostics.

Use `scripts/intelligence_kernels.py` as vetted build-time reference for reproducible sensitivity and empirical bootstrap patterns. Copy only required functions into the notebook.

## Decision-Relevance Gate

Compare the recommended action across the tested range. If it does not change, say that the decision is stable across the approved assumptions. If it changes, identify the smallest assumption movement or break-even point that changes it.

Do not surface a large scenario table when the employee only needs the stable recommendation and material boundary. Keep details in the output workbook or Show work as appropriate.

## Validation

Test:

- Base case reproduces the deterministic calculation.
- Bounds and units are valid.
- Higher or lower inputs move outputs in the expected direction when monotonicity is a business rule.
- Scenario labels map to the correct assumptions.
- Random results reproduce with the same seed.
- Output percentiles are ordered.
- The recommendation changes only when its confirmed threshold is crossed.

Return a privacy-safe `analysis_summary` with suitability, sensitivity, method family, and fallback reason bands. Do not expose protected scenario values to the connected AI tool.
