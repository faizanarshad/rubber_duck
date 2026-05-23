# RubberDuck Workflow for Change Impact Pro

## Start sequence

Use the strongest available codebase-intelligence path:

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="main",
    semantic_mode="full",
)
```

Poll semantic readiness:

```python
get_started(repo="<owner/repo or authorized mirror>")
```

Then load relevant source:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

Repeat per relevant extension.

## Required tool categories

Use whichever RubberDuck action names are available in the environment:

```text
plan_change
search_code
analyze_code
symbols_overview
query_action(call_chain)
query_action(trace_variable)
query_action(shared_variables) if available
read_source
get_evidence_pack if available
assess(mode="impact") if available
scan_bug_signals where relevant
logic_analysis where relevant
```

## Do not trust a single channel

Impact claims must reconcile:

```text
plan_change / assess(mode=impact)
call_chain callers/callees
search_code usage scan
read_source of top callers
symbols_overview
trace_variable / shared_variables
tests/mocks search
public API/export proof
```

If one tool says "LOW/no cross-file references" but search/source shows real callers, use the reconciled evidence and explain the disagreement.

## Tool health fields to record

Every run must record:

```text
index_status
commit
instance_id
phase1/phase2 readiness
semantic_loaded
load coverage
cache_stats if present
pending_eviction_notices if present
analysis_id map
tool output spillovers
parser/tool degradation
CI fusion availability
```

## Spillover handling

If a tool output spills to a file:

```text
parse it with Python/jq/read tool result file
extract coverage
extract analysis IDs
extract target file/function
write evidence/tool-output-spillovers.md or evidence/tool-calls.md note
```

Never ignore spillover files.

## Local path scrub

Final reports and share packages must not contain local absolute paths, uploaded-file markers, platform metadata, sandbox-link markers, or hidden OS metadata.

Use repo-relative paths. The verifier script checks for common absolute-path and artifact-marker patterns.
