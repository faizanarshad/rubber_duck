# Graph Fingerprints

## Dimensions

```text
F1 AST shape
F2 CFG/control structure
F3 DDG/data-flow shape
F4 dominator/centrality/call-context
F5 CDG/control-dependence signature
F6 reaching definitions
F7 taint/source-sink connectivity
F8 type/effect signature
F9 comment-contract rationale
```

## Dimension status

Every pair/cluster must mark each dimension:

```text
COMPUTED
APPROXIMATED
SKIPPED
UNAVAILABLE
NOT_APPLICABLE
```

## Composite score rule

Composite score may include:

```text
COMPUTED dimensions
APPROXIMATED dimensions, if clearly labeled
```

Composite score must not include:

```text
SKIPPED
UNAVAILABLE
NOT_APPLICABLE
```

Skipped dimensions can reduce confidence but cannot increase similarity.

## Thresholds

Suggested:

```text
>= 0.85 strong match
0.70–0.84 likely match
0.55–0.69 possible match
< 0.55 weak / lookalike
```

## Matrix format

```markdown
| Pair | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | Included dimensions | Composite | Confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
```

If a tool limitation prevents a dimension, record it in `evidence/graph-dimension-coverage.md`.
