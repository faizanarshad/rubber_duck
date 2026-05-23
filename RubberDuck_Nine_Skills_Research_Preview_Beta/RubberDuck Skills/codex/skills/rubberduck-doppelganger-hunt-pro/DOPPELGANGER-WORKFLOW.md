# Doppelganger Workflow

## Phase 0 — Mode selection

Declare exactly one:

```text
SEEDED
CONCEPT
UNCONSTRAINED
```

Required envelope fields:

```text
repo
commit
instance_id
mode
seed or concept
tool-call count
candidate generators run
candidate count before/after prefilter
clusters found
evidence-pack mode
limitations
```

## Phase 1 — Candidate generation

Run multiple candidate generators. Do not rely on one search.

Minimum for SEEDED:

```text
seed symbol/source read
name/lexical search
effect-token search
API-call search
type signature search
inline-pattern search
caller/callee context search
comment/doc search
```

Minimum for CONCEPT:

```text
concept keyword search
API/effect-token search
type/effect search
inline-pattern search
test/prod split search
comment/doc search
```

Minimum for UNCONSTRAINED:

```text
CI redundancy/near-duplicate seeds
hotspot/function inventory
public API inventory
test helper inventory
inline effect-pattern search
candidate-generator ledger
```

## Phase 2 — Fingerprint short-list

For candidates, compute or mark unavailable:

```text
F1 AST shape
F2 CFG/control structure
F3 DDG/data-flow shape
F4 dominator/centrality/call-context
F5 CDG/control-dependence guards
F6 reaching definitions
F7 taint/source-sink connectivity
F8 type/effect signature
F9 comment-contract/historical rationale
```

F9 is not included in structural score by default; it explains divergence and mergeability.

## Phase 3 — Cluster formation

Cluster by:

```text
same intended effect
compatible type/effect signature
similar control/data-flow shape
shared resource lifecycle
shared call-context or role
not merely name similarity
```

## Phase 4 — Role and mergeability

Classify every member:

```text
CANONICAL
HIDDEN_CANONICAL
WRAPPER_OR_ORCHESTRATOR
ACCIDENTAL_REIMPLEMENTATION
INLINE_COPY
TEST_FIXTURE_COPY
DELIBERATE_DIVERGENCE
SELECTOR_OR_ADAPTER
LOOKALIKE_NOT_DUPLICATE
```

Classify mergeability:

```text
SAFE_TO_MERGE
API_CHANGING
TEST_ONLY_CLEANUP
KEEP_SEPARATE
DELIBERATE_DIVERGENCE
NEEDS_INVESTIGATION
```

## Phase 5 — Unification plan

Only produce a unification plan after change-impact preflight.

The plan must include:

```text
PR sequence
risk per PR
tests to run
export/API impact
behavioral differences
what not to merge
rollback plan
```
