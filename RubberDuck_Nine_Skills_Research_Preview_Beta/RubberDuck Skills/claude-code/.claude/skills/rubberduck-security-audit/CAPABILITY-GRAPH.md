# Capability Graph Playbook

Use this before final sink/CWE triage.

## Mental model

```text
attacker language A -> adapter X -> representation B -> adapter Y -> privilege domain Z
```

## Attacker languages

Examples:

```text
HTTP/JSON bodies
headers / cookies / tokens
CLI args
env vars
YAML/TOML/JSON config
database rows
session state
artifact IDs
file paths
archive contents
URLs
templates
schemas
metadata
plugin names
callback names
import paths
serialized bytes
```

AI/agent additions:

```text
user prompts
tool outputs
retrieved documents
memory rows
scheduled task prompts
compaction summaries
vector-store context
model-selected tool args
conversation history
prompt-adjacent markdown/config files
```

ML/model-serving additions:

```text
model artifacts
registry payloads
pickle/cloudpickle/torch/joblib files
model IDs
trust_remote_code flags
setup scripts
custom objects
pipeline classes
file/image inputs
inter-service responses
```

## Privilege domains

```text
deserialization/code execution
dynamic import
subprocess/shell/argv tool execution
filesystem read/write/delete
archive extraction
network fetch
cloud APIs under ambient credentials
database writes
session persistence
tool execution
scheduler/autonomous execution
credential storage
prompt/system-context influence
```

## Adapters

```text
route handlers
serde registries
content-type dispatch
schema validators
config loaders
model loaders
framework loaders
import resolvers
tool registries
archive extractors
state merge layers
prompt builders
runner clients
task/result stores
tenant selectors
command builders
CI workflow steps
```

## Ranked hypothesis format

```text
H-ID:
Graph edge:
Attacker language:
Adapter:
Privilege domain:
Broken assumption:
Worst case:
Evidence needed:
Validation plan:
Current confidence:
```

## Prior-run regression ledger

For comparisons/re-audits, create a P-ledger before final report.

Extract from every prior report/evidence pack:

```text
final findings
root-cause families
exploit variants
Tier-2 validations
ruled-out hypotheses
weakened hypotheses
open candidates
tooling limitations
```

Each prior candidate gets:

```text
Prior ID:
Prior report:
Prior status:
Normalized root cause:
Current status: promoted / merged / ruled out / weakened / open / invalidated
Current evidence:
If merged: target root-cause family:
If ruled out/weakened: source or validation evidence:
If open: next validation step:
If prior Tier-2 existed: reproduced / reused / invalidated / runtime-validation incomplete:
```

No prior-run candidate may disappear silently.
