# Repo Intelligence Brief

The Repo Intelligence Brief is the bridge between RubberDuck evidence and a repo-specific audit prompt.

## Purpose

A generic prompt wastes effort. The brief makes the audit adaptive:

```text
RubberDuck evidence -> repo facts -> selected playbooks -> tailored audit prompt
```

The brief must consume the deterministic census. RubberDuck evidence identifies semantic risk; the census prevents file/sink classes from disappearing because the scanner did not rank them highly.

## Inputs

Use:

```text
detailed_repo_analysis
load_code inventory
analysis-ID map
symbols_overview
top scanner clusters
taint flows
scan_bug_signals
search_code discovery
file inventory
sink census
route/file census
API-response/file census
subprocess census
secrets/logging census
network-fetch census
auth/session census
unsupported surfaces
prior reports
tool-health notes
```

## Required template

```markdown
# Repo Intelligence Brief

## Repo class
<ML model server / AI agent / web API / CLI tool / CI action / parser / SDK / build tool / cloud client / etc.>

## Primary languages
...

## Supported semantic surface
...

## Unsupported surfaces
| Surface | Count | Privilege | Router | Status |
|---|---:|---|---|---|

## Entry points
...

## Attacker languages
...

## Privilege domains
...

## Adapters
...

## High-risk trust-boundary transitions
...

## Top scanner signal clusters
| Cluster | Files | Raw severity | Likely root cause | Triage plan |
|---|---|---|---|---|

## Top census clusters
| Census | Files | Row count | Privileged? | Triage plan |
|---|---|---:|---|---|

## Route/file and API-response/file surfaces
| Surface | Files | Why privileged | Current disposition |
|---|---|---|---|

## Likely false-positive clusters
...

## Tool health and degraded areas
...

## Prior-run candidates requiring reconciliation
...

## Selected specialist playbooks
...

## Specialist playbooks explicitly not selected
| Playbook | Reason |
|---|---|

## Universal baseline sweeps
...

## Tier-2 validation opportunities
...

## Claims currently unsupported
...
```

## Repo class examples

Use repo class to select emphasis, not to skip universal baseline.

```text
ML/model-serving:
  model artifact loading, serde/content-type dispatch, inter-service protocols, archives, URL/file ingestion

AI agent:
  prompt/tool boundary, durable memory/schedules/summaries, OAuth tools, prompt-adjacent sidecars

CI/CD action:
  workflow YAML, shell, env vars, token permissions, checkout, artifacts, external actions

CLI/build tool:
  argv option injection, config-to-action, subprocess, repository files, plugin scripts

Parser/processor:
  file content, decompression, archive traversal/DoS, parser CVEs, ReDoS

Web API:
  auth/authz, SSRF, injection, object-level authorization, control-plane IDs
```
