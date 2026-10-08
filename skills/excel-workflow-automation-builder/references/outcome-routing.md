# Minimum-Outcome Routing

Use this reference for every new automation or material redesign. Keep the routing internal; employees describe the outcome and never choose an analytical mode.

## Define The Two Contracts

Write a concise outcome contract containing:

- Requested artifact and delivery format.
- Audience and recurring operating process.
- Action the artifact enables, if any.
- Required period, grain, and grouping only when material.
- Conditions that would make the result unusable or unsafe.

Write a concise evidence contract containing:

- Relevant protected source contracts and likely field roles.
- Confirmed business definitions and constraints.
- What the available evidence can support.
- Reversible assumptions the automation may infer and validate.
- Material ambiguities that require confirmation.

Do not ask for a detail merely because it is unknown. Ask only when plausible answers would change the output, business meaning, feasibility, recommendation, or risk. Ask no more than one logical group at a time.

## Select The Minimum Capabilities

Classify the workflow with the smallest sufficient subset:

- `clean`: parse, normalize, map aliases, handle confirmed missing-value rules, and expose exceptions.
- `reconcile`: join, aggregate, compare, validate, and create a report or template output.
- `calculate`: apply deterministic formulas or explicit assumptions.
- `allocate`: assign limited capacity, budget, stock, people, or time under confirmed constraints.
- `predict`: estimate an unknown future quantity from historical evidence.
- `simulate`: explore material uncertainty or interacting assumptions that may change the action.
- `compare`: evaluate alternatives, thresholds, or recommendations using confirmed criteria.

Always preserve `clean + reconcile` as the default for reporting. A capability may be selected without capabilities that appear earlier in this list. A plan may be deterministic. A decision may be threshold-based. A scenario may use explicit assumptions without a forecast.

Record the selected capabilities and one plain-language reason for each in maintainer diagnostics. Do not expose them as user choices.

## Escalation Gates

Select `predict` only when all are true:

1. The requested output requires an unknown future value.
2. Historical evidence is relevant to that value.
3. A time field, target measure, horizon, and grain can be established.
4. The protected runtime can test a candidate against a simple temporal baseline.

Otherwise use a known-input calculation, assumption-based projection, or report and explain the limitation.

Select `simulate` only when uncertainty or interactions between assumptions could materially change the action. Prefer explicit base/upside/downside cases or sensitivity tables before Monte Carlo.

Select `allocate` only when there is a target or demand, limited resources, and at least one confirmed constraint. Do not invent objectives such as minimizing cost or maximizing service.

Select `compare` only when alternatives or decision thresholds are explicit. Do not create a weighted score without confirmed criteria, direction, weights, missing-value behavior, and tie handling.

## Rollout Modes

Read `implementation_contract.minimum_intelligence.mode`; treat a missing mode as `shadow`:

- `off`: do not classify or add advanced behavior; use the existing reporting and reconciliation path.
- `shadow`: record the classification in maintainer evidence but do not add advanced behavior.
- `beta`: add advanced behavior only for an explicitly requested advanced outcome after every gate passes.
- `enabled`: add the minimum advanced capabilities required by the confirmed outcome after every gate passes.

In `shadow`, treat the classification as a hypothesis for regression evidence. Never reinterpret the employee's requested report merely to exercise an advanced capability.

Examples:

- `Monthly report for my manager` -> `clean`, `reconcile`.
- `Next month's schedule from these availability rules` -> `clean`, `calculate`, `allocate`.
- `Recommend reorder quantities` -> `clean`, `calculate`; add `predict` only when demand is not already supplied.
- `Compare these suppliers using price, quality, and lead time` -> `clean`, `compare`.
- `Show the effect of a 10% cost increase` -> `calculate`, not `simulate`, unless uncertainty around several assumptions affects the choice.

## Safe Fallbacks

Use the least ambitious valid fallback:

1. Validated report or reconciliation.
2. Deterministic calculation from known inputs.
3. Assumption-based projection with visible assumptions.
4. Simple baseline forecast with an uncertainty range.
5. More advanced candidate only when it passes its method-specific gate.

Never hide a fallback. State it in plain language in the result and record its reason in `analysis_summary` when that optional result is used.

## Employee Output

Return only what helps the employee act:

- The exact requested artifact.
- One concise outcome statement.
- The next action when applicable.
- Material warnings, infeasibility, or unresolved assumptions.

Place capability selection, method names, test scores, diagnostics, and code details in Show work. Do not add an intelligence-mode selector or analytical jargon to the primary path.
