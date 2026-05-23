# Semantic Map Workflow

## Atlas mode

Run one of two modes:

```text
WHOLE_REPO_ATLAS
FEATURE_ATLAS
```

Use FEATURE_ATLAS when the user specifies a feature, file, endpoint, class, function, user journey, issue, module, or behavior. Feature mode still requires RubberDuck codebase intelligence and semantic intelligence, but the semantic map centers on the requested behavior. Read `FEATURE-ATLAS-MODE.md` for the full contract.

FEATURE_ATLAS required evidence:

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

## Symbol mapping

Run `symbols_overview` on:

```text
entry-point files
hot files
central classes/modules
files selected by codebase-intelligence metrics
```

For each symbol:

```text
name
kind
file:line
role
subsystem
entry/helper/internal/exported
evidence tool
```

## Entry point mapping

Confirm entry points with at least two evidence sources when possible:

```text
search_code match
package metadata/script config
symbols_overview
call_chain
source read
```

## Call-chain mapping

Run `call_chain` on:

```text
main entry points
core orchestration functions
hot/central methods
feature-specific entry if user asked about a feature
```

Record:

```text
caller -> callee
line numbers
cross-package edges and tags
coherence score if available
unresolved calls
```

## Data-flow mapping

Run `trace_variable` on important data objects:

```text
args
request
response
config
app
state
session
payload
context
job
task
model
client
```

Record:

```text
source
transformation
mutation
consumer
output/sink
scope boundary
unresolved hops
```

## Falsification recipe

Every major section and flow must include or link to:

```text
To refute this flow, rerun:
- <exact RubberDuck query>
- <search pattern>
- <source file / function>
Expected contradiction:
- <what output would invalidate the claim>
```

Minimum recipe coverage:

```text
architectural surprises
entry points
call chains
data flows
architectural spine
cross-package coupling
bus-factor function
unsupported surfaces
major negative claims
```

Centralize recipes in `evidence/falsification-recipes.md` when inline recipes would make the report noisy.
