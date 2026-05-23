# Concept Fusion

Concept fusion is the riskiest part of this skill. Do not hallucinate equivalence between fields.

## Concept evidence row

```markdown
| Concept | Layer | Name/path | Evidence | Type/shape | Confidence |
|---|---|---|---|---|---|
```

## Fusion ledger

```markdown
| Fusion ID | Canonical concept | Layer members | Confidence | Why fused | Why not rejected |
|---|---|---|---|---|---|
```

## Confidence rules

HIGH requires at least two of:

```text
same normalized field name
same entity/model context
same route/handler/repository path
trace_variable or call_chain linkage
same serializer/validator path
contract-to-handler evidence
```

MEDIUM requires:

```text
same normalized name plus co-occurrence in a related path
```

LOW is lexical similarity only. LOW cannot become final drift without more evidence.

REJECT if:

```text
same name but different entity
different route namespace
different data lifecycle
unrelated test fixture
only docs mention with no code link
```

## Negative fusion

Record rejected fusions when names are deceptively similar.
