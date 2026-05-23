# Witness Generation

A witness is an input/state that distinguishes BEFORE from AFTER.

Witness sources:

```text
graph-derived
guard-expression-derived
manual from source
runtime-test-confirmed
unavailable
```

Required for:

```text
NOT_EQUIVALENT
CONDITIONALLY_EQUIVALENT
EQUIVALENT_WITH_STRUCTURAL_DRIFT when risk remains
```

Output:

```text
Witness ID
Input/state
Before behavior
After behavior
Why this distinguishes
Test expression
Evidence
```

If unavailable, explain blocker.
