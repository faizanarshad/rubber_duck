# Impact Risk Scoring

Use max-risk aggregation. One high dimension can make the overall risk high.

## Dimensions

```text
caller_count
production_callers
public_api
shared_state
mock_breakage
comment_contracts
test_coverage_gap
runtime_behavior_change
cross_package_impact
unsupported_surface_gap
```

## Suggested levels

```text
LOW: isolated, internal, tests obvious, no shared state, no public export.
MEDIUM: multiple internal call sites, mocks/tests affected, comments/docs change.
HIGH: production call sites, public API, shared state, cross-package, external users, or unclear callers.
CRITICAL: not usually used for change impact unless availability/security/customer-impact is direct and likely.
```

## Required report fields

```text
risk level
risk reasoning
highest-risk dimension
confidence
what would lower risk
what would raise risk
```

## Recommended change order

1. Add/adjust tests.
2. Add compatibility shim if public.
3. Update implementation.
4. Update callers/imports/mocks.
5. Update comments/docs.
6. Run targeted tests.
7. Run broader tests if public/cross-package.
