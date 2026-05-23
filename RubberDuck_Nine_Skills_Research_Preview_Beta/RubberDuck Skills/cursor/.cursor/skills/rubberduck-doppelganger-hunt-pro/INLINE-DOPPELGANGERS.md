# Inline Doppelgangers

Named functions are not enough. Search for inline behavior.

## What to search

```text
same API calls
same resource lifecycle
same ordering of effects
same variables and transformations
same open/use/close pattern
same parse/validate/dispatch pattern
same retry/error-handling pattern
same test fixture lifecycle
```

## Required output

```markdown
| Inline member | File:line | Effect signature | Named cluster matched | Role | Mergeability | Evidence |
|---|---|---|---|---|---|---|
```

## Inline claim rule

Do not say "functionally identical" unless:

```text
effect signature matches
control/data-flow shape matches or is explicitly approximated
behavioral differences are listed
```
