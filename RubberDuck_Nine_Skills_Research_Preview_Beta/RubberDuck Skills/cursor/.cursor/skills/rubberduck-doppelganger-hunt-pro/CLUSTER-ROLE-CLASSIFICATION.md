# Cluster Role Classification

Each cluster member must have one role.

## Roles

```text
CANONICAL
HIDDEN_CANONICAL
WRAPPER_OR_ORCHESTRATOR
ACCIDENTAL_REIMPLEMENTATION
INLINE_COPY
TEST_FIXTURE_COPY
DELIBERATE_DIVERGENCE
SELECTOR_OR_ADAPTER
LOOKALIKE_NOT_DUPLICATE
```

## Required table

```markdown
| Member | Role | Why | Evidence | Mergeability implication |
|---|---|---|---|---|
```

## Role rules

- `CANONICAL`: exported/public or clearly intended reusable implementation.
- `HIDDEN_CANONICAL`: best implementation exists but is internal/not exported.
- `WRAPPER_OR_ORCHESTRATOR`: calls or selects canonical behavior; not duplicate implementation.
- `DELIBERATE_DIVERGENCE`: evidence shows copy exists for a reason; do not auto-merge.
- `LOOKALIKE_NOT_DUPLICATE`: similar name/shape but different behavior.
