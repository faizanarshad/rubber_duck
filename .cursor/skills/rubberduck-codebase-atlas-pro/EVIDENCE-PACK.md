# Evidence Pack

DEEP mode produces an `evidence/` directory unless the user explicitly requests report-only output.

## Required layout

```text
evidence/
  evidence-manifest.md
  tool-calls.md
  symbols-overview.md
  entry-points.md
  call-chains.md
  data-flows.md
  source-snippets.md
  structural-metrics.md
  unsupported-surfaces.md
  claim-ledger.md
  negative-claims.md
  tool-health.md
  falsification-recipes.md
  cross-package-coupling.md
  bus-factor-function.md
  atlas-summary.json
```

If raw RubberDuck or tool responses are exported, store them under:

```text
evidence/raw-tool-output/
```

## Evidence levels

Every bundle and report must declare which evidence level is present:

```text
raw tool output — exact RubberDuck/tool response
normalized evidence — compacted from tool/source output
report-derived evidence — extracted from final report for shareability
```

Raw transcript export is preferred when available, but not mandatory. If raw outputs are absent, the bundle must say `normalized evidence` or `report-derived evidence`; never imply forensic raw output exists.

Do not include non-public benchmark files, expected-result corpora, local machine paths, previous report bundles, or raw transcripts that were not intentionally produced for the current share bundle.

## Evidence manifest

Every evidence pack must include `evidence/evidence-manifest.md`:

```markdown
# Evidence Manifest

| Evidence file | Type | Source | Raw or derived? | Supports sections | Limitations |
|---|---|---|---|---|---|
| tool-calls.md | tool ledger | RubberDuck calls | raw / normalized / report-derived | §13, claim ledger | ... |
| symbols-overview.md | symbol evidence | symbols_overview | raw / normalized / report-derived | §1 | ... |
| entry-points.md | entry-point evidence | search_code, metadata, symbols_overview | raw / normalized / report-derived | §2 | ... |
| call-chains.md | call-chain evidence | call_chain, get_evidence_pack | raw / normalized / report-derived | §3 | ... |
| data-flows.md | data-flow evidence | trace_variable, get_evidence_pack | raw / normalized / report-derived | §4 | ... |
| structural-metrics.md | graph metrics | detailed_repo_analysis | raw / normalized / report-derived | §5-§10 | ... |
| unsupported-surfaces.md | unsupported surface ledger | inventory and tool-health checks | raw / normalized / report-derived | §11, §14 | ... |
| claim-ledger.md | claim ledger | final claim audit | raw / normalized / report-derived | Evidence Ledger | ... |
| negative-claims.md | negative claim ledger | search evidence and caveats | raw / normalized / report-derived | §12 | ... |
| tool-health.md | tool health ledger | tool status checks | raw / normalized / report-derived | §14 | ... |
| falsification-recipes.md | falsification ledger | verifier plan | raw / normalized / report-derived | major sections | ... |
| cross-package-coupling.md | coupling evidence | call_chain, search, source, metadata | raw / normalized / report-derived | §8 | ... |
| bus-factor-function.md | bus-factor evidence | graph/call/data/source evidence | raw / normalized / report-derived | §10.5 | ... |
| atlas-summary.json | machine-readable summary | report + evidence pack | normalized / report-derived | bundle consumers | ... |
```

## Report consistency rules

The final report must:

```text
link to evidence/evidence-manifest.md
state the evidence level present
state whether raw-tool-output exists
not say evidence files are absent when evidence/ exists
not say atlas-summary.json is absent when evidence/atlas-summary.json exists
normalize local paths to repo-relative paths where possible
```
