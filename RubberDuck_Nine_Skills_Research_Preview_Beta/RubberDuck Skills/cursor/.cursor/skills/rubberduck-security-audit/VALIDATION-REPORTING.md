# Validation and Reporting

## Promotion rule

A candidate can be promoted only if the report proves:

```text
entry point
attacker control
trust boundary crossed
transformations
guards present
guards missing/insufficient
callee-side invariant rechecks
privileged operation
realistic exploitability
source evidence
evidence tier
```

## P0/P1 Tier-2 rule

For P0/P1 RCE, unsafe deserialization, command/code execution, auth bypass, or cross-tenant impact claims:

```text
Attempt Tier-2 unless user forbids runtime checks.
If Tier-2 fails, execute recovery sequence.
If still blocked, mark report: source-confirmed; runtime validation incomplete.
```

Prior Tier-2 cannot be silently downgraded:

```text
reproduce it,
reuse/link it,
invalidate it,
or mark runtime-validation incomplete.
```

## Documented-trust policy

Separate severities:

```text
single-tenant/operator-authored
trusted publisher
untrusted publisher
multi-tenant marketplace
user-uploaded artifact
build-time supply chain
runtime execution
```

## Prior-reviewed severity lock

If a reviewed prior report classifies a finding as High or Critical, preserve that severity unless a dedicated downgrade note proves at least one of:

```text
the vulnerable code changed
the exploit path no longer reaches the sink
the reviewed threat model is explicitly out of scope for this rerun
the prior report's severity basis is factually wrong
```

If none is proven, preserve the prior severity. Caveats about preconditions are allowed, but they do not justify silently reducing severity.

## Supply-chain RCE floor

For build, release, packaging, CI/CD, installer, artifact-generation, or package-publishing paths:

```text
attacker-influenced input -> shell/code execution on artifact-producing or publishing host = minimum High severity
```

Only lower this if the audit proves the host cannot access sensitive credentials and cannot affect distributed artifacts. Constrained build-input reachability may reduce likelihood, but not impact; write this as "High impact with constrained preconditions," not Medium, unless the downgrade rule is satisfied.

## Safe validation

Prefer:

```text
TestClient
loopback server
fake runner/client
fixture DB rows
monkeypatch
temp dir
marker-file gadget
no shell
no real third-party systems
```

## Runtime recovery sequence

```text
inspect pyproject/setup
create clean venv
editable install or wheel install
install minimal extras
patch only safe generated metadata/version stubs
use TestClient or loopback
use function-level harness if app import fails
label direct sink-block harness as Tier-2-lite
```

## Finding write-up fields

```text
title
category/root cause
evidence tier
entry point
attacker language
data flow
trust boundary
guards present/missing
high-risk operation
broken assumption
confidence
risk
non-destructive validation
worst-case impact
minimal fix
regression tests
rollout/rollback
```
