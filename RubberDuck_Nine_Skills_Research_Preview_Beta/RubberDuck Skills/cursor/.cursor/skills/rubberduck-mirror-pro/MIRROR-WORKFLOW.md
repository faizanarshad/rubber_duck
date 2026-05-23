# Mirror Workflow

## Phase 0 — Scope and target resolution

Resolve:

```text
repo / commit / branch
mode
before implementation
after implementation
preserved contract
out-of-scope effects
```

## Phase 1 — Import and module context

Before comparing bodies, inspect:

```text
imports
module-level constants
ambient state
export status
helper bindings
dependency versions if obvious
framework/runtime wrappers
```

Divergent imports may create divergent behavior even if bodies look similar.

## Phase 2 — Path catalogue

Build path catalogues for BEFORE and AFTER:

```text
guards
branches
early returns
exceptions
async/await
resource acquire/use/release
callback/event handlers
side effects
external calls
state mutations
```

## Phase 3 — Path reconciliation

Match paths:

```text
MATCHED
DIVERGENT
MISSING_IN_BEFORE
MISSING_IN_AFTER
UNDECIDABLE
```

Every unmatched path needs a reason.

## Phase 4 — Side-effect and exception comparison

Compare:

```text
outputs
mutations
I/O
network
filesystem
timers
events/listeners
resource lifecycle
logging/telemetry
exceptions/errors
async/concurrency behavior
```

## Phase 5 — Witness generation

For NOT_EQUIVALENT or CONDITIONAL verdicts, synthesize at least one witness input or state why not possible.

## Phase 6 — Test generation

Generate regression tests in the detected framework, or output standalone pseudo-tests if test framework cannot be identified.

## Phase 7 — Verdict

Use the verdict taxonomy. Include contract and confidence.

## Phase 8 — Falsification recipes

Every verdict must say what would refute it.
