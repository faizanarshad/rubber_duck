---
name: rubberduck-schema-code-api-drift-pro
description: Evidence-governed RubberDuck skill for finding drift between database schema, code types/models, validators, runtime handlers, and API contracts. Uses RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full", inventories representation layers, fuses concepts with confidence, builds a drift matrix, predicts runtime failures, checks round-trip paths, proposes remediation diffs, and emits an auditable evidence pack.
trigger: when the user asks for schema drift, API contract drift, DB/type/API consistency, model-field mismatch, nullability/default/validation drift, broken generated clients, migration risk, schema-code-api comparison, or data model consistency review
version: 2026-05-22-schema-code-api-drift-pro
---

# RubberDuck Schema-Code-API Drift Pro

This skill finds where a repository's data representations tell different stories:

```text
database schema
  ↔ code model / type
  ↔ validator / serializer
  ↔ route / handler
  ↔ API contract
  ↔ client type
```

It is not a generic schema checklist. It is an evidence-governed triangulation workflow.

## Core promise

```text
Your schema says one thing.
Your code says another.
Your API ships a third.
RubberDuck shows exactly where.
```

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure which RubberDuck skill to use, or drift findings should continue into change impact, remediation planning, build, or autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

## Hard requirements

1. Use RubberDuck codebase intelligence and semantic intelligence for the primary report.
2. Use `semantic_mode="full"` when calling codebase intelligence.
3. Do not claim complete drift coverage unless all relevant representation layers were inventoried or explicitly ruled out.
4. No drift row may be reported unless at least two layers are cited.
5. No runtime-failure prediction may be reported unless it points to a specific drift cell.
6. No "no drift found" claim may appear unless relevant layers, dimensions, and unsupported surfaces are documented.
7. Concept fusion must have confidence: HIGH / MEDIUM / LOW / REJECTED.
8. LOW confidence concept fusions are candidates, not final drift findings.
9. If layer inventory is partial, mark the report targeted or incomplete.
10. Do not interrupt halfway after setup/discovery unless the target or RubberDuck tooling blocks the primary report.

## Modes

Choose exactly one mode and state it in the report:

```text
ANCHORED_CONCEPT
  User supplies a concept/field/entity, e.g. "user.email".

SCOPE_DRIFT
  User supplies a package/path/service/scope to analyze.

UNCONSTRAINED
  Enumerate all concepts with at least two representations.
```

UNCONSTRAINED must not claim exhaustive coverage unless layer inventory is complete.

## Representation layers

Inventory all relevant layers:

```text
DB_SCHEMA
CODE_TYPE
VALIDATOR
RUNTIME_HANDLER
SERIALIZER
API_CONTRACT
CLIENT_TYPE
TEST_FIXTURE
DOCS_OR_MIGRATION_NOTE
```

Examples:

```text
SQL migrations
Prisma / Drizzle / TypeORM
SQLAlchemy / Django models
Mongoose schemas
Pydantic / dataclasses
TypeScript interfaces/types/classes
Zod / Yup validators
OpenAPI / Swagger
GraphQL
protobuf
tRPC routers
REST handlers
serializers/deserializers
generated client types
```

## Drift dimensions

Required dimensions:

```text
D1 name / alias drift
D2 type drift
D3 nullability drift
D4 format / length / precision drift
D5 default value drift
D6 validation constraint drift
D7 cardinality / relation drift
D8 encoding / serialization drift
```

Optional dimensions when evidence exists:

```text
D9 authorization / visibility drift
D10 lifecycle / state-machine drift
D11 versioning / backward-compatibility drift
D12 test-fixture / generated-client drift
```

## Workflow

```text
Phase 0    Scope, repo, commit, and mode
Phase 1    RubberDuck full setup
Phase 2    Layer inventory
Phase 3    Concept extraction
Phase 4    Concept fusion
Phase 5    Drift matrix
Phase 6    Runtime-failure prediction
Phase 7    Round-trip proof
Phase 8    Remediation diffs
Phase 9    Negative claims and unsupported surfaces
Phase 10   Falsification recipes
Phase 11   Evidence pack and protocol completion
```

## First-screen hook

Every report starts with:

```text
§0 Triangle Stat
```

Example shape:

```text
Mapped N concepts across DB / code / API / validators.
M concepts have drift.
K predict runtime failures.
S indicate silent data-loss or unreachable-state risks.
```

If no drift is found, the hook must say which layers and dimensions were actually checked.

## Required output

```text
REPORT.md
evidence/layer-inventory.md
evidence/concept-map.md
evidence/concept-fusion-ledger.md
evidence/drift-matrix.csv
evidence/runtime-failure-predictions.md
evidence/round-trip-proof.md
evidence/remediation-diffs.md
evidence/coverage-gaps.md
evidence/negative-claims.md
evidence/falsification-recipes.md
evidence/tool-health.md
evidence/schema-drift-summary.json
evidence/protocol-completion.md
```

## Verdict language

Use these categories:

```text
NO_DRIFT_CONFIRMED
DRIFT_NO_RUNTIME_FAILURE
PREDICTED_RUNTIME_FAILURE
SILENT_DATA_LOSS_RISK
UNREACHABLE_STATE_RISK
CONTRACT_BREAK_RISK
INCOMPLETE_LAYER_COVERAGE
LOW_CONFIDENCE_CANDIDATE
```

Do not use absolute language like "schema is clean" unless all relevant layers and dimensions are covered.

## Anti-hallucination rule

Base findings on RubberDuck, source reads, schema files, contracts, validators, and traceable code evidence. Do not fuse concepts by similar names alone. Do not invent schemas, contracts, or API fields from framework knowledge.
