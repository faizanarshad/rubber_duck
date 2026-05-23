# Impact Workflow

## Phase 0 — Scope and tool setup

Pin repo, branch, commit, target, desired change, change type, and budget.

## Phase 1 — Target resolution

Use `TARGET-RESOLUTION.md`.

## Phase 2 — Shadow / doppelganger preflight

Use `SHADOW-PREFLIGHT.md`.

Search for semantically similar functions, duplicated implementations, and same-concept helpers.

Do not stop if shadows are found. Emit alert and continue in single-target mode unless:
- shadow is public/production and clearly higher-priority than target,
- or user asked to unify the concept.

## Phase 3 — Dual-source caller/callee discovery

Use `DUAL-SOURCE-ADJUDICATION.md`.

Required:
- call_chain callers,
- call_chain callees,
- search_code usage scan,
- source reads of top callers,
- symbol/export checks.

## Phase 4 — Shared state and variable flow

Use:

```python
query_action(action="shared_variables", function="<target>")
query_action(action="trace_variable", var="<key_var>")
```

If `shared_variables` is unavailable, approximate from source reads, module-level variables, class fields, and trace_variable.

## Phase 5 — Public API / export / config / deploy impact

Check:

```text
package exports
barrel exports
CLI registration
public directory / API package
config names
docs/comments
runtime/deploy usage
```

## Phase 6 — Tests and mocks

Search for:
- direct target usage in tests,
- module mocks,
- factory mocks,
- vi/jest mocks,
- post-import symbol mocks,
- snapshots,
- integration tests.

Use `MOCK-BREAKAGE.md`.

## Phase 7 — Comment contracts

Use `COMMENT-CONTRACTS.md`.

## Phase 8 — Quality, rare signals, runtime optimization

Use:
- `QUALITY-RUNTIME-SWEEP.md`
- `RUNTIME-OPTIMIZATION.md`

## Phase 9 — Risk, order, tests, rollback

Use `IMPACT-RISK-SCORING.md`.

## Phase 10 — Evidence pack + final report

Use:
- `EVIDENCE-PACK.md`
- `REPORT-TEMPLATE.md`
- consistency checkers.
