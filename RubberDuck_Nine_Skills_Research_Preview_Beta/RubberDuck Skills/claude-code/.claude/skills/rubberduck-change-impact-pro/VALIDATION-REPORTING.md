# Validation and Reporting

## Falsification recipes

For each major claim, provide:

```text
To refute:
Tool/query:
Expected contradiction:
```

Write `evidence/falsification-recipes.md`.

## Tests to run

Classify tests:

```text
must run
should run
nice to run
not relevant
```

For each test:

```text
why
expected breakage
what it covers
```

## Report status

Possible statuses:

```text
complete
source-confirmed but runtime/tests not executed
degraded due tooling
draft / incomplete
```

## Paste-ready PR description

Always include:

```text
risk badge
files changed
tests to run
migration notes
rollback
reviewer callouts
shadow/doppelganger note if any
comment-contract note if any
```
