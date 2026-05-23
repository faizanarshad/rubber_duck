# Schema-Code-API Drift Workflow

## Phase 0 — Scope and mode

Declare:

```text
mode: ANCHORED_CONCEPT / SCOPE_DRIFT / UNCONSTRAINED
target concept or scope:
repo / commit:
coverage goal:
```

## Phase 1 — Layer inventory

Inventory DB/schema, code types, validators, runtime handlers, API contracts, serializers, clients, tests, and docs/migration notes.

Do not proceed to "no drift" claims until layer inventory is complete or gaps are disclosed.

## Phase 2 — Concept extraction

Extract candidate concepts from each layer:

```text
entity names
field names
route payloads
model attributes
validator keys
OpenAPI/GraphQL/proto fields
serializer/deserializer fields
client/generated types
test fixtures
```

Normalize:

```text
case
snake/camel/kebab
pluralization
common aliases
entity prefixes/suffixes
```

## Phase 3 — Concept fusion

Fuse concepts only with evidence. Assign confidence:

```text
HIGH:
  same normalized name + code path/route/model linkage + compatible type context

MEDIUM:
  same normalized name + co-occurrence in handler/repository/serializer path

LOW:
  lexical similarity only or weak co-occurrence

REJECTED:
  similar name but different entity, route, or semantic role
```

LOW-confidence fusions are candidates, not drift findings.

## Phase 4 — Drift matrix

For each HIGH/MEDIUM concept with at least two cited layers, evaluate drift dimensions D1-D12.

Each cell must say:

```text
MATCH
DRIFT
UNKNOWN
NOT_APPLICABLE
```

## Phase 5 — Runtime-failure prediction

For each drift row, determine:

```text
Will this break reads?
Will this break writes?
Will this violate API contract?
Will this silently drop data?
Will this create unreachable states?
Will this break generated clients?
```

No prediction without a specific drift cell.

## Phase 6 — Round-trip proof

Trace at least one path when possible:

```text
write path:
  API input -> validator -> code model -> DB write

read path:
  DB row -> code model -> serializer -> API response -> client type
```

If only one path is available, label proof partial.

## Phase 7 — Remediation diffs

Suggest minimal remediation:

```text
change DB schema
change code type
change validator
change serializer
change API contract
change client type
add test
add migration
```

Do not generate implementation code unless user asks. Produce plan/diff sketch.

## Phase 8 — Final gates

Before finalizing, verify:

```text
each drift row has >=2 layers
each runtime prediction points to a drift cell
all no-drift claims have layer/dimension coverage
unsupported surfaces are listed
falsification recipes exist
validators pass
```
