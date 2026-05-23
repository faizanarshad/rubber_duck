# RubberDuck Security Audit Report Template

```markdown
# <Repo> — Security Review Report

| Field | Value |
|---|---|
| Repository | owner/repo |
| Local path | <path> |
| Commit | <hash> (<branch>) |
| Scan date | YYYY-MM-DD |
| Scan type | Full / Vuln / Targeted / Re-audit |
| RubberDuck instance_id | <id> |
| MCP environment | prod/dev |
| Audit status | Complete / Draft / Blocked - CI semantic full unavailable / Post-CI source-confirmed but runtime-validation incomplete |
| Runtime validation status | Tier-2 reproduced / reused / blocked / not attempted |
| Validation basis | RubberDuck CI semantic full + source + Tier-2 / post-CI source-confirmed graph-degraded |
| Protocol completion check | passed / failed / not run |
| Report consistency check | passed / failed / not run |

## Executive Summary

## Scope and Coverage Integrity

## Exhaustive Census Summary

| Census | Rows | Untriaged | Promoted | Hardening | False positive / expected | Blocked |
|---|---:|---:|---:|---:|---:|---:|

## Route / File Matrix

| Route | Handler | Param source | File operation | Containment guard | Exposure/CORS | Disposition |
|---|---|---|---|---|---|---|

## API-Response / File Matrix

| Source | Field | Local path construction | File operation | Guard | Disposition |
|---|---|---|---|---|---|

## Repo Intelligence Brief

## Compiled Audit Prompt

## Tool Health and Degradation

## Unsupported Surface Routing

| Surface | Count | Privilege | Review path | Status |
|---|---:|---|---|---|

## System Model

### Attacker Languages
### Privilege Domains
### Adapters
### Strongest Trust-Boundary Transitions

## Ranked Exploit Hypotheses

## Prior-Run Regression Ledger

| Prior ID | Prior report | Prior status | Current status | Root-cause family | Evidence | If absent, why |
|---|---|---|---|---|---|---|

## RubberDuck Detection Summary

## Candidate Ledgers

### R-ledger — RubberDuck Signals
### H-ledger — Graph Hypotheses
### M-ledger — Rescue Sweep Candidates
### P-ledger — Prior-Run Candidates
### Sink Census Ledgers
### Claim Ledger
### Negative-Claim Ledger

## Mandatory Rescue Sweep Tables

Include when applicable:
- ML/model-artifact loader table
- URL-fetch / SSRF table
- Opaque-ID control-plane table
- Argv option-injection table
- Archive traversal-vs-DoS table
- Unsupported-surface table

## Root-Cause De-duplication

| Family | Root cause | Shared fix | Counted severity | Variants preserved |
|---|---|---|---|---|

### Root-cause variant table

| Variant | Entry point | Attacker position | Sink / operation | Evidence tier | Status |
|---|---|---|---|---|---|

## New Validated Findings Only

### F-001 — <Title>

| Field | Value |
|---|---|
| Severity | |
| CWE / category | |
| Evidence tier | |
| File(s) | |
| Entry point | |
| Attacker language | |
| Data flow | |
| Trust boundary | |
| High-risk operation | |
| Broken assumption | |
| Guards present | |
| Guards missing | |
| Confidence | |
| Risk | |
| Non-destructive validation | |
| Worst-case impact | |

## Ruled-Out or Weakened Hypotheses

## Informational / Defense-in-Depth

## False Positive / Overcount Analysis

## Tooling Issues and Likely Fixes

## Claim Firewall Result

## Exhaustive Completion Check Result

## Protocol Completion Check Result

## Consistency Check Result

## Recommendations, Regression Tests, and Instrumentation
```
