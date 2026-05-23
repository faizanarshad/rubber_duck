# Architectural Surprises

The final report must include `§A — Architectural Surprises`.

A surprise is an evidence-backed fact that contradicts the obvious read of the repo or reveals a hidden structural property.

In DEEP mode, every surprise must have a falsification recipe in `evidence/falsification-recipes.md` and supporting evidence listed in `evidence/evidence-manifest.md`.

## Surprise rules

Try these rules:

1. **Centrality surprise** — the most central file/function is not the obvious entry point.
2. **Community mismatch** — graph communities do not match directory layout.
3. **Bridge surprise** — one small file/function connects major subsystems.
4. **Articulation surprise** — removing one node disconnects large portions of the graph.
5. **Call-chain surprise** — the longest path begins in an unexpected entry point.
6. **Data-flow surprise** — a variable crosses subsystem boundaries unexpectedly.
7. **Self-spawn / recursion surprise** — a command starts itself, shells out to itself, or loops through the same binary.
8. **Public-but-unused surprise** — an exported/public symbol has no internal callers.
9. **Private-but-central surprise** — an internal helper is more central than public APIs.
10. **Taint/flow surprise** — codebase-level flow contradicts manual expectation.
11. **Duplicate logic surprise** — near-duplicate functions exist in different subsystems.
12. **Unsupported-surface surprise** — important behavior lives outside supported semantic languages.
13. **Docs-vs-code surprise** — metadata/docs imply an entry point that call graph does not support.
14. **Test-coverage surprise** — central code has weak/no apparent tests.

## Surprise floor

Find at least three surprises when possible.

If fewer than three rules fire:

```text
lower threshold and try again
```

If still fewer than three:

```text
This codebase contains no architectural surprises detectable by the selected rules and available evidence.
```

Do not invent surprises.

## Surprise format

```markdown
### Surprise N — <title>

**Evidence:** <tool/action/file:line>
**Why it is surprising:** ...
**Impact for a new engineer:** ...
**How to verify/refute:** <exact query>
```
