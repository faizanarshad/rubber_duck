# Evidence Pack Requirements

DEEP mode must produce `impact-summary.json` and evidence files.

## Required files

```text
evidence/tool-health.md
evidence/tool-calls.md
evidence/target-resolution.md
evidence/dual-source-adjudication.md
evidence/search-results.md
evidence/source-snippets.md
evidence/callers.md
evidence/callees.md
evidence/shared-variables.md
evidence/data-flows.md
evidence/module-state.md
evidence/comment-contracts.md
evidence/mock-breakage.md
evidence/public-api-proof.md
evidence/test-coverage-matrix.md
evidence/rare-signals.md
evidence/runtime-optimization.md
evidence/quality-scorecard.md
evidence/evidence-reuse-ledger.md
evidence/unsupported-surfaces.md
evidence/claim-ledger.md
evidence/negative-claims.md
evidence/falsification-recipes.md
```

If a section is not applicable, create it with a reason.

## impact-summary.json schema

Required keys:

```json
{
  "target": {},
  "change": {},
  "risk": {},
  "callers": [],
  "callees": [],
  "shared_state": [],
  "data_flows": [],
  "public_api": {},
  "mock_sites": [],
  "comment_contracts": [],
  "tests_to_run": [],
  "runtime_optimization": [],
  "change_order": [],
  "rollback": [],
  "tool_health": {},
  "unsupported_surfaces": [],
  "claims": []
}
```

## Hygiene

No local machine paths or uploaded-file markers in shareable output.
Use repo-relative paths.
