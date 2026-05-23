# False Positives and Root-Cause De-duplication

## Core rule

Normalize by root-cause family before counting. Scanner-rich runs over-split sink fan-out.

Collapse counts when variants share:

```text
same entry primitive
same trust boundary
same broken assumption
same fix
```

But de-duplication collapses vulnerability counts, not evidence obligations.

## Root-cause family table

```text
Family | Root cause | Shared fix | Counted severity | Variants preserved
```

## Variant table

Every root cause must preserve:

```text
Variant | Entry point | Attacker position | Sink / operation | Evidence tier | Current status
```

## Do not erase variants

Do not allow "same root cause" to erase:

```text
response-side vs request-side
external route vs internal channel
runtime vs build-time
single-tenant vs cross-tenant
Tier-2 vs Tier-1 evidence
different attacker positions
```

## Common false positives

```text
argv-array as shell injection without option-injection analysis
operator-supplied cloud endpoint as SSRF
vendored static JS as server RCE
test fixture sinks as production issues
bind-all if source downgrades/refuses public bind
JSON parser as XXE
fixed host fetch as SSRF
safe SQL template interpolation as SQLi
```

## Do not over-demote

For subprocess findings, distinguish:

```text
shell metacharacter injection
argv option injection
operator-only invocation
untrusted publisher/build input
```

Only the first is ruled out by argv arrays.

## False-positive write-up

For every FP category:

```text
candidate
why it looked dangerous
source evidence
why not exploitable
remaining hardening note if any
```
