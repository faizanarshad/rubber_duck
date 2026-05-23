# Path Enumeration

For each implementation, enumerate observable paths.

## Path table

```text
Path ID
Guard / condition
Inputs triggering path
Calls / side effects
Return / throw
Resource lifecycle
Evidence
```

## Matching table

```text
Before path | After path | Status | Divergence | Evidence
```

Statuses:

```text
MATCHED
DIVERGENT
MISSING_IN_BEFORE
MISSING_IN_AFTER
UNDECIDABLE
```

Do not claim equivalence if unmatched paths remain unless the preserved contract explicitly excludes them.
