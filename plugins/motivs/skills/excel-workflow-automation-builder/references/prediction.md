# Privacy-First Prediction

Use this reference only when the requested output requires estimating an unknown future quantity from historical evidence. If known inputs or explicit assumptions are sufficient, use deterministic calculation instead.

## Prediction Contract

Confirm or safely derive:

- Target measure and business definition.
- Time field, frequency, aggregation grain, and forecast horizon.
- Entity or segment grain.
- Whether partial current periods should be excluded.
- Known future commitments, promotions, closures, stockouts, or structural changes.
- Non-negative, integer, capacity, or other output constraints.
- Error cost: whether over-prediction or under-prediction is more harmful.

Do not use an identifier, cumulative total, already-forward-looking plan, or target value as the historical outcome. Block ambiguous target definitions.

## Data-Fitness Gate

Run the gate inside Motivs against protected values. Check:

- Parseable and ordered time values.
- Duplicate observations at the intended grain.
- History length relative to the horizon and possible seasonal cycle.
- Missing periods and irregular cadence.
- Partial latest period.
- Missing, negative, sparse, or zero-heavy target values.
- Outliers, discontinuities, and structural breaks.
- Leakage from future-derived fields.

Classify suitability as `suitable`, `limited`, or `insufficient`. If insufficient, return a validated report or assumption-based projection instead of a historical forecast. Do not impute material gaps, remove outliers, or complete partial periods without a confirmed rule.

## Vetted Method Set

Use only methods needed by the evidence:

- Last-value baseline.
- Seasonal-naive at the week (7 days) for daily data.
- Seasonal-naive at the year for daily data — as 364 days, not 365, so weekday alignment survives. **Mandatory whenever the history covers at least a year**: annual weather and calendar cycles routinely beat week-scale methods on months unlike the recent past, and a candidate set that only looks weeks back cannot see that. Skipping it is not a defensible judgment call; if it loses the backtest, say so in the diagnostics rather than leaving it untried.
- Simple moving average.
- Weighted moving average with weights fixed before evaluation.
- Simple exponential smoothing.
- Simple linear trend projection when trend continuation is plausible.
- Explicit assumption-based projection when history is not predictive.

Use `scripts/intelligence_kernels.py` as the vetted build-time reference. Copy only selected functions into the self-contained notebook; never import the helper at runtime. Do not add neural networks, automated ML, or large modeling libraries.

## Temporal Evaluation

Never use random train/test splitting. Preserve time order and use an expanding-window or rolling-origin evaluation. Evaluate the horizon required by the business outcome when the history is long enough.

Always compare candidates with last-value and, when applicable, seasonal-naive baselines. When the history covers a year or more of daily data, the 364-day seasonal-naive method enters this comparison as a candidate in its own right, not only as a baseline: backtest it alongside every other candidate and name it in the report among the methods compared. A target month unlike the recent past is decided by year-scale seasonality; every week-scale method under-predicts or over-predicts it together, so their mutual agreement proves nothing. Prefer the simpler baseline unless another method improves the primary error by a material predeclared margin and does not introduce unacceptable bias.

Report at least:

- MAE for scale-readable error.
- WAPE when the total absolute actual value is non-zero.
- Signed bias in the target's natural units or as a safe band.

Do not use MAPE when actual values may be zero or close to zero. Do not select a method using the same final holdout used to make the readiness claim when enough data exists for nested evaluation; otherwise label the evidence limited.

## Uncertainty And Fallback

Produce a range as well as a point estimate. For the initial method set, use empirical backtest residual quantiles or explicit scenario assumptions. Label the range as an empirical planning range, not a guaranteed confidence interval.

Fall back to the simplest valid method when:

- No candidate materially beats the baseline.
- Backtest evidence is too short or unstable.
- Bias is material for the business cost.
- Cadence or target quality cannot be repaired safely.
- A structural change makes historical extrapolation misleading.

Do not hide fallback. Return a plain-language reason and a privacy-safe `analysis_summary` following `references/privacy-safe-diagnostics.md`.

## Output Rules

- Preserve actual versus forecast distinction.
- Include period, grain, point estimate, lower planning range, and upper planning range.
- Keep confirmed future commitments separate from statistically estimated values.
- Avoid false precision; round according to business units.
- Reconcile totals across entity and aggregate outputs when both are present.
- Clearly mark partial or unsupported segments.

## Self-Checks

Include synthetic checks for:

- Constant series.
- Linear trend.
- Seasonal pattern.
- Zeros and sparse demand.
- Missing values and missing periods.
- Insufficient history.
- Partial latest period.
- Candidate worse than baseline, which must trigger baseline fallback.
- Deterministic reproducibility of ranges when a random seed is used.
