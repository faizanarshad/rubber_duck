# Defense Verification

Security review should validate defenses, not only bugs.

## Defense ledger

Create a D-ledger for important defenses:

```text
defense ID
defense function/file
threat it is meant to block
input classes handled
bypass cases checked
tool evidence
source evidence
status: strong / partial / brittle / bypassed / not reached
```

## Defenses to look for

```text
auth checks
token comparisons
content-type blocks
URL/IP guards
archive path guards
regex/prompt scanners
memory/sidecar sanitizers
context fences
sandbox allowlists
dangerous command filters
plugin load restrictions
profile/archive extractors
CSRF/session controls
rate limits and timeouts
```

## Bypass-oriented checks

For each defense, ask:

```text
does the guard run before parsing/body use?
does the guard apply to all sibling paths?
does the guard depend on platform/runtime/backend?
does replacement/normalization happen before or after scanning?
does a second sink exist after the guard?
is fail-open possible?
what edge cases bypass same-line or multi-step defenses?
```

## Report requirement

Validated defenses should appear in the report as:

```text
Defense | Threat | Evidence | Bypass cases checked | Status
```

This prevents false positives and makes "ruled out" claims defensible.
