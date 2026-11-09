# Privacy-Safe Analysis Diagnostics

Use this reference when protected validation needs to tell the connected AI tool whether an advanced method was suitable, tested, or safely downgraded. Employee-authenticated outputs may contain their own business values; the connected tool channel must not.

## Optional Result Contract

An advanced automation may return an `analysis_summary` object beside its normal employee result. The platform treats this object as untrusted and forwards only allowlisted categorical fields.

Use schema version `minimum-intelligence-v1` and only these fields:

- `capabilities`: subset of `clean`, `reconcile`, `calculate`, `allocate`, `predict`, `simulate`, `compare`.
- `suitability`: `suitable`, `limited`, `insufficient`, `not_applicable`.
- `time_field`: `detected`, `not_detected`, `not_applicable`.
- `history_length`: `very_short`, `short`, `moderate`, `long`, `not_applicable`.
- `cadence`: `daily`, `weekly`, `monthly`, `quarterly`, `yearly`, `irregular`, `unknown`, `not_applicable`.
- `missing_periods`: `none_detected`, `low`, `material`, `unknown`, `not_applicable`.
- `partial_period`: `detected`, `not_detected`, `unknown`, `not_applicable`.
- `sparsity`: `dense`, `some_zeros`, `zero_heavy`, `unknown`, `not_applicable`.
- `outlier_signal`, `trend_signal`, `seasonality_signal`: `none_detected`, `weak`, `present`, `unknown`, `not_applicable`.
- `method_family`: `reporting`, `deterministic`, `allocation`, `last_value`, `seasonal_naive`, `moving_average`, `weighted_moving_average`, `exponential_smoothing`, `linear_trend`, `assumption_projection`, `sensitivity`, `bootstrap`, `monte_carlo`, `threshold`, `weighted_comparison`, `other`, `not_applicable`.
- `baseline_result`: `improved`, `matched_or_fallback`, `worse`, `not_testable`, `not_applicable`.
- `bias_band`: `low`, `moderate`, `high`, `unknown`, `not_applicable`.
- `uncertainty_band`: `narrow`, `moderate`, `wide`, `unknown`, `not_applicable`.
- `sensitivity`: `stable`, `sensitive`, `unknown`, `not_applicable`.
- `fallback_reason`: `none`, `insufficient_history`, `data_quality`, `baseline_not_beaten`, `unstable_backtest`, `material_bias`, `structural_change`, `missing_business_rule`, `infeasible`, `unsupported`, `other`.
- `warning_codes`: subset of the stable codes implemented by the platform sanitizer.

Omit fields that do not apply. Never add free-form text, field names, entity names, source values, exact counts, exact dates, exact errors, predictions, totals, scores, residuals, thresholds, file paths, hashes, or snippets to `analysis_summary`.

## Separate The Three Channels

- **Employee result**: may show the authenticated employee their report, forecast, plan, ranges, and business-specific explanations.
- **Platform Show work**: may show authorized maintainers detailed diagnostics and protected execution logs according to platform permissions.
- **Connected AI tool**: receives only the sanitized categorical `analysis_summary`, structured validation stages, and existing metadata-safe issue codes.

Do not reuse employee-facing messages as connected-tool diagnostics.

## Suitability And Bands

Define band thresholds inside the notebook before protected execution and test their boundaries with synthetic fixtures. Choose thresholds appropriate to the confirmed frequency, horizon, business cost, and method; do not claim that one universal observation count makes every series suitable.

Use `unknown` or `not_applicable` rather than inventing a classification. Use `insufficient` when a missing target definition, time field, history, or data-quality rule blocks responsible use.

## Privacy Tests

Before release, attempt to place protected-looking text, field names, numbers, nested objects, unknown enum values, long arrays, and path-like strings in `analysis_summary`. Confirm the platform drops them and returns only allowlisted enum values. Confirm ordinary reporting automations that omit `analysis_summary` retain the exact existing validation response shape.
