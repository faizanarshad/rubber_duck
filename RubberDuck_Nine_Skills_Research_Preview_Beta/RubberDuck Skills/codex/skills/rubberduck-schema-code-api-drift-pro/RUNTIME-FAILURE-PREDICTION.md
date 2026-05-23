# Runtime Failure Prediction

Predict runtime failures only from specific drift cells.

## Prediction table

```markdown
| Prediction ID | Concept | Drift cell | Failure mode | Path | Evidence | Confidence | Test to expose |
|---|---|---|---|---|---|---|---|
```

## Failure modes

```text
READ_BREAK
WRITE_BREAK
API_CONTRACT_VIOLATION
CLIENT_TYPE_BREAK
SILENT_DATA_LOSS
UNREACHABLE_STATE
DEFAULT_MISMATCH
VALIDATION_REJECTION
SERIALIZATION_MISMATCH
AUTH_VISIBILITY_LEAK
```

## Rule

No prediction without a drift matrix row. No high-confidence prediction without a path or source evidence.
