# Dual-Source Adjudication

This is load-bearing.

## Rule

Do not trust `assess(mode="impact")`, `plan_change`, or `call_chain` alone.

Always reconcile at least two channels:

```text
call_chain callers/callees
search_code usage scan
source reads
symbols_overview
trace_variable/shared_variables
tests/mocks search
```

## Required table

Write `evidence/dual-source-adjudication.md`:

| Claim | Tool A result | Tool B result | Adopted truth | Reason | Confidence |
|---|---|---|---|---|---|

## Override rule

If RubberDuck impact mode says LOW/no cross-file refs but `search_code` finds production usages:

```text
Do not report LOW.
Upgrade risk according to discovered usages.
Explain the disagreement.
```

If search_code finds text hits but call_chain/source proves they are unrelated:

```text
Demote the text hits.
Explain why.
```

## Falsification

For each adopted truth, include how to refute it:

```text
Rerun query:
Expected contradiction:
```
