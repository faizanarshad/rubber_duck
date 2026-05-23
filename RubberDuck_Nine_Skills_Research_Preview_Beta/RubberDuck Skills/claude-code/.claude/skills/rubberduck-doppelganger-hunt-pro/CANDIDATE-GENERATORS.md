# Candidate Generators

A doppelganger report is only as good as its candidate generation.

## Required ledger

```markdown
| ID | Generator | Query / method | Scope | Matches | Kept | Discarded | Reason |
|---|---|---|---|---:|---:|---:|---|
```

## Generators

```text
G1 Lexical/name search
G2 Import/API surface search
G3 Effect-token search
G4 Type signature search
G5 AST skeleton search
G6 DDG/trace-variable similarity
G7 Call-context similarity
G8 Inline-pattern search
G9 Comments/docs/history search
G10 CI redundancy/near-duplicate seed
G11 Test/prod boundary search
G12 Public export / hidden helper search
```

## Negative-result rule

If the report says there are no more doppelgangers, it must cite generator rows showing scope and match counts.

## Prefilter honesty

If prefiltering is used, say:

```text
Candidate generation used prefilters.
The report is exhaustive for the listed candidate generators, not for all theoretical functions.
```

Do not write "every loaded function was fingerprinted" unless every loaded function actually was fingerprinted across required dimensions.


## Required lowercase ledger fields

Every candidate generator row must include lowercase fields: matches, kept, discarded.
