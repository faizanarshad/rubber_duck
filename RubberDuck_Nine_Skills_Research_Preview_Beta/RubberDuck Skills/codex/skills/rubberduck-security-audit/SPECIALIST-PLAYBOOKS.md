# Specialist Playbooks

Select playbooks from the Repo Intelligence Brief. Always run the universal baseline too.

## ML / model-serving

Prioritize:

```text
model artifact deserialization
torch/joblib/cloudpickle/pickle
trust_remote_code
from_pretrained / pipeline
serde/content-type dispatch
inter-service runner/worker protocols
archive extraction
URL/file ingestion
model registry trust
setup scripts
```

Required outputs:

```text
ML artifact trust matrix
loader table
content-type dispatch table
inter-service protocol table
version-aware torch/load analysis
```

## AI agent / coding agent

Prioritize:

```text
prompt/tool boundary
memory/schedule/summary sidecars
OAuth/cloud tool execution
prompt-adjacent files
durable state
tool result injection
autonomous tasks
model-mediated persistence
```

Required outputs:

```text
sidecar control table
tool capability table
prompt-boundary table
durable-state table
```

## CI/CD action or workflow repo

Prioritize:

```text
workflow YAML
shell scripts
token permissions
pull_request vs pull_request_target
checkout/ref behavior
artifacts/cache
external actions
env var injection
```

Required outputs:

```text
workflow permission table
untrusted PR input table
shell/YAML routing table
```

## CLI/build tool

Prioritize:

```text
argv option injection
repo-file input
config-to-action
plugin scripts
package install
subprocess
archive extraction
credential writes
```

## Web API / SaaS

Prioritize:

```text
auth/authz
tenant isolation
object-level auth
SSRF
SQL/template injection
opaque-ID control planes
session/cookie handling
rate limits
```

## Parser / processor

Prioritize:

```text
file parsing
archive traversal/DoS
decompression
ReDoS
parser CVEs
memory/CPU exhaustion
deserialization
```

## Cloud/client SDK

Prioritize:

```text
credential storage
endpoint control
TLS/mTLS
SSRF vs operator endpoint
token logging
config persistence
subprocess/tool wrappers
```
