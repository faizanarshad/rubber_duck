#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


def resolve_report(arg: str | None) -> tuple[Path, Path]:
    target = Path(arg) if arg else Path("REPORT.md")
    if target.is_dir():
        return target, target / "REPORT.md"
    return target.parent, target


root, report = resolve_report(sys.argv[1] if len(sys.argv) > 1 else None)
if not report.exists():
    print(f"Missing report: {report}")
    sys.exit(1)

text = report.read_text(encoding="utf-8", errors="replace")
lower = text.lower()

required_sections = [
    "§0 Atlas Envelope",
    "§A Architectural Surprises",
    "§1 Major Symbols",
    "§2 Entry Points",
    "§3 Call-Chain Atlas",
    "§4 Data-Flow Atlas",
    "§8 Cross-Package Coupling",
    "§10.5 Bus-Factor Function",
    "§13 30 / 60 / 180-Minute Reading Plan",
    "§14 Tool Health",
]

required_markers = [
    ("Atlas/not-security framing", ["not a vulnerability report", "not a security audit"]),
    ("feature mode decision", ["WHOLE_REPO_ATLAS", "FEATURE_ATLAS", "Atlas mode"]),
    ("evidence pack status", ["Evidence pack", "evidence/evidence-manifest.md"]),
    ("evidence manifest", ["evidence-manifest.md", "Evidence Manifest"]),
    ("full symbol appendix or scoped caveat", ["Full Symbol Inventory", "evidence/symbols-overview.md", "curated major-symbol"]),
    ("falsification recipes", ["Falsification Recipes", "evidence/falsification-recipes.md"]),
    ("cross-package evidence table", ["Cross-Package Coupling Evidence", "evidence/cross-package-coupling.md", "cross-package coupling unavailable"]),
    ("bus-factor function", ["Bus-Factor Function", "bus-factor function unavailable"]),
    ("machine-readable summary", ["atlas-summary.json", "Machine summary"]),
    ("evidence level", ["raw tool output", "normalized evidence", "report-derived evidence", "Evidence level"]),
]

missing = [s for s in required_sections if s not in text]
if missing:
    print("Missing required atlas sections:")
    for s in missing:
        print(f" - {s}")
    sys.exit(2)

if "Unsupported" not in text and "unsupported" not in text:
    print("Missing unsupported surface disclosure")
    sys.exit(3)

if "Evidence Ledger" not in text and "evidence/claim-ledger.md" not in text:
    print("Missing Evidence Ledger")
    sys.exit(4)

marker_missing = []
for label, options in required_markers:
    if not any(option.lower() in lower for option in options):
        marker_missing.append(label)
if marker_missing:
    print("Missing required protocol markers:")
    for label in marker_missing:
        print(f" - {label}")
    sys.exit(5)

is_deep = "deep" in lower
report_only = "report-only" in lower or "report only" in lower
if is_deep and not report_only:
    evidence = root / "evidence"
    for name in [
        "evidence-manifest.md",
        "atlas-summary.json",
        "falsification-recipes.md",
        "bus-factor-function.md",
        "cross-package-coupling.md",
        "symbols-overview.md",
    ]:
        if not (evidence / name).exists() and f"evidence/{name}" not in text:
            print(f"Missing DEEP evidence artifact or report link: evidence/{name}")
            sys.exit(6)

print("OK: protocol completion check passed")
