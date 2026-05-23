# Runtime Optimization Opportunity Pass

Every Change Impact report must ask:

```text
Can the target function or high-impact affected functions be optimized while producing the same observable result?
```

## Scope

Analyze:
- target function,
- top callers,
- hot callees,
- functions with loops/I/O/allocation/concurrency/cache behavior,
- code affected by proposed change.

## Equivalence rule

```text
Deterministic exact outputs: 0% behavior tolerance.
Approximate/statistical/performance domains: ±5% tolerance only if explicitly appropriate.
No API/side-effect/order/concurrency change unless requested.
```

## What to inspect

```text
algorithmic complexity
loop count / nested loops
repeated I/O
repeated parsing/regex
unnecessary allocations
cache opportunities
batching opportunities
concurrency opportunities
avoidable work in tests/mocks
```

## Output

```text
§12 Runtime Optimization Opportunities
```

Table:

| Function | Opportunity | Same-result proof needed | Risk | Expected impact | Test/benchmark |
|---|---|---|---|---|---|

If none:

```text
No safe runtime optimization opportunity identified from current evidence.
```

Do not let optimization analysis replace impact analysis.
