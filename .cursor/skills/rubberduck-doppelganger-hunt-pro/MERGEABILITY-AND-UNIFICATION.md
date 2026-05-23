# Mergeability and Unification

## Mergeability classes

```text
SAFE_TO_MERGE
API_CHANGING
TEST_ONLY_CLEANUP
KEEP_SEPARATE
DELIBERATE_DIVERGENCE
NEEDS_INVESTIGATION
```

## Required unification plan

```markdown
| PR | Change | Risk | Tests | Rollback | Why this order |
|---|---|---|---|---|---|
```

## What not to merge

Every report must include:

```text
members that should not be unified
lookalikes excluded
deliberate divergences to preserve
API compatibility warnings
```

## Plan rule

A unification plan is invalid without change-impact preflight.
