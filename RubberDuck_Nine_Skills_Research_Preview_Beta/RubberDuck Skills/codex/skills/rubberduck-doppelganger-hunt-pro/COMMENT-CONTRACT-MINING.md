# Comment Contract Mining

Comments often explain why duplicates exist.

## Search targets

```text
function names
cluster concept terms
resource names
TODO/FIXME/NOTE/WARNING
"do not use"
"race"
"workaround"
"temporary"
"copy"
"duplicate"
"cannot"
"because"
test names
docstrings/JSDoc
README snippets
commit messages when available
```

## Required output

```markdown
| Comment / doc | Location | Mentions | Contract implied | Explains divergence? | Evidence |
|---|---|---|---|---|---|
```

## Divergence reasons

```text
accidental
API visibility gap
historical leftover
bug workaround
safety/security workaround
performance reason
compatibility reason
test fixture convenience
deliberate divergence
unknown
```

Comment-contract evidence is explanatory. It should not override code evidence.
