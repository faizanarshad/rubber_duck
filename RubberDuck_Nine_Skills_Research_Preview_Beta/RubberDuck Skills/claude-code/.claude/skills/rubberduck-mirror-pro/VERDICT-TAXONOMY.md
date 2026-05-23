# Verdict Taxonomy

Use exactly one verdict:

```text
PROVEN_EQUIVALENT_UNDER_CONTRACT
NOT_EQUIVALENT
CONDITIONALLY_EQUIVALENT
EQUIVALENT_WITH_STRUCTURAL_DRIFT
UNDECIDABLE
HEURISTIC_ONLY
```

## Requirements

### PROVEN_EQUIVALENT_UNDER_CONTRACT

Requires:

```text
preserved_contract stated
all comparable paths matched
0 divergent paths
0 undecidable blockers
side-effect comparison complete or explicitly out of scope
exception comparison complete or explicitly out of scope
falsification recipe present
```

### NOT_EQUIVALENT

Requires:

```text
at least one divergence
witness input or witness blocker
generated test or reason test cannot be generated
```

### CONDITIONALLY_EQUIVALENT

Requires:

```text
conditions listed
paths/effects outside condition listed
tests for condition boundaries
```

### EQUIVALENT_WITH_STRUCTURAL_DRIFT

Use when behavior matches under contract but structure differs enough to affect maintainability, observability, performance, or future changes.

### UNDECIDABLE

Use when dynamic dispatch, external state, missing semantics, unsupported language, missing source, or environmental dependency blocks a verdict.

### HEURISTIC_ONLY

Use for advisory comparisons, especially cross-language or low-evidence contexts.
