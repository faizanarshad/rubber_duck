# RubberDuck Workflow

Use RubberDuck as the source of truth for finding patterns and integration points.

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

Preferred setup:

```python
get_started(repo="<owner/repo or authorized mirror>")
detailed_repo_analysis(repo="<owner/repo or authorized mirror>", branch="<branch>", semantic_mode="full")
load_code(repo="<owner/repo or authorized mirror>", instance_id="<instance_id>", max_files=2000, file_pattern="*.py")
```

Repeat `load_code` for supported languages.

Use:

```python
search_code(pattern="<similar functionality>", analysis_id="all", repo="<owner/repo or authorized mirror>")
query_action(action="symbols_overview", analysis_id="<aid>")
query_action(action="call_chain", analysis_id="<aid>", method="<method>")
query_action(action="trace_variable", analysis_id="<aid>", var="<var>")
read_source(analysis_id="<aid>", function_name="<function>")
analyze_code(statement="<tests-first design or pattern comparison>", analysis_id="<aid>")
```

Record tool health, coverage, parser degradation, and unsupported surfaces.
