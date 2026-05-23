# Change-Impact Preflight

Before proposing unification, run a lightweight impact analysis.

## Required checks

```text
callers of canonical member
callers of duplicate member
public exports
test-only vs production paths
API compatibility
type compatibility
behavioral differences
state/concurrency differences
error-handling differences
affected tests
migration risk
```

## Required table

```markdown
| Impact area | Evidence | Risk | Required action |
|---|---|---|---|
```

## Risk rules

- If the canonical helper is not exported, unification is API-changing.
- If production and test paths differ, treat as context-sensitive.
- If a comment explains divergence, preserve it unless a fix addresses the reason.
