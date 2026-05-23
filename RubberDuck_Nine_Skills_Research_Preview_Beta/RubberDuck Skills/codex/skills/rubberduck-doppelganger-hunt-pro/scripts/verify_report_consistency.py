#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

REQUIRED_REPORT_SECTIONS = [
    "§0 Envelope",
    "§1 Sightings",
    "§2 Candidate Generation Ledger",
    "§5 Graph Dimension Coverage",
    "§6 Divergence Matrix",
    "§7 Inline Implementations",
    "§8 Comment Contract Findings",
    "§9 Cluster Role Classification",
    "§10 Mergeability Classification",
    "§11 Change-Impact Preflight",
    "§12 Unification Plan",
    "§13 Negative Results",
    "§14 Tool Health",
    "§15 Falsification Recipes",
]

REQUIRED_EVIDENCE = [
    "candidate-generators.md",
    "function-inventory.md",
    "cluster-summary.json",
    "cluster-members.md",
    "fingerprint-matrix.csv",
    "graph-dimension-coverage.md",
    "divergence-matrix.md",
    "source-snippets.md",
    "inline-implementations.md",
    "comment-contracts.md",
    "call-path-map.md",
    "negative-results.md",
    "mergeability.md",
    "change-impact-preflight.md",
    "unification-plan.md",
    "tool-health.md",
    "falsification-recipes.md",
    "protocol-completion.md",
]

BANNED_MARKERS = ["/"+"Users/", "C:"+"\\\\Users\\\\", "/home/"+"ec2-user/", "/mnt/"+"data", "file_"+"000", "sandbox"+":/", "__"+"MACOSX"]

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Report bundle root")
    args = ap.parse_args()
    root = Path(args.root)
    report = read(root / "REPORT.md")
    errors = []
    warnings = []

    if not report:
        errors.append("Missing REPORT.md")

    for sec in REQUIRED_REPORT_SECTIONS:
        if sec not in report:
            errors.append(f"REPORT.md missing section: {sec}")

    evidence_dir = root / "evidence"
    if not evidence_dir.exists():
        errors.append("Missing evidence/ directory")
    else:
        for rel in REQUIRED_EVIDENCE:
            p = evidence_dir / rel
            if not p.exists():
                errors.append(f"Missing evidence/{rel}")

    all_text = report
    for p in root.rglob("*"):
        if p.is_file():
            try:
                all_text += "\n" + read(p)
            except Exception:
                pass
    for marker in BANNED_MARKERS:
        if marker in all_text:
            errors.append(f"Local/private artifact marker found: {marker}")

    # Summary JSON checks
    summary_path = evidence_dir / "cluster-summary.json"
    if summary_path.exists():
        try:
            summary = json.loads(read(summary_path))
            clusters = summary.get("clusters", [])
            if not isinstance(clusters, list):
                errors.append("cluster-summary.json: clusters is not a list")
            for c in clusters:
                cid = c.get("id", "<unknown>")
                named = c.get("named_members", [])
                inline = c.get("inline_members", [])
                roles = c.get("roles", {})
                if len(roles) < len(named) + len(inline):
                    errors.append(f"cluster {cid}: fewer roles than members")
                dim = c.get("dimension_coverage", {})
                if not dim:
                    errors.append(f"cluster {cid}: missing dimension_coverage")
                else:
                    for k, v in dim.items():
                        status = str(v).upper()
                        if status not in {"COMPUTED", "APPROXIMATED", "SKIPPED", "UNAVAILABLE", "NOT_APPLICABLE"}:
                            errors.append(f"cluster {cid}: invalid dimension status {k}={v}")
                included = set(c.get("included_dimensions", []))
                for d in included:
                    if str(dim.get(d, "")).upper() not in {"COMPUTED", "APPROXIMATED"}:
                        errors.append(f"cluster {cid}: included dimension {d} is not computed/approximated")
                if c.get("composite_score") is not None and not c.get("included_dimensions"):
                    errors.append(f"cluster {cid}: composite_score present but included_dimensions absent")
        except Exception as e:
            errors.append(f"cluster-summary.json parse failed: {e}")

    # Score inclusion sanity
    dim_text = read(evidence_dir / "graph-dimension-coverage.md") if evidence_dir.exists() else ""
    if "SKIPPED included" in dim_text or "UNAVAILABLE included" in dim_text:
        errors.append("Skipped/unavailable dimensions appear included in score")

    # Candidate generator ledger
    gen_text = read(evidence_dir / "candidate-generators.md") if evidence_dir.exists() else ""
    if gen_text and not re.search(r"\|\s*G\d+", gen_text):
        warnings.append("candidate-generators.md has no G# generator rows")

    if errors:
        print("FAIL: Doppelganger report consistency")
        for e in errors:
            print(f" - {e}")
        if warnings:
            print("Warnings:")
            for w in warnings:
                print(f" - {w}")
        return 2

    print("OK: Doppelganger report consistency checks passed")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f" - {w}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
