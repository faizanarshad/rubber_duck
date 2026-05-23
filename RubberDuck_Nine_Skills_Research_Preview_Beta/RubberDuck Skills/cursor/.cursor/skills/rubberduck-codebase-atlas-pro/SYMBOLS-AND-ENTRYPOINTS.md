# Symbols and Entry Points

## Major symbols table

```markdown
| Subsystem | File | Symbol | Kind | Line | Role | Evidence |
|---|---|---|---|---:|---|---|
```

This is a curated table for reviewer orientation. It is not the full symbol inventory.

## Full or near-full Symbol Inventory evidence

For DEEP mode, create either:

```text
evidence/symbols-overview.md with full or near-full symbols_overview output for core loaded files
```

or:

```text
an explicit report caveat that §1 is curated and raw/complete symbol output is unavailable
```

In DEEP mode, prefer full or near-full symbol evidence. The evidence file must preserve `symbols_overview` evidence by file where available and distinguish:

```text
curated major symbols
full/near-full raw symbols_overview inventory
normalized or report-derived symbol evidence
uninspected files
unsupported files
```

Do not claim "all major classes/functions" unless this full symbols evidence exists or the report caveats the exact scope.

## Entry point table

```markdown
| Entry point | Type | File:line | Evidence | Call-chain status | Notes |
|---|---|---|---|---|---|
```

## Entry types

```text
CLI command
HTTP route
background worker
library public API
plugin/hook
build/deploy script
test/dev helper
configuration-driven entry
```

## Rules

Do not choose entry points by name vibes. Confirm with RubberDuck or metadata.

Entry point candidates that cannot be confirmed should be listed separately as "unconfirmed candidates."

For FEATURE_ATLAS mode, entry-point discovery starts at the requested feature, endpoint, class, function, journey, or behavior, then expands outward only as needed to explain confirmed call/data flow.
