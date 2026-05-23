# RubberDuck Workflow

## Required setup

Use both codebase and semantic intelligence when available:

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before repo-backed setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="<branch>",
    semantic_mode="full",
)
```

Load relevant before/after files:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

or load exact files / scratch code when comparing patches:

```python
load_code(file_path="<before_path>", analysis_id="before")
load_code(file_path="<after_path>", analysis_id="after")
```

If RubberDuck supports raw scratch loading, use it for direct patch comparisons. If not, use source reads and label graph evidence unavailable for scratch snippets.

## Required semantic calls

Use as applicable:

```python
query_action(action="symbols_overview", analysis_id="<before_aid>")
query_action(action="symbols_overview", analysis_id="<after_aid>")
query_action(action="call_chain", analysis_id="<aid>", method="<method>", direction="callers")
query_action(action="call_chain", analysis_id="<aid>", method="<method>", direction="callees")
query_action(action="trace_variable", analysis_id="<aid>", var="<var>")
query_action(action="control_guards", analysis_id="<aid>", line=<line>)
query_action(action="def_sites", analysis_id="<aid>", var="<var>")
read_source(analysis_id="<aid>", function_name="<function>")
search_code(pattern="<imports/classes/helpers>", analysis_id="all", repo="<owner/repo or authorized mirror>")
```

Use codebase metrics for reachability and importance, but do not use centrality as equivalence proof unless the mode is `ai-patch-verify`.

## Hard gate

If both semantic and source evidence are unavailable for either side, stop and report the blocker. Do not produce a Mirror verdict from prose alone.

## Tool health

Record:

```text
commit
instance_id
loaded analyses
before/after analysis IDs
parser degradation
unresolved calls
dynamic dispatch
unsupported language
source-only fallback
runtime/test execution availability
```
