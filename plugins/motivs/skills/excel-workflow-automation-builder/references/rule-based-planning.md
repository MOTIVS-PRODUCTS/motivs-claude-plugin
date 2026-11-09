# Rule-Based Planning And Allocation

Use this reference only when the outcome requires deterministic calculation, allocation, scheduling, or feasibility under confirmed rules. Do not add prediction or simulation unless their separate escalation gates pass.

## Planning Contract

Confirm or mark unresolved:

- Target, demand, or required coverage.
- Available resources and their units.
- Hard constraints that may never be violated.
- Soft preferences and their priority order.
- Objective, such as cover demand, minimize cost, preserve buffer, or allocate fairly.
- Planning horizon and grain.
- Tie-breaking and rounding rules.
- Approval and override policy.

Never infer an objective from generic words such as `best`, `efficient`, or `optimal`. Ask which business outcome matters when different objectives produce materially different plans.

## Prefer Deterministic Methods

Use simple, inspectable methods before optimization:

- Target minus available capacity.
- Required hours divided by productive hours per person.
- Opening cash plus confirmed inflows minus confirmed outflows.
- Reorder point from confirmed lead-time demand and buffer policy.
- Priority-ordered allocation with explicit caps and floors.
- Earliest-due or highest-priority scheduling with availability and coverage constraints.
- Proportional allocation with a documented residual rule.
- Threshold-based approval or exception routing.

Use `scripts/intelligence_kernels.py` as vetted build-time reference for bounded allocation and weighted comparison patterns. Copy only the required functions into the self-contained notebook; never import the helper at platform runtime.

## Feasibility Before Presentation

Check hard constraints before calling a plan ready:

- Total demand versus total capacity.
- Per-period and per-resource caps.
- Required minimums or service levels.
- Availability and eligibility.
- Non-negative or whole-unit requirements.
- Conservation: allocations equal the amount available or the documented usable amount.
- Unallocated demand and unused capacity.

When infeasible, do not silently relax a constraint. Return the closest useful evidence:

- Which constraint fails.
- The shortfall or conflict in the employee's own authenticated output.
- Which decision could restore feasibility.
- A partial plan only when governance allows it and it is labeled partial.

## Dirty-Data Rules

- Reject mixed or unknown units until mapped.
- Preserve identifiers and leading zeros.
- Do not treat a missing capacity, cost, availability, or demand value as zero without a confirmed rule.
- Separate duplicate records from repeated legitimate events.
- Flag negative or impossible values unless the business definition explicitly permits them.
- Detect contradictory constraints before allocation.
- Keep source lineage for every allocation or exception.

## Validation

Add synthetic self-checks for:

- Exact capacity equals demand.
- Capacity shortage.
- Excess capacity.
- Ties and deterministic ordering.
- Zero demand and zero capacity.
- Missing values and invalid units.
- Caps, floors, and rounding residuals.
- Contradictory constraints.

Recalculate every hard constraint from the produced plan rather than trusting intermediate state. A successful plan must be feasible, reproducible, and traceable.

## Employee Result

Lead with the operational result, not the algorithm. Show the plan or workbook, feasibility status, material shortfalls or unused capacity, and the next decision. Put allocation order, formulas, and constraint checks in Show work.
