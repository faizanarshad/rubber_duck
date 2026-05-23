# Evidence Governance

## Required evidence pack

```text
evidence/mirror-summary.json
evidence/before-source.md
evidence/after-source.md
evidence/import-context.md
evidence/path-catalogue-before.md
evidence/path-catalogue-after.md
evidence/path-match-table.md
evidence/side-effect-manifest.md
evidence/exception-envelope.md
evidence/witness-inputs.md
evidence/generated-tests.md
evidence/undecidable-blockers.md
evidence/structural-drift.md
evidence/falsification-recipes.md
evidence/tool-health.md
evidence/protocol-completion.md
```

If unavailable, create placeholder with reason and impact.

## Evidence labels

```text
semantic-tool-confirmed
codebase-intelligence-confirmed
source-confirmed
runtime-test-confirmed
manual-source-inference
heuristic
unsupported
out-of-scope
```

## mirror-summary.json

Minimum:

```json
{
  "mode": "",
  "preserved_contract": "",
  "verdict": "",
  "divergence_count": 0,
  "undecidable_count": 0,
  "generated_tests": 0,
  "confidence": ""
}
```
