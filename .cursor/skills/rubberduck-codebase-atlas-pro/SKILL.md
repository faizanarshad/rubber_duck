---
name: rubberduck-codebase-atlas-pro
description: RubberDuck UC1, Codebase Atlas Pro: an evidence-governed skill for deep codebase understanding and the primary entrypoint for RubberDuck Skill Advisor requests. Use when the user says "I need help from the RubberDuck Advisor.", asks which RubberDuck skill to use, or wants repository architecture, onboarding, entry points, call/data flow, feature walkthroughs, or a RubberDuck-backed codebase overview. Uses mandatory RubberDuck codebase intelligence + semantic intelligence with semantic_mode="full" for Atlas work.
trigger: when the user says "I need help from the RubberDuck Advisor.", asks for the RubberDuck Skill Advisor, wants help choosing RubberDuck skills, wants to get to know a codebase, understand repository architecture, onboard to a repo, map code structure, explain how a feature works, identify entry points, trace call/data flow, or produce a RubberDuck-backed codebase overview
version: 2026-05-rubberduck-uc1-codebase-atlas-pro-codex-skill
when_to_use: Use when the user says "I need help from the RubberDuck Advisor.", asks for a RubberDuck skill recommendation, asks for a complete overview of a codebase, a repo map, architecture walkthrough, entry-point map, symbol/call-chain/data-flow explanation, feature walkthrough, or "get to know this codebase" style analysis.
argument-hint: [repo/path/commit/scope/feature/budget]
---

# RubberDuck UC1, Codebase Atlas Pro

RubberDuck UC1, Codebase Atlas Pro is a methodology-only skill for deep, evidence-governed codebase understanding.

It is not a generic "explain this repo" prompt. It is a **RubberDuck UC1 atlas compiler backed by RubberDuck tools**:

```text
RubberDuck codebase intelligence + semantic intelligence
  -> Repo Intelligence Brief
  -> repo-specific atlas prompt
  -> semantic symbol / entry-point / call-chain / data-flow mapping
  -> graph architecture and surprise discovery
  -> claim firewall
  -> unsupported-surface disclosure
  -> final atlas + evidence pack
```

## Operating mode

Default mode is **DEEP**.

```text
Budget: up to 200 RubberDuck/tool calls if needed.
Primary report requires BOTH:
- RubberDuck codebase intelligence, with full semantics where available.
- RubberDuck semantic intelligence / code model.
```

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user says `I need help from the RubberDuck Advisor.`, asks for the RubberDuck Skill Advisor, or asks which RubberDuck skill/order/mode to use, enter advisor mode:

```text
Read RUBBERDUCK-SKILL-ADVISOR.md.
Produce only the advisor recommendation and approval question.
Do not start Codebase Atlas, long multi-skill workflows, GitHub mirror/push, file mutation, commit, push, or PR creation until the user approves the recommended path.
```

If the user is unsure which RubberDuck skill to use, or this task should continue into audit, change impact, drift review, planning, build, or autonomous mode after the Atlas, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

If either RubberDuck codebase intelligence or semantic intelligence is unavailable, stale, or bound to the wrong commit:

```text
Stop and report the tooling blocker.
Do not silently produce a generic source-read overview.
Offer source-read fallback only if the user explicitly asks for it.
```

## Report framing

Every Atlas report must say:

```text
This is a Codebase Atlas, not a vulnerability report.
Security-sensitive flows may be mentioned as architecture boundaries, but findings are not security-validated unless explicitly labeled.
```

Title reports as:

```text
<Repo> — RubberDuck UC1 Codebase Atlas
```

Do not imply full runtime or deployment coverage when semantic coverage is partial. The Atlas envelope must state semantic surface covered, codebase-intelligence surface covered, unsupported surfaces, and whether runtime/deployment behavior was proven by tool evidence.

## Atlas modes

Select one mode in Phase 0:

```text
WHOLE_REPO_ATLAS
FEATURE_ATLAS
```

Use `FEATURE_ATLAS` when the user specifies a feature, file, endpoint, class, function, user journey, issue, module, or behavior. Read `FEATURE-ATLAS-MODE.md` when this mode triggers. Feature Atlas output must include:

```text
feature description
entry points
symbols involved
call chains
data flow
state/config involved
external integrations
tests related to the feature
unresolved edges
files to read first
falsification recipes
```

Use `WHOLE_REPO_ATLAS` when no feature is specified.

## What this skill optimizes for

This skill must produce a codebase overview where every important relationship is backed by evidence:

```text
symbols_overview for major symbols,
call_chain for main flows,
trace_variable for important data/request objects,
search_code for entry-point discovery and negative claims,
codebase-intelligence metrics for structural ranking,
read_source for source anchors when needed,
tool-health disclosure for degraded or unsupported claims.
```

For DEEP Atlases, generate an evidence pack unless the user explicitly asks for report-only output. Read `EVIDENCE-PACK.md` before packaging or finalizing a DEEP report.

```text
evidence/evidence-manifest.md
evidence/tool-calls.md
evidence/symbols-overview.md
evidence/entry-points.md
evidence/call-chains.md
evidence/data-flows.md
evidence/source-snippets.md
evidence/structural-metrics.md
evidence/unsupported-surfaces.md
evidence/claim-ledger.md
evidence/negative-claims.md
evidence/tool-health.md
evidence/falsification-recipes.md
evidence/cross-package-coupling.md
evidence/bus-factor-function.md
evidence/atlas-summary.json
```

`atlas-summary.json` is required in DEEP mode unless report-only output was explicitly requested. Read `ATLAS-SUMMARY-SCHEMA.md` before writing it.

The evidence pack must declare one evidence level:

```text
raw tool output
normalized evidence
report-derived evidence
```

If raw RubberDuck outputs are exported, store them under `evidence/raw-tool-output/`. If raw outputs are not exported, explicitly say the evidence pack is normalized/derived or report-derived, not a raw transcript. Do not let `REPORT.md` say evidence files or `atlas-summary.json` are absent when the bundle contains them. Normalize local paths to repo-relative paths wherever possible.

## Do not interrupt halfway

Once the target repo/path/commit is known, proceed through the protocol without asking midway for permission. Use defaults:

```text
budget = DEEP
tooling = RubberDuck codebase + semantic mandatory
output = one-screen brief + full atlas
unsupported surfaces = disclose and route
claim style = evidence-backed only
```

Ask a clarifying question only if the target repo/path/commit is missing or the tools cannot identify a repo.

## Mandatory files

When this skill is installed, read these support files as needed:

```text
RUBBERDUCK-WORKFLOW.md
REPO-INTELLIGENCE-BRIEF.md
ATLAS-PROMPT-COMPILER.md
SEMANTIC-MAP-WORKFLOW.md
SYMBOLS-AND-ENTRYPOINTS.md
CALL-CHAIN-AND-DATA-FLOW.md
ARCHITECTURAL-SURPRISES.md
GRAPH-ATLAS-SECTIONS.md
UNSUPPORTED-SURFACE-ROUTER.md
EVIDENCE-GOVERNANCE.md
CLAIM-FIREWALL.md
TOOL-HEALTH-SENTINEL.md
PROTOCOL-COMPLETION.md
REPORT-TEMPLATE.md
EVIDENCE-PACK.md
FEATURE-ATLAS-MODE.md
ATLAS-SUMMARY-SCHEMA.md
```

## Phases

```text
Phase 0  Scope and target pinning
Phase 1  RubberDuck codebase + semantic readiness
Phase 2  Repo Intelligence Brief
Phase 3  Repo-specific Atlas Prompt Compiler
Phase 4  Entry-point discovery
Phase 5  Symbol atlas
Phase 6  Call-chain atlas
Phase 7  Data-flow atlas
Phase 8  Graph architecture atlas
Phase 9  Architectural surprises
Phase 10 Unsupported surface router
Phase 10.5 Bus-factor function
Phase 11 Evidence / claim firewall
Phase 12 Reading plan
Phase 13 Tool health and protocol completion
Phase 14 Final report
```

## Phase 0 — Scope and target pinning

Record:

```text
repo/path
branch/commit when available
analysis scope
atlas mode: WHOLE_REPO_ATLAS / FEATURE_ATLAS
requested feature/module if any
budget: QUICK / STANDARD / DEEP
RubberDuck environment
```

If the user only says "get to know this codebase" and a repo is obvious from context, proceed.

If the user asks how a specific feature works, pin the feature target and run FEATURE_ATLAS without dropping the minimum repo context needed to explain that feature. Do not run the entire deep whole-repo Atlas first when a feature-only Atlas is requested.

## Phase 1 — RubberDuck readiness

Start with codebase intelligence and semantic intelligence.

Preferred modern path:

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="<branch>",
    semantic_mode="full",
)
```

Alternative legacy path when exposed by the RubberDuck MCP:

```python
list_repos()
load_repo(repo="<owner/repo or authorized mirror>")
```

Load source with high enough capacity:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id if available>",
    max_files=2000,
    file_pattern="<language pattern>",
)
```

Record:

```text
commit
instance_id
language/file counts
semantic coverage
codebase-intelligence coverage
tool health
unsupported surfaces
analysis_id map
```

## Phase 2 — Repo Intelligence Brief

Produce the brief before writing the final overview.

Required fields:

```text
repo class
primary languages/frameworks
major packages/directories
entry-point candidates
major symbols
data/storage/config
external integrations
build/test/deploy workflow
tool coverage
unsupported surfaces
hot files / graph centers
scanner/quality signal clusters
initial atlas prompt emphasis
```

## Phase 3 — Repo-specific atlas prompt

Compile a repo-specific prompt from the brief.

Example structure:

```text
This repo appears to be <repo class>.
Atlas mode is <WHOLE_REPO_ATLAS or FEATURE_ATLAS>.
Prioritize <entry points>, <main adapters>, <data flows>, <hot files>, <unsupported surfaces>.
If FEATURE_ATLAS, prioritize <feature/endpoint/class/function/user journey>.
Use symbols_overview for <files>.
Use call_chain for <entry points>.
Use trace_variable for <important request/data objects>.
Use graph/quality metrics to rank structural importance.
Do not claim relationships not backed by RubberDuck evidence.
```

The compiled prompt controls the rest of the analysis.

## Phase 4 — Entry-point discovery

Use search and metadata, not intuition.

Required evidence sources:

```text
search_code for main/CLI/server/router/handler symbols
package metadata / script entries when available
symbols_overview on candidate files
call_chain on confirmed entry points
read_source only as anchor, not as substitute for call graph
```

Classify entry points:

```text
CLI
HTTP/API
worker/background job
library public API
plugin/hook
test/dev tooling
build/deploy
```

## Phase 5 — Symbol atlas

Use `symbols_overview`.

Required output:

```text
curated major symbols table
full symbols_overview inventory in Appendix A or evidence/symbols-overview.md
major classes
major functions
line numbers
roles
which files were analyzed
which symbols are entry points vs helpers
which files were uninspected or unsupported
```

Do not claim "all major classes/functions" unless full symbols evidence exists or caveats explain scope. Keep the report's curated major-symbol table, but put complete tool-backed symbol details in the appendix or evidence pack.

## Phase 6 — Call-chain atlas

Use `query_action(action="call_chain")` on main entry points and central functions.

Required output:

```text
call-chain diagrams
caller/callee evidence
coherence score where available
cross-package coupling evidence table
longest execution path
which paths were not resolved
```

## Phase 7 — Data-flow atlas

Use `trace_variable` on key objects:

```text
request
response
args
config
app
client
session
state
model
payload
context
event
message
job
task
```

Required output:

```text
source -> transformations -> sinks/outputs
where data crosses subsystem boundaries
important state mutation
where variable tracing failed
```

## Phase 8 — Graph architecture atlas

Use codebase-intelligence metrics where available:

```text
hot files
god nodes
centrality / pagerank
articulation points
bridges
communities
longest paths
taint-flow clusters
duplicate/dead/untested clusters
quality hotspots
```

If the tool exposes only partial metrics, use what exists and state what is missing.

## Phase 8.5 — Cross-package coupling evidence

Every important coupling edge must be tagged:

```text
INTRA-PACKAGE
CROSS-PACKAGE
CROSS-LANGUAGE
EXTERNAL
UNKNOWN
```

Report a table with edge, source package/file, target package/file, evidence tool, evidence detail, and confidence. Manual synthesis is allowed only when labeled `manual inference` and supported by source/search evidence.

## Phase 9 — Architectural surprises

The final atlas must include `§A — Architectural Surprises`.

Find at least three evidence-backed surprises when possible.

Use rules from `ARCHITECTURAL-SURPRISES.md`.

If fewer than three rules fire, lower thresholds. If still fewer than three, state:

```text
This codebase contains no architectural surprises detectable by the selected rules and available evidence.
```

Do not invent surprises.

## Phase 10 — Unsupported surface router

Always list unsupported or weakly covered surfaces:

```text
shell scripts
YAML workflows
Dockerfiles
Terraform/IaC
PowerShell
Markdown instruction files
JSON/TOML configs
generated/vendor/binary files
external repos/actions
```

For each:

```text
count
privilege
coverage status
recommended review path
whether claims exclude it
```

## Phase 10.5 — Bus-factor function

Identify the single function or method no one should change casually. If exact centrality is unavailable, use best available evidence and label the score approximate.

Required fields:

```text
Function / method
File:line
Why this is the bus-factor function
Evidence
Callers
Callees
Fan-in / fan-out
Complexity / centrality / hot-file status
Data-flow or taint-flow involvement
What breaks if changed
Tests to run before changing
Safe modification plan
Confidence
```

If no defensible bus-factor function can be selected, report it as unavailable with the exact missing evidence.

## Phase 11 — Claim firewall

Every important claim must be evidence-classified:

```text
source-confirmed
symbols-confirmed
call-chain-confirmed
data-flow-confirmed
search-confirmed
codebase-metric-confirmed
manual inference
unsupported
out of scope
```

Negative claims require:

```text
search pattern
scope
match count
unsupported surfaces
caveat
```

Block unsupported claims.

Every major section must include or link to a falsification recipe:

```text
To refute this claim/flow, rerun:
- <exact tool call>
- <search pattern>
- <source file / function>
Expected contradiction:
- <what output would invalidate the claim>
```

Minimum sections requiring recipes: architectural surprises, entry points, call chains, data flows, architectural spine, cross-package coupling, bus-factor function, unsupported surfaces, and major negative claims. Centralized recipes may live in `evidence/falsification-recipes.md`.

## Phase 12 — Reading plan

Always include:

```text
30-minute reading plan
60-minute reading plan
180-minute reading plan
```

Reading plans must be based on entry points, central symbols, call chains, and architectural surprises.

## Phase 13 — Protocol completion

Before final answer, complete the protocol checklist:

```text
RubberDuck codebase intelligence complete
RubberDuck semantic intelligence complete
feature mode decision recorded
Repo Intelligence Brief written
Atlas prompt compiled
entry points discovered
symbols_overview run
full symbol appendix or scoped caveat included
call_chain run on main entry points
trace_variable run on important flows
cross-package evidence table included
architectural surprises evaluated
bus-factor function included or unavailable with reason
unsupported surfaces disclosed
evidence pack generated, or report-only request recorded
evidence/evidence-manifest.md included
evidence/atlas-summary.json included in DEEP mode
falsification recipes included
Atlas/not-security framing included
claim firewall applied
tool health disclosed
final report consistent
```

## Phase 14 — Final report

Use `REPORT-TEMPLATE.md`.

Required section order:

```text
§0 Atlas Envelope / One-screen onboarding brief
§A Architectural Surprises
§1 Major Symbols
§2 Entry Points
§3 Call-Chain Atlas
§4 Data-Flow Atlas
§5 Architectural Spine
§6 Articulation Points & Bridges
§7 Communities / Subsystems
§8 Cross-Package Coupling Map
§9 God Nodes / Hot Files
§10 Refactor Leverage
§10.5 Bus-Factor Function
§11 Dead / Duplicated / Untested / Unsupported
§12 Anti-Claims and Caveats
§13 30 / 60 / 180-Minute Reading Plan
§14 Tool Health & Coverage Gaps
§15 What RubberDuck Proved That Prose Would Guess
Appendix A Full Symbol Inventory or evidence/symbols-overview.md
Falsification Recipes or evidence/falsification-recipes.md
```

## Anti-hallucination rules

Never claim:

```text
"This is the architecture"
"all files are covered"
"no X exists"
"the main flow is..."
"this function is unused"
"this class is central"
```

unless the claim is backed by the relevant tool evidence.

Use wording like:

```text
"Within the loaded Python/TypeScript semantic surface..."
"RubberDuck call_chain confirms..."
"Search found no matches for pattern X in scope Y; unsupported surfaces remain..."
"Codebase metrics rank this file as central..."
```

## Budget policy

Default is DEEP.

```text
QUICK: up to 30 tool calls
STANDARD: up to 80 tool calls
DEEP: up to 200 tool calls
```

For DEEP, do not prematurely stop after a shallow overview. Use additional calls for:

```text
entry-point disambiguation
call chains
trace variables
cross-package edges
surprise rules
unsupported surface routing
tool-health checks
claim ledger
```

Drop order if budget is constrained:

```text
drop cosmetic tables first
never drop entry points
never drop symbols_overview
never drop main call_chain
never drop at least one trace_variable where applicable
never drop architectural surprises
never drop unsupported surfaces
never drop tool health
never drop claim firewall
```

## Deliverable philosophy

This is not a prose tour. It is a falsifiable atlas.

Every important claim should answer:

```text
what is claimed?
what tool proved it?
what file/line/symbol supports it?
what confidence applies?
what would falsify it?
```
