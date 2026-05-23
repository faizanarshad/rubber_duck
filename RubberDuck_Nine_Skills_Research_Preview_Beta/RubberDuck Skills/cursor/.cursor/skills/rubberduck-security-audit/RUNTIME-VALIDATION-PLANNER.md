# Runtime Validation Planner

Tier-2 validation should be planned for high-risk findings.

## When Tier-2 is expected

```text
P0/P1 RCE
unsafe deserialization
auth bypass
cross-tenant impact
control-plane mutation
ReDoS/DoS
archive/resource exhaustion
credential leakage
```

## Plan fields

```text
finding ID
goal
harness type
dependencies
runtime setup
side effects
marker path
expected output
failure recovery
safety constraints
```

## Safe harness patterns

```text
TestClient
loopback fake server
fake runner/client
fixture database
monkeypatch
temp directory
marker file
short timeouts
bounded resource sizes
```

## Prohibited by default

```text
real third-party calls
real credential use
destructive DELETE/WRITE outside temp dir
shell execution unless explicitly safe and approved
network egress beyond loopback
```

## Failure behavior

If Tier-2 import/runtime fails:

```text
try recovery sequence
document exact blocker
keep Tier 1
mark runtime validation incomplete
do not call complete if P0/P1 and Tier-2 was feasible
```
