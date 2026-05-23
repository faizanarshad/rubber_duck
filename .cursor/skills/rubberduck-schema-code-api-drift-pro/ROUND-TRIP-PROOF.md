# Round-Trip Proof

A round-trip proof connects write and read paths.

## Write path

```text
API input -> validator -> handler -> code model -> DB write
```

## Read path

```text
DB row -> code model -> serializer -> API response -> client type
```

## Required table

```markdown
| Concept | Write path evidence | Read path evidence | Round-trip status | Caveat |
|---|---|---|---|---|
```

## Status

```text
FULLY_TRACED
WRITE_ONLY
READ_ONLY
MODEL_ONLY
CONTRACT_ONLY
UNTRACED
```

Do not claim round-trip safety unless both paths are traced or explicitly modeled with caveats.
