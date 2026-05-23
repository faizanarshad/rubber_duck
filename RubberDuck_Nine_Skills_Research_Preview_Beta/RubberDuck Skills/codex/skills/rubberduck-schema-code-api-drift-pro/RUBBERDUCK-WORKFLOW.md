# RubberDuck Workflow

## Setup

Run codebase intelligence first:

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="<branch>",
    semantic_mode="full",
)
```

Poll readiness:

```python
get_started(repo="<owner/repo or authorized mirror>")
```

Load semantic source:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

Repeat for relevant supported extensions:

```text
*.py
*.ts
*.tsx
*.js
*.sql
*.graphql
*.proto
```

If a file type cannot be loaded semantically, route it through source/search evidence and mark the layer as source-only.

## Discovery calls

Use:

```python
search_code(pattern="<schema/type/contract patterns>", analysis_id="all", repo="<owner/repo or authorized mirror>")
query_action(action="symbols_overview", analysis_id="<aid>")
query_action(action="call_chain", analysis_id="<aid>", method="<handler_or_serializer>")
query_action(action="trace_variable", analysis_id="<aid>", var="<field_or_payload>")
read_source(analysis_id="<aid>", function_name="<function>")
```

Use `analyze_code` only as a reasoning aide. Treat it as a lead until source/query evidence confirms.

## Tool-health rules

Record:

```text
commit
instance_id
codebase intelligence status
semantic intelligence status
file types loaded
unsupported file types
parser degradation
truncated outputs
analysis ID collisions
stale/wrong repo signs
```

If RubberDuck cannot load a layer, mark that layer as:

```text
source-only
grep-only
unsupported
out of scope
```

Do not hide gaps.
