#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re

REQUIRED_REPORT_SECTIONS = [
    "§0 Envelope",
    "§1 Verdict",
    "§2 Headline",
    "§3 Input",
    "§4 Import",
    "§5 Path Catalogue",
    "§6 Path-Match Table",
    "§7 Divergences",
    "§8 Side-Effect",
    "§9 Exception",
    "§10 Witness",
    "§11 Generated",
    "§12 Undecidable",
    "§13 Structural",
    "§14 Falsification",
    "§15 Tool Health",
    "§16 Evidence Pack",
]

REQUIRED_EVIDENCE = [
    "mirror-summary.json",
    "before-source.md",
    "after-source.md",
    "import-context.md",
    "path-catalogue-before.md",
    "path-catalogue-after.md",
    "path-match-table.md",
    "side-effect-manifest.md",
    "exception-envelope.md",
    "witness-inputs.md",
    "generated-tests.md",
    "undecidable-blockers.md",
    "structural-drift.md",
    "falsification-recipes.md",
    "tool-health.md",
    "protocol-completion.md",
]

LOCAL_MARKERS = [
    "/" + "Users/",
    "C:" + "\\\\" + "Users" + "\\\\",
    "/" + "home/" + "ec2-user/",
    "/" + "mnt/" + "data",
    "sandbox" + ":/",
    "file_" + "000",
    "__" + "MACOSX",
    ".DS" + "_Store",
    "expected " + "findings",
    "Bento" + "ML",
    "Trust" + "Claw",
    "Composio" + "HQ",
    "hermes" + "-agent",
]

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    report = read(root / "REPORT.md")
    errors = []

    if not report:
        errors.append("missing REPORT.md")

    for sec in REQUIRED_REPORT_SECTIONS:
        if sec not in report:
            errors.append(f"missing report section: {sec}")

    ev = root / "evidence"
    if not ev.exists():
        errors.append("missing evidence directory")
    else:
        for rel in REQUIRED_EVIDENCE:
            if not (ev / rel).exists():
                errors.append(f"missing evidence/{rel}")

    summary_path = ev / "mirror-summary.json"
    if summary_path.exists():
        s = json.loads(summary_path.read_text(encoding="utf-8", errors="replace"))
        verdict = s.get("verdict", "")
        if verdict == "PROVEN_EQUIVALENT_UNDER_CONTRACT":
            if int(s.get("divergence_count", 0) or 0) != 0:
                errors.append("equivalence verdict has divergence_count > 0")
            if int(s.get("undecidable_count", 0) or 0) != 0:
                errors.append("equivalence verdict has undecidable_count > 0")
        if verdict == "NOT_EQUIVALENT" and int(s.get("divergence_count", 0) or 0) < 1:
            errors.append("NOT_EQUIVALENT requires divergence_count >= 1")
    else:
        errors.append("missing mirror-summary.json")

    all_text = report
    for p in root.rglob("*"):
        if p.is_file():
            try:
                all_text += "\n" + p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass
    for marker in LOCAL_MARKERS:
        if marker in all_text:
            errors.append(f"private/local marker found: {marker}")

    if "preserved contract" not in report.lower():
        errors.append("report must state preserved contract")
    if "falsification" not in report.lower():
        errors.append("report must include falsification recipes")
    if "side-effect" not in report.lower():
        errors.append("report must include side-effect comparison")
    if "exception" not in report.lower():
        errors.append("report must include exception envelope comparison")

    if errors:
        print("FAIL: mirror report consistency")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: mirror report consistency passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
