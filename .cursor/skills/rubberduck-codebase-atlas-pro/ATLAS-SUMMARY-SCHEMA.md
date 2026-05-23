# Atlas Summary Schema

DEEP mode must produce:

```text
evidence/atlas-summary.json
```

The file is required unless the user explicitly requested report-only output.

## Required schema

```json
{
  "repo": "",
  "commit": "",
  "mode": "WHOLE_REPO_ATLAS | FEATURE_ATLAS",
  "budget": "DEEP",
  "rubberduck": {
    "codebase_intelligence": "ok|degraded|unavailable",
    "semantic_intelligence": "ok|degraded|unavailable",
    "semantic_mode": "full",
    "coverage": {}
  },
  "repo_class": "",
  "primary_languages": [],
  "unsupported_surfaces": [],
  "entry_points": [],
  "major_symbols": [],
  "call_chains": [],
  "data_flows": [],
  "architectural_surprises": [],
  "bus_factor_function": {},
  "cross_package_edges": [],
  "reading_plan": {
    "30_min": [],
    "60_min": [],
    "180_min": []
  },
  "claims": {
    "supported": [],
    "negative": [],
    "unsupported": []
  },
  "evidence_files": [],
  "caveats": []
}
```

## Consistency rules

```text
If REPORT.md says atlas-summary.json exists, evidence/atlas-summary.json must exist.
If evidence/atlas-summary.json exists, REPORT.md must not say it is absent.
If the summary is derived, label it derived in the report or evidence manifest.
JSON must parse.
Use repo-relative paths in arrays and caveats.
```

