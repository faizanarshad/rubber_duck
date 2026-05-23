# Change Type Playbooks

## Rename

Check:
```text
imports
exports
barrel files
mock factories
vi/jest mocked symbol calls
comments
docs
string references
type declarations
public API aliases
```

## Signature change

Check:
```text
all call shapes
positional/keyword args
optional/default params
overloads/interfaces
test helper calls
mock implementations
external/public consumers
```

## Behavior change

Check:
```text
invariants
comment contracts
test oracles
edge cases
state transitions
callees
runtime optimization equivalence
```

## Deprecate

Check:
```text
public API proof
migration window
alias/shim
warnings
docs
semver
downstream consumers
```

## Remove

Check:
```text
dead-code proof
public API proof
external references
tests
docs
semver/migration
fallback behavior
```

## Move

Check:
```text
import paths
path aliases
barrel exports
circular dependencies
package boundaries
test imports
docs
```

## Optimize

Check:
```text
same observable result
deterministic exactness or ±5% tolerance if approximate domain
benchmark/profiling plan
equivalence tests
allocation/I/O/concurrency/cache effects
```
