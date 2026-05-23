# Proof-Carrying Patch and Runtime Instrumentation

For each validated finding, generate:

```text
minimal fix
defense-in-depth fix
regression test
negative test
rollout plan
rollback plan
production instrumentation
```

## Proof-carrying patch format

```text
Input X reaches sink Y without guard Z.
Patch adds guard Z at adapter A.
Regression test fails before and passes after.
Verification calls confirm source no longer reaches sink.
```

## Runtime instrumentation examples

```text
ReDoS -> regex execution-time histogram, slow-pattern alert
SSRF -> blocked internal IP egress counter
deserialization -> dangerous content-type alert
archive DoS -> extracted byte/member/ratio metrics
task control -> task_id access logs and anomaly detection
auth bypass -> 401/403 ratios and unsigned-request counters
credential file -> file-mode check in startup health
```
