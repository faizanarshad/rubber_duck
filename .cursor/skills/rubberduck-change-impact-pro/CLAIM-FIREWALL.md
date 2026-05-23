# Claim Firewall

Before final output, block or caveat unsupported claims.

## Block conditions

```text
claim has no evidence
negative claim lacks search/scope/caveat
tool was degraded and claim lacks caveat
local path leaks into shareable report
public API claim lacks export/path/package evidence
runtime optimization claim lacks equivalence test plan
```

## Required final note

Every report must state:

```text
This report is an impact analysis, not an implementation patch.
No implementation code is generated unless explicitly requested.
```
