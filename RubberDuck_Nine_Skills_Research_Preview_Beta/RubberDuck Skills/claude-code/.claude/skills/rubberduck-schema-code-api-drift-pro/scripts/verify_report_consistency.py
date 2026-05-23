#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, sys

REQUIRED_REPORT_SECTIONS = [
    "§0 Triangle Stat",
    "§1 Layer Inventory",
    "§2 Concept Map",
    "§3 Concept Fusion Ledger",
    "§4 Drift Matrix",
    "§5 Predicted Runtime Failures",
    "§6 Round-Trip Proof",
    "§7 Remediation Diffs",
    "§8 Coverage Gaps",
    "§9 Negative Claims",
    "§10 Tool Health",
    "§11 Falsification Recipes",
]

REQUIRED_EVIDENCE = [
    "layer-inventory.md",
    "concept-map.md",
    "concept-fusion-ledger.md",
    "drift-matrix.csv",
    "runtime-failure-predictions.md",
    "round-trip-proof.md",
    "remediation-diffs.md",
    "coverage-gaps.md",
    "negative-claims.md",
    "falsification-recipes.md",
    "tool-health.md",
    "schema-drift-summary.json",
    "protocol-completion.md",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Report bundle root")
    args = ap.parse_args()
    root = Path(args.root)
    report = root / "REPORT.md"
    errors = []
    if not report.exists():
        errors.append("missing REPORT.md")
    else:
        txt = report.read_text(encoding="utf-8", errors="replace")
        for section in REQUIRED_REPORT_SECTIONS:
            if section not in txt:
                errors.append(f"missing report section: {section}")
        if "No drift" in txt and "dimension coverage" not in txt and "Layer Inventory" not in txt:
            errors.append("possible no-drift claim without layer/dimension coverage")
    evidence = root / "evidence"
    if not evidence.exists():
        errors.append("missing evidence directory")
    else:
        for rel in REQUIRED_EVIDENCE:
            if not (evidence / rel).exists():
                errors.append(f"missing evidence/{rel}")
        summary = evidence / "schema-drift-summary.json"
        if summary.exists():
            try:
                data = json.loads(summary.read_text(encoding="utf-8", errors="replace"))
                for key in ["mode", "concepts_mapped", "concepts_with_drift", "coverage_gaps"]:
                    if key not in data:
                        errors.append(f"schema-drift-summary.json missing key: {key}")
            except Exception as exc:
                errors.append(f"schema-drift-summary.json invalid JSON: {exc}")
    # Local/private marker scan
    markers = [
        "/" + "Users/",
        "C:" + "\\\\" + "Users" + "\\\\",
        "/" + "home/" + "ec2-user/",
        "/" + "mnt/" + "data",
        "sandbox" + ":/",
        "file_" + "000",
        "__" + "MACOSX",
        ".DS" + "_Store",
    ]
    for p in root.rglob("*"):
        if p.is_file():
            txt = p.read_text(encoding="utf-8", errors="replace")
            for marker in markers:
                if marker in txt or marker in p.as_posix():
                    errors.append(f"private/local marker {marker} in {p.relative_to(root)}")
    if errors:
        print("FAIL")
        for error in errors:
            print(" -", error)
        return 2
    print("OK: Schema Drift report consistency checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
