# Evidence Governance

## Evidence pack

DEEP reports must produce:

```text
evidence/candidate-generators.md
evidence/function-inventory.md
evidence/cluster-summary.json
evidence/cluster-members.md
evidence/fingerprint-matrix.csv
evidence/graph-dimension-coverage.md
evidence/divergence-matrix.md
evidence/source-snippets.md
evidence/inline-implementations.md
evidence/comment-contracts.md
evidence/call-path-map.md
evidence/negative-results.md
evidence/mergeability.md
evidence/change-impact-preflight.md
evidence/unification-plan.md
evidence/tool-health.md
evidence/falsification-recipes.md
evidence/protocol-completion.md
```

## Claim ledger

Every major claim must state:

```text
claim
evidence file
tool/source
confidence
caveat
```

## Cluster summary JSON

Required fields:

```json
{
  "mode": "SEEDED|CONCEPT|UNCONSTRAINED",
  "repo": "",
  "commit": "",
  "seed_or_concept": "",
  "candidate_generators": [],
  "clusters": [
    {
      "id": "",
      "concept": "",
      "named_members": [],
      "inline_members": [],
      "roles": {},
      "dimension_coverage": {},
      "composite_score": null,
      "mergeability": "",
      "unification_recommended": true
    }
  ],
  "limitations": []
}
```
