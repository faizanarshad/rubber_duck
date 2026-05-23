# Remediation Diffs

The skill recommends minimal changes, not implementation code, unless user asks.

## Remediation table

```markdown
| Drift | Preferred fix layer | Alternative fixes | Migration needed? | Tests | Risk |
|---|---|---|---|---|---|
```

## Fix layers

```text
DB_SCHEMA
CODE_TYPE
VALIDATOR
SERIALIZER
API_CONTRACT
CLIENT_TYPE
TEST_FIXTURE
DOCS
```

## Rules

Prefer changing the layer that is wrong relative to runtime truth. If truth is ambiguous, recommend a product/API decision first.
