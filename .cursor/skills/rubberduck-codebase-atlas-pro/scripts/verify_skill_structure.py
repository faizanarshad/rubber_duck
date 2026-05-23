#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "REPO-INTELLIGENCE-BRIEF.md",
    "ATLAS-PROMPT-COMPILER.md",
    "SEMANTIC-MAP-WORKFLOW.md",
    "SYMBOLS-AND-ENTRYPOINTS.md",
    "CALL-CHAIN-AND-DATA-FLOW.md",
    "ARCHITECTURAL-SURPRISES.md",
    "GRAPH-ATLAS-SECTIONS.md",
    "UNSUPPORTED-SURFACE-ROUTER.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "PROTOCOL-COMPLETION.md",
    "REPORT-TEMPLATE.md",
    "EVIDENCE-PACK.md",
    "FEATURE-ATLAS-MODE.md",
    "ATLAS-SUMMARY-SCHEMA.md",
    "CHANGELOG.md",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    sys.exit(1)

bad_dirs = ["benchmarks", "private", "regression-corpus", "__" + "MACOSX"]
for d in bad_dirs:
    if (root / d).exists():
        print(f"Forbidden directory present: {d}")
        sys.exit(2)

skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
for needle in [
    "rubberduck-codebase-atlas-pro",
    "semantic_mode=\"full\"",
    "DEEP",
    "Architectural Surprises",
    "evidence pack",
    "Bus-Factor Function",
    "FEATURE_ATLAS",
    "evidence/evidence-manifest.md",
    "atlas-summary.json",
]:
    if needle not in skill:
        print(f"Required marker missing from SKILL.md: {needle}")
        sys.exit(3)

support_markers = {
    "EVIDENCE-PACK.md": ["evidence-manifest.md", "raw tool output", "normalized evidence", "report-derived evidence"],
    "FEATURE-ATLAS-MODE.md": ["FEATURE_ATLAS", "feature entry points", "falsification recipes"],
    "ATLAS-SUMMARY-SCHEMA.md": ["atlas-summary.json", "semantic_mode", "cross_package_edges"],
}
for filename, markers in support_markers.items():
    text = (root / filename).read_text(encoding="utf-8", errors="replace")
    for marker in markers:
        if marker not in text:
            print(f"Required marker missing from {filename}: {marker}")
            sys.exit(3)

# Privacy guard.
private_markers = [
    "/" + "Users" + "/",
    "C:" + "\\\\" + "Users" + "\\\\",
    "/" + "home" + "/" + "ec2-user" + "/",
    "mnt" + "/" + "data",
    "private" + " " + "benchmark",
    "expected" + "-" + "finding",
    "expected" + " " + "findings",
    "Bento" + "ML",
    "Trust" + "Claw",
    "security vulnerability details" + " from prior private runs",
]
for path in root.rglob("*"):
    if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
        continue
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in private_markers:
            if marker in text:
                print(f"Private/repo-specific marker found in {path}: {marker}")
                sys.exit(4)

print("OK: RubberDuck UC1 Codebase Atlas Pro Skill structure verified")
