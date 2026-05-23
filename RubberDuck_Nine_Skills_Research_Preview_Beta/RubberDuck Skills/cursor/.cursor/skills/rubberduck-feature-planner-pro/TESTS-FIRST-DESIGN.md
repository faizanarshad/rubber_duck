# Tests-First Design

Design tests before implementation.

Tests must map to acceptance criteria:

```text
AC id
criterion
test name
test file
expected assertion
implementation status
```

The plan should produce `test_diff.patch`.

`validate_generated_diff` must be run against the test diff if the tool is available. A WARN may pass only if all blocking checks pass and warnings are adjudicated in `PLAN.md`.
