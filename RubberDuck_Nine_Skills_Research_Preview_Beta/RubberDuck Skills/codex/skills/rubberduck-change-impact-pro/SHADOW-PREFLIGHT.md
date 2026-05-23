# Shadow / Doppelganger Pre-flight

A shadow is a different function/module implementing the same concept.

## Why it matters

A change may affect the concept, not only the named function.

## Search strategy

Use names, synonyms, comments, and behavior terms.

Examples:

```text
target: getAvailableTCPPort
search: available.*port|free.*port|port.*listen|server.listen|EADDRINUSE
```

## Fingerprint levels

Label honestly:

```text
lightweight heuristic fingerprint: search_code + read_source
semantic fingerprint: symbols/call/data-flow available
computed fingerprint: explicit AST/CFG/DDG evidence present
```

Do not claim computed AST/CFG fingerprint without evidence.

## Output

```text
§0.5 Shadow / Doppelganger Pre-flight
```

Required table:

| Shadow candidate | File | Similarity evidence | Production/test | Public/internal | Action |
|---|---|---|---|---|---|

Action values:

```text
ignore
note
review
unify candidate
blocks target-only analysis
```

Do not halt unless target ambiguity is unsafe.
