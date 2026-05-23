# Atlas Prompt Compiler

After the Repo Intelligence Brief, compile a repo-specific execution prompt.

## Compiler input

```text
repo class
language/frameworks
atlas mode: WHOLE_REPO_ATLAS / FEATURE_ATLAS
feature target when present
entry candidates
central files
hot symbols
unsupported surfaces
tool health
budget
```

## Compiler output

```text
You are producing a RubberDuck UC1 Codebase Atlas for <repo class>.
Mode: <WHOLE_REPO_ATLAS or FEATURE_ATLAS>.

Prioritize:
- <entry point families>
- <main subsystems>
- <central files/symbols>
- <data/request objects>
- <unsupported surfaces>
- <architectural surprise rules likely to fire>
- <feature target and behavior> when mode is FEATURE_ATLAS

Required tool calls:
- symbols_overview on <files>
- call_chain on <entry points>
- trace_variable on <objects>
- search_code for <negative claims / entry discovery>
- read_source for <source anchors>

Do not claim:
- unsupported surfaces are covered,
- relationships not backed by symbols/call/data evidence,
- negative claims without search evidence.

Required output:
- Codebase Atlas, not a security audit framing,
- one-screen brief,
- architectural surprises,
- major symbols,
- full symbol inventory appendix or evidence/symbols-overview.md,
- entry points,
- call/data-flow atlas,
- cross-package coupling evidence table,
- graph architecture,
- bus-factor function,
- unsupported surfaces,
- reading plan,
- evidence ledger,
- falsification recipes,
- evidence pack with evidence/evidence-manifest.md,
- required atlas-summary.json in DEEP mode.
```

## Feature Atlas additions

When mode is FEATURE_ATLAS, the compiled prompt must require:

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

## Universal baseline

Repo-specific emphasis changes priority, not the universal baseline. Always include:

```text
entry points
major symbols
call chains
data flow
architectural surprises
bus-factor function
cross-package coupling evidence
unsupported surfaces
tool health
claim firewall
falsification recipes
evidence pack
reading plan
```
