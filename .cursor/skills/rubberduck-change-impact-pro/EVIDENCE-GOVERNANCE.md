# Evidence Governance

Every major claim must be labeled:

```text
source-confirmed
graph-confirmed
search-confirmed
runtime-confirmed
manual inference
unsupported
out of scope
```

## Claim ledger

Write `evidence/claim-ledger.md`:

| Claim | Evidence | Evidence type | Confidence | Caveat |
|---|---|---|---|---|

## Negative claim ledger

Write `evidence/negative-claims.md`:

| Negative claim | Search pattern | Scope | Matches | Unsupported caveat |
|---|---|---|---|---|

## Anti-overclaim rules

Do not say:
- "no callers" unless call_chain and search_code agree or disagreement is explained,
- "safe" without guard/test/source evidence,
- "complete coverage" without unsupported-surface handling,
- "optimized" without same-result proof/test plan.
