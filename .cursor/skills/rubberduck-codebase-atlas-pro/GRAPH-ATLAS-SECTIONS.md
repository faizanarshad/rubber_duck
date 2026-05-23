# Graph Atlas Sections

Use codebase-intelligence metrics when available. If a metric is unavailable, mark it unavailable instead of guessing.

## Architectural spine

Rank the files/functions that explain the core behavior.

Inputs:

```text
entry point calls
centrality/pagerank
hot files
call-chain fan-in/fan-out
taint/data-flow clusters
```

## Articulation points and bridges

Output:

```markdown
| Node/edge | Type | Connects | Risk if misunderstood | Evidence |
|---|---|---|---|---|
```

## Bus-factor function

Identify the function no one should change alone.

Approximate score when data exists:

```text
score = centrality_or_pagerank * log(1 + complexity) * (1 + flow_touch_count)
```

If exact metrics are unavailable, use ranked evidence from:

```text
call-chain centrality
hot file status
fan-in/fan-out
taint/data-flow touch count
complexity/tool quality signals
```

Output:

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

If exact centrality/pagerank is unavailable, use best available evidence and label the score approximate:

```text
call_chain centrality
hot file status
fan-in/fan-out
complexity/quality metrics
data-flow touch count
source reads
```

The report section `§10.5 Bus-Factor Function` and `evidence/bus-factor-function.md` are mandatory in DEEP mode. If exact graph centrality is unavailable, the score label must be one of:

```text
approximate
manual synthesis
RubberDuck metric-backed
```

If no defensible candidate exists, write:

```text
Bus-Factor Function unavailable: <missing centrality/call/data evidence>
```

## Cross-package coupling evidence

For `§8 Cross-Package Coupling Map`, include:

```markdown
| Edge | Source package/file | Target package/file | Tag | Evidence tool | Evidence detail | Confidence |
|---|---|---|---|---|---|---|
```

Tags:

```text
INTRA-PACKAGE
CROSS-PACKAGE
CROSS-LANGUAGE
EXTERNAL
UNKNOWN
```

Every row must name its evidence basis:

```text
RubberDuck call-chain
RubberDuck search
source-read
package metadata
manual synthesis with caveat
```

Manual synthesis is allowed only when labeled `manual synthesis with caveat` and supported by source/search evidence. Mirror the table at `evidence/cross-package-coupling.md` in DEEP mode.

## Bus-factor change analysis

For the selected bus-factor function, include:

```text
what it does
why it is sensitive
what breaks if changed
callers/callees
tests to run
safe modification plan
```

## Longest execution path

Use call_chain and codebase metrics. If tool cannot compute longest path, derive only from confirmed call chains and label approximate.

## Communities

Map graph communities/subsystems:

```markdown
| Community | Key files | Shared purpose | Entry points | Cross-community edges |
|---|---|---|---|---|
```

## God nodes / hot files

List high-centrality, high-fanout, or high-complexity nodes. Explain whether each is:

```text
true orchestrator
accidental god object
framework hub
generated/vendor noise
```

## Refactor leverage

Suggest only evidence-backed refactor opportunities:

```text
high centrality + high complexity
duplicate logic
bridge node with too many responsibilities
public symbol with no callers
private helper with high centrality
```
