# Protocol Completion Matrix

Protocol completion is a table, not a feeling.

Maintain the matrix during the audit. Do not reconstruct it from memory at the end.

## Required phase matrix

For each phase and closeout row, use this table shape:

```text
| Row | Required actions | Tools/commands run | Result | Status | Evidence pointer | Blocking? | Next incomplete action |
|---|---|---|---|---|---|---|---|
| scope and commit pinned | ... | ... | ... | complete | SCOPE.md | no | none |
```

`Evidence pointer` must be a real file path in the report bundle, such as `SCOPE.md`, `TRACE.md`, `REPORT.md`, `ledgers/f-ledger.md`, `evidence/tool-health.md`, or `logs/protocol_check.txt`. Placeholder evidence does not count.

## Required Closeout Rows

```text
scope and commit pinned
RubberDuck CI semantic full completed with `detailed_repo_analysis(..., semantic_mode="full")`
semantic source loaded or post-CI unsupported/degraded status documented
full file inventory and deterministic sink census completed
all privileged census rows triaged or blocked with evidence
route/file and API-response/file matrices completed
coverage governance written and open gaps classified
impossible zero-file/zero-node tool states ruled out or documented
Repo Intelligence Brief written
repo-specific audit prompt compiled
capability graph written
universal baseline sweeps run
selected specialist playbooks run
unsupported and uncovered surfaces routed
critical-surface coverage plan executed or gap recorded
negative claims backed by search/scope evidence
prior-run candidates reconciled
High/Critical prior-reviewed downgrades have dedicated downgrade notes or preserve prior severity
per-finding protocol matrix completed or exceptions documented
P0/P1 Tier-2 attempted or blocker documented
important defenses validated and bypass-checked
root-cause variants preserved
final claims pass claim firewall
exhaustive completion checker passed or report marked incomplete
protocol-completion checker passed or report marked draft
consistency checker passed with no warnings/errors or report marked draft
```

## Per-finding validation tool matrix

For each promoted finding, attempt or justify:

```text
read_source
query_action(control_guards)
query_action(trace_variable) where variable path exists
query_action(def_sites) where variable origins matter
query_action(call_chain) for reachability
logic_analysis(infer_intent) where guard/policy intent matters
logic_analysis(simulate_paths) for exploit path
explain_finding where RubberDuck finding ID exists
get_evidence_pack where tool supports it
Tier-2 validation plan for P0/P1 or high-risk classes
```

If a post-CI tool is unavailable, degraded, unsupported for the language, or impossible due repo eviction, record the reason and fallback. If CI semantic full itself is unavailable, abort instead of recording a fallback.

If the user asks whether the protocol is complete, first re-open `ledgers/protocol-completion.md`, `evidence/tool-health.md`, `evidence/open_coverage_gaps.md`, and the checker outputs. Do not answer from memory.

## Completion status

Allowed statuses:

```text
complete
complete-with-accepted-gaps
post-CI source-confirmed partial
runtime-validation incomplete
post-CI tooling-blocked partial
draft
```

Do not use "complete" if:

```text
file inventory or sink census is missing
privileged census rows remain untriaged
route/file or API-response/file matrix rows are open
high-risk coverage gaps remain open
P0/P1 Tier-2 failed without accepted blocker
prior-run candidates are missing
required validation tools were skipped without reason
consistency checker warnings are unresolved
protocol-completion checker warnings are unresolved
CI semantic full is missing or tooling returned impossible metrics
```

## Fix completeness matrix

Every final finding should include:

```text
minimal fix
defense-in-depth fix
positive regression test
negative regression test
runtime/monitoring signal
rollout plan
rollback plan
verification command/tool call
```

If any are not applicable, say why.
