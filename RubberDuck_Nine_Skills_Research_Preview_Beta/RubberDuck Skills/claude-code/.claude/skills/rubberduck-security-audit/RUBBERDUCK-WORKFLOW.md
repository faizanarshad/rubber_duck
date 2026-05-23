# RubberDuck Workflow for RubberDuck Security Audit

This file defines tool choreography. `SKILL.md` defines audit policy.

## Server selection

- Use production RubberDuck servers unless explicitly asked for dev.
- Never mix prod and dev in one scan.
- Record server set in the report.

## Start sequence

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="main",
    semantic_mode="full",
)
```

CI semantic full completion gate:

```text
Repeat `detailed_repo_analysis(..., semantic_mode="full")` and wait/poll until the complete CI semantic full report is returned. Do not proceed to repo intelligence, prompt compilation, playbooks, validation, fallback, or reporting while the result is only queued, indexing, pending, degraded, unavailable, or failed. If repeated attempts fail, abort the audit session and report the blocker.
```

Re-poll semantic readiness:

```python
get_started(repo="<owner/repo or authorized mirror>")
```

Record:

```text
instance_id
commit
branch
phase1/phase2 readiness
GitHub App status
security grade/score
raw counts
dashboard URL
tool health
```

## Loading

Always pass `instance_id` and `max_files`:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

Repeat per supported extension and high-risk subpath.

## Analysis-ID map

After load, build:

```text
analysis_id -> file_path -> extension -> line_count -> current repo confirmed
```

Duplicate stems are expected. Never use an ambiguous ID for final claims.

## Detection stack

Repo level:

```python
assess(mode="repo_detailed", repo="owner/repo")
```

Per file:

```python
assess(
    mode="security",
    repo="owner/repo",
    analysis_id="<aid>",
    include_ci=true,
)
```

Bug families:

```python
scan_bug_signals(
    analysis_id="<aid>",
    families="all",
    min_suspicion="low",
)
```

Query and source:

```python
query_action(action="symbols_overview", analysis_id="<aid>")
query_action(action="trace_variable", analysis_id="<aid>", var="<var>")
query_action(action="call_chain", analysis_id="<aid>", method="<method>")
query_action(action="control_guards", analysis_id="<aid>", line=<line>)
query_action(action="def_sites", analysis_id="<aid>", var="<var>")
read_source(analysis_id="<aid>", function_name="<function>")
read_source(analysis_id="<aid>", start_line=<n>, end_line=<m>)
```

Logic:

```python
logic_analysis(action="risk_score", analysis_id="<aid>", target="<function>")
logic_analysis(action="detect_anomalies", analysis_id="<aid>", target="<function>", objective="<objective>")
logic_analysis(action="infer_intent", analysis_id="<aid>", target="<function>", objective="<objective>")
logic_analysis(action="simulate_paths", analysis_id="<aid>", target="<function>", scenario="<scenario>")
```

## search_code rule

`search_code` is valid for graph construction, adapter discovery, sibling discovery, rescue sweeps, negative claims, and validation.

A search hit is not a finding. A zero-hit search is only a negative claim for the searched scope and pattern.

## Degraded-tool interpretation

If CI fusion fails on local semantic repo:

```text
semantic-only clean != no finding
```

If parser confidence is low:

```text
source-confirmed but graph-degraded
```

If output truncates:

```text
rerun with narrower pattern or persisted output
```

If tool auto-corrects a target:

```text
verify with read_source
```

## Tooling issue format

For every issue:

```text
tool
query
exact failure
blocks or slows
workaround
impact on final claims
```
