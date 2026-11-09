# Verification Catalogue

Recognisable report shapes and the arithmetic each one owes. Read this when
declaring `verification` in the manifest, after picking the grain and before
writing any code. The syntax lives in `references/platform-ui-contract.md`;
this file is about which check a given task actually calls for.

Pick a form by what the task describes, the way you pick a grain. If the task
matches none of these, declare no reconciliation and say why in your report. An
invented check is worse than an absent one: it buys a green verdict without
earning it.

Every entry names what the form **cannot** prove. Write those lines into the
report you hand back, so the reader knows where the certificate goes quiet.

---

## 1. Summary of a measure by category

A total per group: sales by product, hours by project, spend by department.
The most common shape by far.

**Recognise it by** an input of line entries and a result of one row per group,
where the result column and the input column mean the same thing.

**Grain** the grouping columns.

**Check** an identity — the total did not change, only its arrangement.

```json
{ "measure": "Net Sales", "equals": "net_sales",
  "columns": { "net_sales": "Net Sales" },
  "phrase": "net sales recomputed from the line entries",
  "tolerance": 0.05 }
```

**Tolerance** 0.05 for money, 0 for counts.

**Cannot prove** that rows landed in the right group. The total is right even
if every row went to the wrong category. Grain and identifier tracing cover
that from the other side, which is why all three run together.

**If the report separates refunds, returns or exclusions into their own
column, name the parts.** A summary of sales that keeps refunds apart is short
by exactly the refunds, and an identity on the sales column alone will fail
every time:

```json
{ "measure": "Net Sales",
  "measure_parts": ["Net Sales", "Refund Amount"],
  "equals": "net_sales",
  "columns": { "net_sales": "Net Sales" },
  "phrase": "sales and refunds together check out against the line entries",
  "tolerance": 0.05 }
```

If the report drops the excluded rows entirely rather than reporting them in a
column, there is nothing to add back: declare no check here and say in your
report which rows were excluded and why.

---

## 2. Revenue from quantity and price

A line total computed rather than copied.

**Recognise it by** an input carrying both a quantity and a unit price, and a
result carrying their product.

**Grain** whatever identifies a line or a group of lines.

**Check** the product, recomputed by the platform.

```json
{ "measure": "Revenue", "equals": "qty * unit_price",
  "columns": { "qty": "Quantity", "unit_price": "Unit Price" },
  "phrase": "revenue recomputed from quantity and unit price",
  "tolerance": 0.05 }
```

**Tolerance** 0.05, or 1.00 over tens of thousands of lines where per-line
rounding accumulates.

**Cannot prove** anything about discounts, taxes or rounding rules applied
between the two columns. If the task applies a discount, this check will fail
honestly — declare the identity from form 1 instead, or name the discount
column in the expression if the input carries it.

**Only declare it when the input carries both columns.** If price lives in a
lookup table the automation joins in, the platform cannot see it and the check
is reported as a blind spot.

---

## 3. Payroll

**Recognise it by** gross pay, deductions and a net figure per person.

**Grain** the employee identifier, plus the period when one file covers several.

**Check** net equals gross minus deductions.

```json
{ "measure": "Net Pay", "equals": "gross - deductions",
  "columns": { "gross": "Gross Pay", "deductions": "Total Deductions" },
  "phrase": "net pay recomputed from gross and deductions",
  "tolerance": 0.01 }
```

**Tolerance** 0.01. Payroll is expected to be exact to the cent; a wider
tolerance here hides the errors this check exists to find.

**Cannot prove** that the deductions themselves are right — tax bands, benefit
rates and thresholds are the automation's own logic. This check proves only
that the subtraction is consistent with the numbers given.

---

## 4. Stock movement and closing balance

**Recognise it by** an opening figure, movements in and out, and a closing
figure.

**Grain** item, or item and location, plus the period.

**Check** the balance equation.

```json
{ "measure": "Closing", "equals": "opening + received - issued",
  "columns": { "opening": "Opening Balance", "received": "Received",
               "issued": "Issued" },
  "phrase": "closing balance recomputed from opening, receipts and issues",
  "tolerance": 0 }
```

**Tolerance** 0 for whole units, 0.001 for weights and volumes.

**Cannot prove** that the opening balance was right to begin with. The check
carries the period forward from whatever it was handed; an error inherited from
last month passes cleanly.

---

## 5. Ledger and cash book

**Recognise it by** debit and credit columns, or a running balance.

**Grain** the entry identifier, or the account plus the period for a summary.

**Check** the balance is what the two sides make it.

```json
{ "measure": "Balance", "equals": "debits - credits",
  "columns": { "debits": "Debe", "credits": "Haber" },
  "phrase": "balance recomputed from debits and credits",
  "tolerance": 0.01 }
```

**Tolerance** 0.01.

**Cannot prove** that entries are posted to the right accounts, or that the
book is complete. A ledger missing a whole day still balances.

**Watch the separators.** Accounting exports write `-74,510.58` and `-3,50` for
the same kind of number. The platform reads either, but your own parsing has to
as well — a column read with the wrong locale produces a difference the
certificate will report against you.

---

## 6. Pass-through export

A file reshaped, renamed or filtered, with no aggregation.

**Recognise it by** a result with the same row count as the input, or the input
minus a stated exclusion.

**Grain** whatever identifies a row, usually a document or transaction id.

**Check** an identity on the amount carried through.

```json
{ "measure": "Amount", "equals": "amount",
  "columns": { "amount": "Importe" },
  "phrase": "amounts carried through unchanged",
  "tolerance": 0 }
```

**Tolerance** 0. Nothing is being recomputed, so any difference is a loss.

**Cannot prove** that the right rows were excluded. If the task filters, the
totals will differ by design and this check is wrong for it — use form 1 on the
subset instead, and say in your report what was excluded and why.

---

## 7. Commission

**Recognise it by** a rate applied to a base amount.

**Grain** the agent, or the agent and the period.

**Check** the product of base and rate.

```json
{ "measure": "Commission", "equals": "base * rate",
  "columns": { "base": "Sale Amount", "rate": "Commission Rate" },
  "phrase": "commission recomputed from the sale amount and the rate",
  "tolerance": 0.05 }
```

**Tolerance** 0.05.

**The rate has to be a column, not a number you type into the expression.** A
constant in the check is a constant you chose, and the check would then agree
with itself whatever the automation did. If the rate lives in a tier table
rather than the file, declare no check and name the tiers as a blind spot.

**Cannot prove** that the right tier or rate was selected, only that the
multiplication is consistent with the rate recorded next to it.

---

## 8. Inventory count

**Recognise it by** a counted quantity against a system quantity, and a
valuation of the difference.

**Grain** item, or item and location.

**Check** the variance, valued.

```json
{ "measure": "Total Cost", "equals": "adjustment_quantity * unit_cost",
  "columns": { "adjustment_quantity": "Adjustment Quantity",
               "unit_cost": "Unit Cost" },
  "phrase": "adjustment value recomputed from the counted difference and unit cost",
  "tolerance": 0.05 }
```

**Tolerance** 0.05.

**Cannot prove the value of stock on hand.** Unit costs usually live in the
automation's own snapshot rather than in the file it was given, and a number
the platform cannot see is a number it cannot recompute. Say so plainly:
"The value of remaining stock is not checked, the unit costs used are not
present in the input." That sentence belongs in your report whether or not you
declare the check above.

---

## 9. Summary card

Almost every report carries one: a sheet of period totals, one metric per line,
the name on the left and the number on the right.

**Recognise it by** the absence of a header row. It is not a table and has no
grain, and read as one it yields a header made of the first metric and its
value.

**Shape** `"card"`, declared explicitly. No grain.

**Check** the totals against the same input the tables were built from, naming
the parts when the card reports them separately.

```json
{ "name": "Summary", "shape": "card",
  "reconciliations": [
    { "measure": "Net Sales",
      "measure_parts": ["Net Sales", "Refund amount"],
      "equals": "net_sales",
      "columns": { "net_sales": "Net Sales" },
      "phrase": "the reported totals together match every line entry",
      "tolerance": 0.05 } ] }
```

**Cannot prove** anything about rows sitting below the card. A ranking table
under the metrics is a different thing entirely and is reported as unchecked.

**Worth doing.** The card is the part of the report a reader actually looks at.
A total nobody checked, printed in bold at the top of the page, is the single
most expensive number in the file.

## When no form fits

Declare the grain, declare no reconciliation, and write one line in your report
saying which arithmetic went unchecked and why. The result is reported as
`Shape only`, which is the honest answer.

These do not fit and are not worth forcing:

- a forecast or any figure derived from assumptions rather than from the input
- a currency conversion whose rate is not in the file
- a result whose measure is an average, a percentage or a ratio; these do not
  add up across rows, so a sum of them means nothing
- anything the automation looks up externally

## Before you declare

- The measure is a **result** column, the expression reads **input** columns.
- Every name in the expression is either an input column or an alias mapped to
  one, and no alias is left unused.
- Values, not formulas, in any column a check measures.
- The tolerance is the narrowest one that survives honest rounding. Never widen
  it to make a failing result pass; a red verdict that is true is the point of
  the whole exercise.
