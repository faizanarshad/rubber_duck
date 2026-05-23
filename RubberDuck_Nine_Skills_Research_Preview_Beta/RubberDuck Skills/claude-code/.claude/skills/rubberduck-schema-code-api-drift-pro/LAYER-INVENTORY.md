# Layer Inventory

The skill must inventory representation layers before finding drift.

## Required table

```markdown
| Layer | Files / patterns | Evidence type | Count | Status | Caveat |
|---|---|---|---:|---|---|
```

## Layers

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

## Common patterns

```text
schema.prisma
migrations/*.sql
*.graphql
openapi.* / swagger.*
*.proto
models.py / schema.py / serializers.py
pydantic / dataclass / attrs
z.object / yup.object
interface / type / class DTO
router / controller / handler
client generated types
fixtures / factories
```

## Coverage rule

If a layer is absent, say:

```text
not found after search <patterns> over <scope>
```

If a layer is present but not analyzable, say:

```text
found but unsupported by semantic graph; source/search evidence only
```
