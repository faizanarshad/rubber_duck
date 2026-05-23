# Evidence Governance

Read `EVIDENCE-PACK.md` before finalizing any DEEP Atlas bundle.

## Evidence pack

For every DEEP Atlas, generate an evidence pack unless the user explicitly asked for report-only output. The final report may summarize; the evidence pack carries complete tool-backed details.

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

Rules:

```text
normalize private local paths to repo-relative paths where possible
record exact tool/query text and result scope
record missing or degraded raw artifacts in the Atlas envelope
do not treat final prose as a substitute for evidence files
do not let REPORT.md say evidence files or atlas-summary.json are absent when the bundle contains them
```

## Evidence levels

Every evidence pack must declare exactly which level is present:

```text
raw tool output
normalized evidence
report-derived evidence
```

Raw RubberDuck/tool transcripts are preferred but not mandatory. If raw outputs are absent, explicitly label the pack as normalized/derived or report-derived, not raw.

`atlas-summary.json` is required in DEEP mode unless report-only output was explicitly requested.

Recommended schema:

```json
{
  "repo": "",
  "commit": "",
  "mode": "WHOLE_REPO_ATLAS or FEATURE_ATLAS",
  "coverage": {
    "semantic_supported": [],
    "unsupported_surfaces": [],
    "tool_health": []
  },
  "entry_points": [],
  "major_symbols": [],
  "call_chains": [],
  "data_flows": [],
  "architectural_surprises": [],
  "bus_factor_function": {},
  "reading_plan": {},
  "confidence": "",
  "caveats": []
}
```

## Evidence labels

Every major claim must be labeled:

```text
RubberDuck codebase-intelligence
symbols_overview
call_chain
trace_variable
search_code
read_source
package metadata
manual inference
unsupported
out of scope
```

## Evidence ledger

```markdown
| Claim | Evidence type | Tool/query | Scope | Confidence | Caveat |
|---|---|---|---|---|---|
```

For DEEP mode, mirror or link the ledger at `evidence/claim-ledger.md`.

## Negative claims

Negative claims require:

```text
search pattern
searched scope
match count
unsupported surfaces
invalidating condition
```

Example:

```text
Claim: no CLI entry point found.
Evidence: search_code("console_scripts|def main|argparse|click|typer") over loaded Python analyses returned 0 matches.
Caveat: shell scripts and package metadata were not reviewed.
```

For DEEP mode, mirror or link major negative claims at `evidence/negative-claims.md`.

## Falsification recipes

Every major section must include or link to a falsification recipe. Centralize them in `evidence/falsification-recipes.md` when the report would become too long.

Required format:

```markdown
| Claim / section | Tool call or check to refute | Expected contradiction | Evidence file |
|---|---|---|---|
```

Minimum required recipe coverage:

```text
architectural surprises
entry points
call chains
data flows
architectural spine
cross-package coupling
bus-factor function
unsupported surfaces
major negative claims
```

If a recipe cannot be written because a tool is unavailable, mark the claim degraded and record the blocker in `evidence/tool-health.md`.

## Anti-claim section

Every report must include:

```text
What this atlas does NOT claim
```

Examples:

```text
does not claim unsupported surfaces are clean
does not claim dynamic runtime dispatch is fully resolved
does not claim external dependencies are understood
does not claim all generated/vendor code is meaningful
```
