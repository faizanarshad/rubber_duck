# Evidence Governance

## Evidence pack

Every DEEP report must produce:

```text
REPORT.md
evidence/layer-inventory.md
evidence/concept-map.md
evidence/concept-fusion-ledger.md
evidence/drift-matrix.csv
evidence/runtime-failure-predictions.md
evidence/round-trip-proof.md
evidence/remediation-diffs.md
evidence/coverage-gaps.md
evidence/negative-claims.md
evidence/falsification-recipes.md
evidence/tool-health.md
evidence/schema-drift-summary.json
evidence/protocol-completion.md
```

If a file cannot be populated, create it with `Status: unavailable` and explain why.

## Claim labels

```text
codebase-intelligence
symbols_overview
call_chain
trace_variable
search_code
read_source
schema-file
api-contract
validator-source
manual inference
unsupported
out of scope
```

## Negative claims

"No drift" claims require:

```text
layer inventory
dimension coverage
unsupported surface caveats
search patterns
scope
```
