# Decision Support

Use this reference only when the requested output must compare alternatives, apply a threshold, or recommend an action. A decision may use current facts and rules without prediction or simulation.

## Decision Contract

Confirm:

- Alternatives or eligible actions.
- Decision owner and required output.
- Criteria and their business definitions.
- Whether higher or lower is better for each criterion.
- Hard disqualifiers and approval rules.
- Weights or priority order when trade-offs exist.
- Missing-value behavior.
- Tie-breaking and override policy.
- Evidence that would invalidate the recommendation.

Do not invent weights, convert a hard constraint into a soft score, or silently normalize incomparable units.

## Choose The Simplest Decision Method

Prefer methods in this order:

1. Direct rule or approval threshold.
2. Eliminate alternatives that violate hard constraints.
3. Lexicographic priority order.
4. Weighted comparison with confirmed directions and weights.
5. Dominance or Pareto comparison when no single weighting is approved.
6. Scenario-sensitive comparison only when uncertainty can change the ranking.

Use `scripts/intelligence_kernels.py` as vetted build-time reference for transparent weighted comparison. Copy only required functions into the self-contained notebook.

## Dirty-Data And Fairness Controls

- Validate units and periods before comparison.
- Keep `missing`, `not applicable`, and zero distinct.
- Do not reward missing evidence through normalization.
- Detect criteria that duplicate the same underlying factor.
- Flag a recommendation driven by one low-confidence field.
- Treat protected or sensitive attributes according to organizational policy; do not introduce them as decision criteria without explicit authorization.
- Preserve the source and transformation lineage of every criterion.

## Robustness Checks

Recompute the decision after:

- Removing each non-hard criterion once.
- Applying approved plausible weight changes.
- Resolving ties through the confirmed rule.
- Moving values within known data-quality or scenario bands.

Classify the result as:

- `stable`: the action is unchanged across approved checks.
- `sensitive`: a plausible change reverses the action.
- `insufficient`: missing definitions or evidence prevent a responsible recommendation.

If sensitive, identify the material boundary or criterion without exposing protected values to the connected AI tool. If insufficient, provide the comparison evidence and ask for the smallest missing decision instead of inventing a recommendation.

## Validation

Test hard disqualifiers, directionality, normalization, missing values, equal scores, deterministic ties, sensitivity, and reproducibility. Recalculate the selected alternative from the final output and confirmed rules.

## Employee Result

Lead with the recommendation only when evidence is sufficient. Include the main business reason, material caveat, and next action. Keep scores, weights, method details, and robustness evidence in the output workbook or Show work unless the user explicitly needs them.
