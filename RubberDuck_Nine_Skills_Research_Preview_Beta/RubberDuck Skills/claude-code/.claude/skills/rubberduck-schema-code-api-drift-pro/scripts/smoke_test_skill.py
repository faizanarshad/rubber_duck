#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile, json, sys, runpy, contextlib, io

def run(script: Path, args: list[str], cwd: Path | None = None) -> int:
    old_argv = sys.argv[:]
    out = io.StringIO()
    code = 0
    try:
        sys.argv = [str(script)] + args
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
    finally:
        sys.argv = old_argv
    return code

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    tokens = [
        "semantic_mode=\"full\"",
        "ANCHORED_CONCEPT",
        "SCOPE_DRIFT",
        "UNCONSTRAINED",
        "No drift row may be reported unless at least two layers are cited",
        "No runtime-failure prediction may be reported unless it points to a specific drift cell",
    ]
    missing = [t for t in tokens if t not in skill]
    if missing:
        print("FAIL: missing smoke tokens", missing)
        return 2
    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td)
        (bundle / "evidence").mkdir()
        (bundle / "REPORT.md").write_text(
            """# X - Drift Report
## \u00a70 Triangle Stat
## \u00a71 Layer Inventory
## \u00a72 Concept Map
## \u00a73 Concept Fusion Ledger
## \u00a74 Drift Matrix
## \u00a75 Predicted Runtime Failures
## \u00a76 Round-Trip Proof
## \u00a77 Remediation Diffs
## \u00a78 Coverage Gaps and Unsupported Surfaces
## \u00a79 Negative Claims
## \u00a710 Tool Health
## \u00a711 Falsification Recipes
""",
            encoding="utf-8",
        )
        evidence_files = [
            "layer-inventory.md","concept-map.md","concept-fusion-ledger.md","runtime-failure-predictions.md",
            "round-trip-proof.md","remediation-diffs.md","coverage-gaps.md","negative-claims.md",
            "falsification-recipes.md","tool-health.md","protocol-completion.md"
        ]
        for name in evidence_files:
            (bundle / "evidence" / name).write_text(f"# {name}\nDB_SCHEMA CODE_TYPE API_CONTRACT Status\nmode declared\nRubberDuck setup\nlayer inventory\nconcept extraction\nconcept fusion\ndrift matrix\nruntime failure prediction\nround-trip proof\nremediation diffs\nnegative claims\nfalsification recipes\nevidence pack\nHIGH\n", encoding="utf-8")
        (bundle / "evidence" / "schema-drift-summary.json").write_text(json.dumps({
            "mode":"SCOPE_DRIFT", "concepts_mapped":1, "concepts_with_drift":1, "coverage_gaps":[]
        }), encoding="utf-8")
        (bundle / "evidence" / "drift-matrix.csv").write_text(
            "concept_id,canonical_concept,layers_compared,dimension,status,db_value,code_value,api_value,validator_value,evidence,confidence,impact\n"
            "C1,user.email,DB_SCHEMA;API_CONTRACT,D3_NULLABILITY,DRIFT,NOT NULL,,nullable,,schema+api,HIGH,API_CONTRACT_VIOLATION\n",
            encoding="utf-8"
        )
        checks = [
            (root / "scripts" / "verify_report_consistency.py", ["--root", str(bundle)]),
            (root / "scripts" / "check_layer_inventory.py", [str(bundle / "evidence" / "layer-inventory.md")]),
            (root / "scripts" / "check_concept_fusion.py", [str(bundle / "evidence" / "concept-fusion-ledger.md")]),
            (root / "scripts" / "check_drift_matrix.py", [str(bundle / "evidence" / "drift-matrix.csv")]),
            (root / "scripts" / "check_protocol_completion.py", [str(bundle / "evidence" / "protocol-completion.md")]),
        ]
        for script, args in checks:
            code = run(script, args)
            if code != 0:
                print(f"FAIL: {script.name} returned {code}")
                return code
    print("OK: Schema-Code-API Drift Pro smoke test passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
