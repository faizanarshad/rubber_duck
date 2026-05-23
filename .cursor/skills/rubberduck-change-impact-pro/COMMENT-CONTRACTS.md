# Comment Contract Analysis

Comments can be informal contracts. For impact analysis, stale comments can break maintainability and reviewer trust.

## Search

Search target name, concept terms, and adjacent comments.

## Mandatory output

```text
§10 ★ Comment Contract
```

Required table:

| Comment / doc | File:line | Contract stated | Change impact | Required edit |
|---|---|---|---|---|

## Priority

Never drop comment contracts from QUICK/STANDARD/DEEP reports when matches exist.

## Examples of contracts

```text
TOCTOU warning
do not remove
public API promise
compatibility note
race/concurrency assumption
performance assumption
migration warning
```
