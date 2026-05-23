# Drift Matrix

## Required CSV columns

```text
concept_id,canonical_concept,layers_compared,dimension,status,db_value,code_value,api_value,validator_value,evidence,confidence,impact
```

## Status values

```text
MATCH
DRIFT
UNKNOWN
NOT_APPLICABLE
```

## Dimensions

```text
D1_NAME_ALIAS
D2_TYPE
D3_NULLABILITY
D4_FORMAT_LENGTH_PRECISION
D5_DEFAULT_VALUE
D6_VALIDATION
D7_CARDINALITY_RELATION
D8_ENCODING_SERIALIZATION
D9_AUTH_VISIBILITY
D10_LIFECYCLE_STATE
D11_VERSIONING_COMPATIBILITY
D12_TEST_FIXTURE_CLIENT
```

## Rules

No drift row without:

```text
canonical concept
>=2 compared layers
specific dimension
evidence pointer
confidence
```

UNKNOWN is acceptable and better than guessing.
