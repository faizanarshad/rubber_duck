# Coverage Governance

Coverage is security evidence. A report cannot claim what its coverage does not support. This governance starts only after CI semantic full has completed; without completed CI semantic full, abort instead of continuing with partial coverage.

## Coverage surfaces

Track separately:

```text
full repo inventory
supported semantic surface
semantically loaded files
semantically queried files
source-read-only files
grep-only files
unsupported file types
external repos/actions/dependencies
runtime-only surfaces
```

Do not collapse these into one "coverage" number.

## Required coverage table

```text
Surface | Total | Loaded | Queried | Source-read | Grep-only | Unsupported | Status | Claim limit
```

The table must include census status:

```text
file inventory
sink census
route/file matrix
API-response/file matrix
subprocess matrix
secrets/logging matrix
network-fetch matrix
auth/session matrix
deserialization/archive matrix
crypto matrix
prior-finding regression ledger
```

Statuses:

```text
complete
complete-with-accepted-gaps
post-CI-source-confirmed-partial
tooling-blocked
unsupported-routed
out-of-scope
```

## Critical Surface Coverage Plan

Before validation, create a ranked plan:

```text
surface
why privileged
entry points
files/directories
coverage target
tool path
post-CI fallback path
status
```

High-risk surfaces include:

```text
routes/gateways/transports
auth/authz/session
tool execution
sandbox backends
model loaders
plugin loaders
memory/schedule/sidecars
CLI/build/deploy
network fetch
archive extraction
credential storage
top-level orchestration files
unsupported but privileged scripts/workflows
```

High-risk surface selection is not sampling permission. Selection only controls validation order after the full census exists. Any privileged census row left untriaged blocks a complete report.

## Open Coverage Gap Register

Every uncovered or partially covered high-risk surface requires:

```text
surface
files/count
why high-risk
what was covered
what was not covered
why not covered
post-CI fallback attempted
next step
does this block "Complete"?
claim limit
```

If open gaps cover privileged or externally reachable surfaces, the audit status cannot be simply "Complete". Use:

```text
source-confirmed partial
tooling-blocked partial
complete-with-accepted-gaps
```

## Coverage arithmetic rules

Do not say:

```text
100% coverage
```

unless all of these are true:

```text
supported semantic files loaded
high-risk unsupported surfaces routed
post-CI source-read/grep fallbacks completed
coverage gaps have status and risk
```

Allowed wording:

```text
100% semantic coverage for supported Python/TypeScript files loaded.
Shell/YAML/Dockerfile/PowerShell routed separately.
N privileged surfaces remain post-CI source-confirmed or open.
```

## Empty or impossible CPG detector

Treat these as invalid or degraded, not clean:

```text
detailed_repo_analysis returns 0 files / 0 graph nodes for a repo known to contain files
history says thousands of files but current graph says zero
security score is perfect because analyzed file count is zero
CI report describes only a tiny change set while task scope is full repo
semantic_loaded shows analyses but repo storage is missing
```

When this occurs:

```text
do not use the clean grade as evidence
mark CI/CPG as degraded or stale
try recovery ladder
after CI semantic full completion only, fall back to local source with reduced claim scope
```

## Coverage claim firewall

Every final claim must include scope:

```text
within semantically loaded files
within source-read files
within grep-only full repo
within unsupported routed surface
out of scope
```

Unsupported and uncovered surfaces invalidate broad "no high vulnerabilities" claims.

## Exhaustive completion gate

For complete reports, run:

```bash
python <installed_skill_dir>/scripts/check_exhaustive_completion.py --root <report_bundle_dir>
```

If the checker reports untriaged privileged rows, missing census ledgers, or prior findings without status, the audit is incomplete until those rows are resolved or explicitly blocked with evidence.
