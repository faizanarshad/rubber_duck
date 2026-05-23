---
name: rubberduck-security-audit
description: RubberDuck Security Audit: an evidence-governed RubberDuck security audit compiler. Use for repository security audits, PR delta security reviews, vulnerability hunts, pentests, audit-run comparisons, scanner-finding validation, and defensible security reports. Builds a repo intelligence brief, full file inventory, deterministic sink census, repo-specific audit prompt, capability graph, universal/specialist playbooks, evidence ledgers, claim firewall, prior-run reconciliation, Tier-2 validation planning, root-cause de-duplication, security delta reports, and consistency checks.
trigger: when performing a security audit, repository security review, pentest, vulnerability hunt, CVE/CWE report, RubberDuck-backed code review, audit-report comparison, or scanner-finding validation against source
version: 2026-05-21-rubberduck-security-audit-exhaustive-default
---

# RubberDuck Security Audit

RubberDuck Security Audit is a methodology-only skill for high-rigor white-hat code review. It uses RubberDuck's rich codebase and semantic intelligence as **audit-planning evidence**, not merely as a vulnerability scanner.

The central idea:

```text
RubberDuck scan
  -> Repo Intelligence Brief
  -> full file inventory + deterministic sink census
  -> repo-specific audit prompt
  -> specialist playbooks + universal baseline
  -> evidence-led validation
  -> claim firewall
  -> consistency verifier
  -> report + evidence pack
```

This package intentionally contains **no repo-specific private expected-result files, private vulnerability corpora, or named private regression corpus targets**. Keep private regression corpora outside the distributable skill.

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure which RubberDuck skill to use, or this task should start with repo intelligence or continue into remediation planning/build after the audit, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

## PR delta security review

When the task is to decide whether a feature PR is safe to mark ready, read `RUBBERDUCK-SECURITY-DELTA-GATE.md` and run `PR_DELTA_SECURITY_REVIEW` mode instead of a full repo cleanup. Compare RubberDuck base branch findings with PR-head findings, classify new/pre-existing/fixed/adjudicated findings, and block only unresolved new Critical/High findings in changed or newly created code by default.

Do not ask the agent to eliminate every RubberDuck finding in the repository unless the user explicitly requests a broad cleanup. Pre-existing findings remain baseline debt and must be reported separately.

## Core operating principle

Do not ask one generic prompt to audit every repository. First learn what the repository is.

```text
1. Run RubberDuck CI with `detailed_repo_analysis(..., semantic_mode="full")` and repeat/wait until the full report completes.
2. Build a Repo Intelligence Brief from the completed CI semantic full evidence.
3. Build a full repository file inventory and deterministic sink census.
4. Compile a repository-specific audit prompt from both RubberDuck and the census.
5. Execute universal and specialist playbooks over the census rows.
6. Govern every final claim with evidence.
```

The same process repeats across repos; the threat model and playbook emphasis are repo-specific.

## Default audit standard

This skill optimizes for client-grade completeness over token economy. A normal security audit is exhaustive by default:

```text
No sampling for final reports.
Every file is inventoried.
Every dangerous operation is entered into a census ledger.
Every privileged census row is triaged with an evidence pointer.
If that cannot be completed, the report is incomplete, not complete.
```

The audit may prioritize which rows receive deep graph/runtime validation first, but it may not omit census categories or finalize with untriaged privileged rows.

## Non-negotiable rules

1. Always use `semantic_mode="full"` for the CI RubberDuck audit call and repeat/wait until it completes.
2. Never run the Security Audit protocol, compile the repo prompt, or produce a report unless CI semantic full has completed; if repeated attempts fail, abort the session and report the blocker.
3. Run RubberDuck first for coverage, but do not let scanner findings define the threat model.
4. Build a full file inventory and deterministic sink census before specialist triage.
5. Sampling is not allowed for final security reports. Targeted deep dives are allowed only after the census exists.
6. Every route/file, API-response/file, subprocess, secrets/logging, network-fetch, auth/session, deserialization/archive, crypto, and config-to-action row must be triaged or explicitly blocked.
7. Build a capability graph before final CWE/sink triage.
8. Use the Repo Intelligence Brief and census ledgers to generate a tailored audit prompt.
9. Run the universal baseline even when the tailored prompt de-emphasizes a class.
10. Tool output is a lead, not a fact.
11. Search hits are candidates, not findings.
12. Negative claims require explicit search/scope evidence.
13. Prior-run candidates may not disappear silently. If prior reports are provided, parse them before final triage and give every prior finding a current status.
14. P0/P1 findings require Tier-2 attempt or documented blocker.
15. Unsupported surfaces must be routed, not hidden.
16. Preserve team-reviewed High/Critical prior severity unless a dedicated downgrade note proves a valid downgrade basis.
17. Treat build/release/package-publishing code execution on artifact-producing hosts as at least High impact unless credential and artifact influence are both disproven.
18. The final report must pass the claim firewall, exhaustive completion check, protocol completion check, and consistency checks.

## Protocol supervision gate

Completion must be artifact-backed, not memory-backed.

At audit start, create `ledgers/protocol-completion.md` or, before the report bundle exists, maintain an equivalent visible phase checklist. After every phase, update it with:

```text
phase
required actions
tools/commands run
result
evidence pointer
degraded/blocking status
next incomplete action
```

Before any final report or final answer, re-open that matrix and run:

```bash
python scripts/check_protocol_completion.py --root <report_bundle_dir>
python scripts/check_exhaustive_completion.py --root <report_bundle_dir>
python scripts/verify_report_consistency.py --root <report_bundle_dir>
```

Do not say the full protocol is complete unless all checks pass with no unresolved warnings/errors, every phase row is `complete` or `complete-with-accepted-gaps`, all privileged census rows are triaged, and every gap has an explicit non-blocking rationale. If the user asks whether the protocol was completed, inspect the matrix and checker outputs first; never answer from recollection.

## Required docs in this package

Load only the docs needed for the current phase.

```text
RUBBERDUCK-WORKFLOW.md              Command choreography and tool-health rules
REPO-INTELLIGENCE-BRIEF.md          Evidence extraction from RubberDuck into a repo profile
AUDIT-PROMPT-COMPILER.md            How to generate a repo-specific audit prompt
CAPABILITY-GRAPH.md                 Attacker language -> adapter -> privilege model
SPECIALIST-PLAYBOOKS.md             Repo-class-specific playbook selection
RESCUE-SWEEPS.md                    Universal mandatory sweeps
EXHAUSTIVE-CENSUS.md                Default full-repo census, ledgers, and checker gates
UNSUPPORTED-SURFACE-ROUTER.md       Shell/YAML/Docker/IaC/Markdown routing
COVERAGE-GOVERNANCE.md              Coverage arithmetic, critical-surface coverage, open gap gates
EVIDENCE-GOVERNANCE.md              Evidence ledger, claim classes, negative-claim rules
CLAIM-FIREWALL.md                   Final claim gating
TOOL-HEALTH-SENTINEL.md             Cache/parser/coverage/degradation gates
PROTOCOL-COMPLETION.md              Required phase/tool/finding completion matrix
DEFENSE-VERIFICATION.md             Validate defenses and bypass cases
LOCAL-GREP-FALLBACK.md              Post-CI source fallback for semantic loading gaps after CI semantic full completes
VALIDATION-REPORTING.md             Evidence tiers, severity, prior-run regression
FALSE-POSITIVES-DEDUP.md            Root-cause compression and FP handling
RUNTIME-VALIDATION-PLANNER.md       Tier-2 planning and recovery
PROOF-CARRYING-PATCH.md             Fix/test/instrumentation planning
REPORT-TEMPLATE.md                  Final report and evidence pack structure
RUBBERDUCK-SECURITY-DELTA-GATE.md   PR base-vs-head security delta gate for build/autonomous workflows
```

## Audit modes

```text
FULL_REPO_SECURITY_AUDIT
TARGETED_SECURITY_REVIEW
PR_DELTA_SECURITY_REVIEW
```

Use `PR_DELTA_SECURITY_REVIEW` for feature PRs, autonomous build final sweeps, and "make this PR clean" requests unless the user explicitly asks for a whole-repo cleanup. This mode produces `security-delta.json`, `security-delta.md`, and `finding-adjudication.json`.

PR delta reports must end with exactly one security delta label, including:

```text
Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH
Security delta status: NEW_FINDINGS_ADJUDICATED
Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS
Security delta status: NOT_RUN_LOCAL_ONLY
```

## Phase overview

```text
Phase 0    Scope and commit pinning
Phase 1    RubberDuck full scan and semantic loading
Phase 1.5  Coverage governance and tool-state sanity checks
Phase 1.6  Full file inventory and deterministic sink census
Phase 2    Repo Intelligence Brief
Phase 3    Repo-specific audit prompt compilation
Phase 4    Capability graph and ranked hypotheses
Phase 5    Universal baseline + specialist playbooks
Phase 6    RubberDuck detection stack and graph-guided searches
Phase 6.5  Local grep/source fallback only after CI semantic full has completed
Phase 7    Unsupported and uncovered surface routing
Phase 8    Ledgers: R/H/M/P/F/D + claim + negative-claim + coverage-gap ledgers
Phase 9    Validation loop, per-finding protocol matrix, and Tier-2 planning
Phase 10   Defense verification and root-cause de-duplication
Phase 11   Claim firewall
Phase 12   Protocol completion and report consistency verification
Phase 13   Final report + evidence pack
```

## Phase 0 — Scope and commit pinning

Record:

```text
repo/path
branch
commit
local path
scan type: vuln / full / targeted / re-audit
RubberDuck environment: prod/dev
GitHub App/mirror status
languages and package managers
runtime/deployment context
secrets/runtime availability
prior reports provided
```

Write this to `SCOPE.md` before starting validation.

Local baseline when available:

```bash
git rev-parse HEAD
git status --short
git ls-files | wc -l
tokei . || cloc .
```

## Phase 1 — RubberDuck full scan and semantic loading

Start with:

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="main",
    semantic_mode="full",
)
```

Completion gate:

```text
Repeat `detailed_repo_analysis(..., semantic_mode="full")` and wait/poll until the full CI semantic report is returned. A response that only says indexing started, queued, pending, degraded, refused, or unavailable is not completion. If repeated attempts fail, stop the audit and report the exact blocker; do not continue with the Security Audit protocol without CI semantic full completion.
```

Poll semantic readiness:

```python
get_started(repo="<owner/repo or authorized mirror>")
```

Load relevant files with `instance_id`:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

Repeat for applicable supported extensions.

Build and save:

```text
analysis_id -> file_path -> extension -> line_count -> current repo confirmed
```

Never trust a bare duplicate stem analysis ID until mapped.

## Phase 1.5 — Coverage governance and tool-state sanity checks

Before claiming coverage or cleanliness, build coverage tables from `COVERAGE-GOVERNANCE.md`.

Required checks:

```text
full repo inventory vs analyzed files
supported semantic surface vs loaded files
loaded files vs semantically queried files
source-read-only files
grep-only files
unsupported file types
external/out-of-scope surfaces
open coverage gaps
```

Block or downgrade broad claims when:

```text
semantic coverage is low for privileged surfaces
high-risk directories/files are unqueried
detailed_repo_analysis returns impossible zero-file / zero-node metrics
cached clean report contradicts repo inventory/history
repo storage is evicted and new load_code calls fail
tool output is truncated and saved result was not parsed
```

If semantic loading is blocked after CI semantic full has completed, run the recovery ladder in `LOCAL-GREP-FALLBACK.md` and label claims `source-confirmed, graph-degraded`. If CI semantic full itself has not completed, abort instead of falling back.

## Phase 1.6 — Full file inventory and deterministic sink census

Run the default exhaustive census before repo-specific prompt compilation and before selecting deep-dive validation order:

```bash
python <installed_skill_dir>/scripts/build_sink_census.py \
  --root <repo_root> \
  --out <report_bundle_dir>
```

`<installed_skill_dir>` means the copied `rubberduck-security-audit` skill folder for the current platform.


The script writes:

```text
ledgers/file-inventory.md
ledgers/sink-census.md
ledgers/route-file-census.md
ledgers/api-response-file-census.md
ledgers/subprocess-census.md
ledgers/secrets-logging-census.md
ledgers/network-fetch-census.md
ledgers/auth-session-census.md
ledgers/deserialization-archive-census.md
ledgers/crypto-census.md
```

Every row starts as `untriaged`. Before final reporting, change each row disposition to one of:

```text
promoted
false-positive
hardening
expected-behavior
fixed
out-of-scope
blocked
```

Rows touching routes, file operations, subprocesses, secrets, auth/session state, network fetch, archive/deserialization, crypto, or config-to-action are privileged by default. Untriaged privileged rows block a complete report.

See `EXHAUSTIVE-CENSUS.md`.

## Phase 2 — Repo Intelligence Brief

Before final triage, write a Repo Intelligence Brief.

Minimum fields:

```text
Repo class:
Primary languages:
Supported semantic surface:
Unsupported surfaces:
Entry points:
Attacker languages:
Privilege domains:
Adapters:
High-risk trust-boundary transitions:
Top scanner signal clusters:
Top census clusters:
Raw false-positive clusters:
Tool health / parser confidence:
Prior-run candidates:
Selected specialist playbooks:
Specialist playbooks explicitly not selected:
Universal baseline sweeps:
Tier-2 validation opportunities:
Claims currently unsupported:
```

See `REPO-INTELLIGENCE-BRIEF.md`.

## Phase 3 — Compile the repo-specific audit prompt

Generate a tailored audit prompt from the Repo Intelligence Brief.

The compiled prompt must contain:

```text
repo class and threat model
priority attacker languages
priority privilege domains
priority adapters
selected specialist playbooks
mandatory universal baseline
mandatory census matrices
unsupported-surface routes
expected false-positive clusters
negative-claim requirements
Tier-2 targets
prior-run regression requirements
final report gates
```

Important:

```text
Repo-specific prompt changes emphasis, not baseline coverage.
```

See `AUDIT-PROMPT-COMPILER.md`.

## Phase 4 — Capability graph

Use:

```text
attacker language A -> adapter X -> representation B -> adapter Y -> privilege domain Z
```

Generate ranked hypotheses before final sink/CWE triage. See `CAPABILITY-GRAPH.md`.

## Phase 5 — Universal baseline + specialist playbooks

Universal baseline always includes:

```text
auth/authz
unsafe deserialization
subprocess/shell/argv option injection
SSRF/URL fetch
file/archive/path traversal
archive resource exhaustion
ReDoS
SQL/template injection
credential storage
tenant/batch invariants
opaque-ID control planes
durable sidecars
unsupported surfaces
```

Then run specialist playbooks selected from repo class and census content, such as:

```text
ML/model-artifact
AI-agent sidecar
CI/CD workflow
CLI/build tool
web API auth
parser/processor
archive/file ingestion
plugin/import-by-name
cloud credential
```

See `SPECIALIST-PLAYBOOKS.md` and `RESCUE-SWEEPS.md`.

Specialist selection changes validation order, not census coverage. Every privileged census row still requires a disposition.

## Phase 6 — Detection and validation stack

Run layered RubberDuck and source validation.

```python
assess(mode="repo_detailed", repo="owner/repo")

assess(
    mode="security",
    repo="owner/repo",
    analysis_id="<aid>",
    include_ci=true,
)

scan_bug_signals(
    analysis_id="<aid>",
    families="all",
    min_suspicion="low",
)
```

Use:

```python
query_action(action="symbols_overview", analysis_id="<aid>")
query_action(action="trace_variable", analysis_id="<aid>", var="<var>")
query_action(action="call_chain", analysis_id="<aid>", method="<method>")
query_action(action="control_guards", analysis_id="<aid>", line=<line>)
query_action(action="def_sites", analysis_id="<aid>", var="<var>")

logic_analysis(action="risk_score", analysis_id="<aid>", target="<function>")
logic_analysis(action="simulate_paths", analysis_id="<aid>", target="<function>", scenario="attacker-controlled X reaches privileged Y")
read_source(analysis_id="<aid>", function_name="<function>")
read_source(analysis_id="<aid>", start_line=<n>, end_line=<m>)
```

## Phase 7 — Unsupported and uncovered surface routing

Create unsupported and uncovered surface tables. Do not imply unsupported or unqueried surfaces are covered.

Examples:

```text
Shell scripts -> shell/argv/CI scanner
YAML workflows -> CI/CD permission and injection sweep
Dockerfile -> build-time and secret leak sweep
PowerShell -> PowerShell injection/credential sweep
Terraform/Helm/K8s -> IaC/cloud permission sweep
Markdown agent instructions -> prompt-adjacent sidecar sweep
JSON/TOML/YAML config -> config-to-action sweep
```

See `UNSUPPORTED-SURFACE-ROUTER.md` and `COVERAGE-GOVERNANCE.md`.

## Phase 8 — Ledgers

Maintain:

```text
File inventory ledger — every repository file and coverage class
Sink census ledger — every dangerous operation and disposition
Route/file census — routes and middleware reaching file operations
API-response/file census — external/API fields reaching local file paths
Subprocess census — shell/argv/option-injection rows
Secrets/logging census — token/secret sources and logging/storage sinks
Network-fetch census — URL construction and fetch/download sites
Auth/session census — authentication, session, token, and identity boundaries
Deserialization/archive census — unsafe load/parse/extract rows
Crypto census — crypto primitives, key/IV/signature use
R-ledger — RubberDuck raw signals
H-ledger — graph hypotheses
M-ledger — rescue sweep candidates
P-ledger — prior-run candidates
F-ledger — final validated findings
D-ledger — validated defenses and bypass checks
Coverage-gap ledger — uncovered/partial surfaces and claim limits
Protocol-completion matrix — required phase/tool/finding actions
Claim ledger — every final claim and its evidence class
Negative-claim ledger — every "no X found" claim and search evidence
```

## Phase 9 — Validation, per-finding protocol matrix, and Tier-2 planning

Promote only with source-backed validation. For each final finding, complete the per-finding validation matrix in `PROTOCOL-COMPLETION.md` or record why a tool was unavailable/degraded.

For P0/P1 RCE, deserialization, auth bypass, cross-tenant, or code execution claims:

```text
Attempt Tier-2 unless the user forbids runtime checks.
If Tier-2 fails due environment, run the recovery sequence.
If still blocked, mark report: source-confirmed, runtime validation incomplete.
```

See `RUNTIME-VALIDATION-PLANNER.md`.

## Phase 10 — Defense verification and root-cause de-duplication

Before final de-duplication, create a D-ledger for important defenses using `DEFENSE-VERIFICATION.md`:

```text
defense
threat blocked
bypass cases checked
evidence
status
```

Validate defenses that justify false positives or weakened findings. A false-positive claim based on a defense is not complete until the defense itself is source-read and bypass-checked.

## Phase 10.5 — Root-cause de-duplication

Collapse counts, not evidence obligations.

Every root-cause family must preserve a variant table:

```text
variant
entry point
attacker position
sink/operation
evidence tier
status
shared fix
```

See `FALSE-POSITIVES-DEDUP.md`.

## Phase 11 — Claim firewall

Before final answer, produce or mentally apply the claim ledger. Block unsupported claims.

Allowed evidence classes:

```text
Tier-2 confirmed
source-confirmed
graph-confirmed
search-confirmed
manual review
unsupported
out of scope
```

A claim marked unsupported cannot appear in final report without a caveat.

See `CLAIM-FIREWALL.md`.

## Phase 12 — Protocol completion and report consistency verification

Run exhaustive, protocol, claim, and consistency checks:

```bash
python scripts/check_exhaustive_completion.py --root <report_bundle_dir>
python scripts/check_protocol_completion.py --root <report_bundle_dir>
python scripts/check_claim_ledger.py <report_bundle_dir>/ledgers/claim-ledger.md
python scripts/verify_report_consistency.py --root <report_bundle_dir>
```

If a checker cannot run, mark the report `tooling-blocked partial` or `draft`; do not manually certify it as complete.

If checks fail or emit unresolved warnings, fix the report or mark it draft/incomplete.

## Output and exit criteria

Use `REPORT-TEMPLATE.md` for the report and `PROTOCOL-COMPLETION.md` for the closeout matrix. The evidence-pack file set is enforced by `scripts/check_protocol_completion.py`.

Do not call the report complete unless the scope/commit, completed RubberDuck CI semantic full scan, full file inventory, sink census, census-row triage, coverage governance, Repo Intelligence Brief, compiled prompt, capability graph, rescue/specialist sweeps, unsupported-surface routing, negative claims, prior-run reconciliation, per-finding validation, Tier-2 status, defense checks, root-cause de-duplication, claim firewall, exhaustive-completion check, protocol-completion check, and report-consistency check are all complete or explicitly marked non-blocking. CI semantic full completion is never a non-blocking gap; if it fails repeatedly, abort the audit session.
