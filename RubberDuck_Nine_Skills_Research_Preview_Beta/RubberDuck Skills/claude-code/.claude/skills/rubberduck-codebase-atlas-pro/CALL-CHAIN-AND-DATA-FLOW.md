# Call Chain and Data Flow

## Call-chain diagram format

```text
entry()
  -> parser()
  -> orchestrator()
  -> domain object()
  -> output/write/response()
```

Each edge must have evidence:

```text
analysis_id
method
line/callee
coherence if available
```

## Data-flow diagram format

```text
source object
  -> transform
  -> state/config/domain object
  -> consumer
  -> output
```

## Cross-package emphasis

Tag each important edge:

```text
INTRA-PACKAGE
CROSS-PACKAGE
CROSS-LANGUAGE
EXTERNAL
UNKNOWN
```

Prioritize cross-package edges in the final atlas because they explain architecture boundaries.

## Cross-package coupling evidence table

The cross-package coupling map must include evidence:

```markdown
| Edge | Source package/file | Target package/file | Evidence tool | Evidence detail | Confidence |
|---|---|---|---|---|---|
```

Also include the edge tag:

```text
INTRA-PACKAGE
CROSS-PACKAGE
CROSS-LANGUAGE
EXTERNAL
UNKNOWN
```

Manual synthesis is allowed only if labeled `manual inference` and supported by source/search evidence.

In DEEP mode, mirror coupling edges at `evidence/cross-package-coupling.md`. Use one of these evidence labels for every row:

```text
RubberDuck call-chain
RubberDuck search
source-read
package metadata
manual synthesis with caveat
```

## Unresolved flow rule

If call_chain or trace_variable cannot resolve a path, report:

```text
unresolved
why
fallback evidence
confidence impact
```
