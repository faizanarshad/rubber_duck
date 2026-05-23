#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def resolve_report(arg: str | None) -> tuple[Path, Path]:
    target = Path(arg) if arg else Path("REPORT.md")
    if target.is_dir():
        root = target
        report = root / "REPORT.md"
    else:
        report = target
        root = report.parent
    return root, report


root, report = resolve_report(sys.argv[1] if len(sys.argv) > 1 else None)
errors: list[str] = []
warnings: list[str] = []

if not report.exists():
    print(f"Missing report: {report}")
    sys.exit(1)

text = read(report)
lower = text.lower()
evidence = root / "evidence"


def has_any(*needles: str) -> bool:
    return any(n.lower() in lower for n in needles)


def require(label: str, *needles: str) -> None:
    if not has_any(*needles):
        errors.append(f"Missing {label}.")


def deep_mode() -> bool:
    if "report-only" in lower and "deep" not in lower:
        return False
    return bool(re.search(r"\bDEEP\b", text)) or "budget | deep" in lower or "budget: deep" in lower


is_deep = deep_mode()
report_only = "report-only" in lower or "report only" in lower

if "complete coverage" in lower and "unsupported" not in lower:
    errors.append("Report claims complete coverage without unsupported-surface caveat.")

require("Atlas/not-security framing", "not a vulnerability report", "not a security audit")
require("Architectural Surprises section", "Architectural Surprises")
require("Bus-Factor Function section or unavailable statement", "Bus-Factor Function", "bus-factor function unavailable")
require("Falsification Recipes or evidence link", "Falsification Recipes", "evidence/falsification-recipes.md")
require("Evidence Ledger or claim ledger link", "Evidence Ledger", "evidence/claim-ledger.md")
require("Unsupported Surfaces", "Unsupported Surfaces", "unsupported surfaces")
require("Tool Health", "Tool Health", "evidence/tool-health.md")
require("Reading Plan", "Reading Plan", "30 / 60 / 180")
require("Full Symbol Inventory or evidence link", "Full Symbol Inventory", "evidence/symbols-overview.md")
require("Cross-Package Coupling Evidence table or unavailable statement", "Cross-Package Coupling Evidence", "evidence/cross-package-coupling.md", "cross-package coupling unavailable")
require("anti-claims or negative claims", "Anti-Claims", "negative claims", "evidence/negative-claims.md")

if is_deep and not report_only:
    required_evidence = [
        "evidence-manifest.md",
        "atlas-summary.json",
        "falsification-recipes.md",
        "bus-factor-function.md",
        "cross-package-coupling.md",
        "symbols-overview.md",
    ]
    if not evidence.exists():
        errors.append("DEEP mode report is missing evidence/ directory.")
    else:
        for name in required_evidence:
            if not (evidence / name).exists():
                errors.append(f"DEEP mode evidence file missing: evidence/{name}")

    summary = evidence / "atlas-summary.json"
    if summary.exists():
        try:
            json.loads(read(summary))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid evidence/atlas-summary.json: {exc}")

if evidence.exists():
    contradiction_patterns = [
        "atlas-summary.json absent",
        "atlas-summary.json is absent",
        "evidence/atlas-summary.json absent",
        "evidence/atlas-summary.json is absent",
        "evidence pack is absent",
        "no evidence files were generated",
        "evidence files were not generated",
        "not materialized as discrete evidence",
        "only report.md exists",
    ]
    for pattern in contradiction_patterns:
        if pattern in lower:
            errors.append(f"Report/evidence contradiction: report says '{pattern}' while evidence/ exists.")
    if (evidence / "atlas-summary.json").exists() and "atlas-summary.json" in lower and "absent" in lower:
        errors.append("Report mentions atlas-summary.json as absent while evidence/atlas-summary.json exists.")

    if "raw rubberduck transcript" in lower and not (evidence / "raw-tool-output").exists():
        warnings.append("Report mentions raw RubberDuck transcript but evidence/raw-tool-output/ is absent.")

negative_patterns = ["no ", "none ", "not found", "zero matches"]
if any(p in lower for p in negative_patterns):
    if "search pattern" not in lower and "evidence ledger" not in lower and "negative-claims.md" not in lower:
        warnings.append("Negative claims appear but no search/evidence ledger is visible.")

if "Architectural Surprises" in text:
    surprise_count = len(re.findall(r"(?im)^###?\s+Surprise", text))
    no_surprise = "no architectural surprises detectable" in lower
    if surprise_count < 3 and not no_surprise:
        warnings.append("Fewer than 3 architectural surprises and no explicit no-surprise statement.")

if "evidence pack" not in lower and "evidence/evidence-manifest.md" not in lower:
    warnings.append("Evidence pack status is not visible.")

scan_files = [report]
for subdir, patterns in [("evidence", ["*.md", "*.json"]), ("validation", ["*.txt"]), ("", ["README.md"])]:
    base = root / subdir if subdir else root
    if base.exists():
        for pattern in patterns:
            scan_files.extend(p for p in base.glob(pattern) if p.is_file())

blocking_markers = [
    "/" + "Users" + "/",
    "C:" + "\\\\" + "Users" + "\\\\",
    "/" + "home" + "/" + "ec2-user",
    "/" + "mnt" + "/" + "data",
    "file_" + "000000",
    "sandbox" + ":",
]
for path in sorted(set(scan_files)):
    content = read(path)
    for marker in blocking_markers:
        if marker in content:
            errors.append(f"Local/private path marker found in {path}: {marker}")
    if "__" + "MACOSX" in path.name or path.name == "." + "DS_Store":
        errors.append(f"Forbidden metadata file present: {path}")
    if re.search(r"(?<![A-Za-z0-9_])/" + "home" + r"/[A-Za-z0-9_.-]+", content):
        warnings.append(f"Potential /home/ path in {path}; review if this is a real local path.")

if errors:
    print("Consistency errors:")
    for e in errors:
        print(f" - {e}")
    sys.exit(2)

if warnings:
    print("Warnings:")
    for w in warnings:
        print(f" - {w}")

print("OK: report consistency check passed")
