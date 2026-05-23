# RubberDuck Tool Workflow for RubberDuck UC1, Codebase Atlas Pro

## Purpose

Use RubberDuck as the source of truth for codebase structure. The primary atlas must be based on RubberDuck codebase intelligence and semantic intelligence, not on general knowledge.

## Mandatory setup

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

Preferred modern flow:

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="<branch>",
    semantic_mode="full",
)
```

Poll until ready:

```python
get_started(repo="<owner/repo or authorized mirror>")
```

Load code:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

Repeat for supported languages:

```text
*.py
*.ts
*.tsx
*.js
```

Alternative legacy flow when exposed:

```python
list_repos()
load_repo(repo="<owner/repo or authorized mirror>")
```

## Tool requirements

Minimum for a valid primary atlas:

```text
RubberDuck codebase-intelligence run
RubberDuck semantic source loaded
symbols_overview on main files
call_chain on main entry points
tool-health / coverage record
```

Preferred deep atlas:

```text
detailed_repo_analysis(semantic_mode="full")
assess(repo_quality or repo_detailed) if available
load_code for all supported source files
symbols_overview on hot files and entry-point files
search_code for entry point discovery
query_action(call_chain) on major flows
query_action(trace_variable) on key data objects
query_action(control_guards / def_sites) when clarifying logic
scan_bug_signals only for structural/logic/quality hints, not security scoring
logic_analysis for risk/complexity/anomaly only when useful
read_source for source anchors
```

## Tool degradation behavior

If a tool fails:

```text
record exact failure
record attempted query
state whether it blocks or only weakens the atlas
use available fallback only if it is clearly labeled
```

If semantic tools are unavailable:

```text
Stop primary atlas.
Offer source-read fallback only with explicit user approval.
```

If codebase intelligence is unavailable:

```text
Stop DEEP atlas.
Optionally produce Semantic Atlas only if user approves and label missing structural ranking.
```

## Analysis ID integrity

Build a table:

```text
analysis_id -> file_path -> line_count -> language -> loaded/current repo confirmed
```

Never trust ambiguous stems like:

```text
index
server
app
route
main
config
```

until mapped.

## Entry point discovery

Search patterns should adapt to language and repo class.

Generic patterns:

```text
def main|if __name__|console_scripts|entry_points|argparse|click|typer
app =|FastAPI|Flask|Django|Express|router|Route|POST|GET
function main|class .*Application|serve|run|start|build
worker|queue|consumer|handler|lambda_handler
```

Use package metadata and config when available:

```text
package.json scripts/bin/exports
pyproject.toml scripts/entry-points
setup.py console_scripts
Cargo.toml bin
go.mod cmd/
```

## Required evidence table

For every major section, record at least one of:

```text
tool
query/action
analysis_id
file/path
line/symbol
confidence/coherence if provided
```
