# Side-Effect Manifest

Extract side effects in source/CFG order.

Categories:

```text
return value
state mutation
object mutation
file I/O
network I/O
process/subprocess
timers
events/listeners
resource acquire/release
logging/telemetry
database/cache
environment reads/writes
```

Output:

```text
Effect | BEFORE | AFTER | Equivalent? | Evidence
```

For resource lifecycle:

```text
acquire
use
release
failure paths
early rejection/throw paths
```

Resource leaks are NOT_EQUIVALENT unless explicitly out of scope.
