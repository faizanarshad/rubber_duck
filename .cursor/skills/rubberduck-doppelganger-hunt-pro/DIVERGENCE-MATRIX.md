# Divergence Matrix

The divergence matrix explains why similar code is not identical.

## Required table

```markdown
| Difference | Member A | Member B | Behavioral impact | Merge risk | Evidence |
|---|---|---|---|---|---|
```

Compare:

```text
inputs
outputs
error handling
state mutation
side effects
resource lifecycle
async/sync behavior
logging/telemetry
test/prod context
public API/export behavior
type signature
guards/invariants
```

If differences are behaviorally irrelevant, say why.
If differences are behaviorally material, mergeability cannot be SAFE_TO_MERGE without a plan.
