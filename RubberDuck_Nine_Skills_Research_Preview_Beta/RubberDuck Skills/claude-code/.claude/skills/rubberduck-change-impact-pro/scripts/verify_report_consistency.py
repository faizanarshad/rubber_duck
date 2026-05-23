#!/usr/bin/env python3
"""Verify a Change Impact Pro output bundle.

This checker validates the generated report/evidence package, not the skill files.
It is intentionally conservative: it catches missing evidence artifacts, local path
leaks, unsupported claims, and output-contract regressions.
"""
from __future__ import annotations
from pathlib import Path
import sys, re, json

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors: list[str] = []
warnings: list[str] = []

report = root / "REPORT.md"
summary = root / "impact-summary.json"
evidence = root / "evidence"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

if not report.exists():
    errors.append("Missing REPORT.md")
if not summary.exists():
    errors.append("Missing impact-summary.json")
else:
    try:
        data = json.loads(read(summary))
        required_keys = [
            "target",
            "change",
            "risk",
            "callers",
            "callees",
            "shared_state",
            "data_flows",
            "public_api",
            "mock_sites",
            "comment_contracts",
            "tests_to_run",
            "runtime_optimization",
            "change_order",
            "rollback",
            "tool_health",
            "unsupported_surfaces",
            "claims",
        ]
        for key in required_keys:
            if key not in data:
                errors.append(f"impact-summary.json missing key: {key}")
    except Exception as exc:
        errors.append(f"impact-summary.json invalid JSON: {exc}")

required_evidence = [
    "tool-health.md",
    "tool-calls.md",
    "target-resolution.md",
    "dual-source-adjudication.md",
    "search-results.md",
    "source-snippets.md",
    "callers.md",
    "callees.md",
    "shared-variables.md",
    "data-flows.md",
    "module-state.md",
    "comment-contracts.md",
    "mock-breakage.md",
    "public-api-proof.md",
    "test-coverage-matrix.md",
    "rare-signals.md",
    "runtime-optimization.md",
    "quality-scorecard.md",
    "evidence-reuse-ledger.md",
    "unsupported-surfaces.md",
    "claim-ledger.md",
    "negative-claims.md",
    "falsification-recipes.md",
    "protocol-completion.md",
]
if not evidence.exists():
    errors.append("Missing evidence/ directory")
else:
    for name in required_evidence:
        if not (evidence / name).exists():
            errors.append(f"Missing evidence/{name}")

txt = read(report)
required_sections = [
    "§0 Impact Summary",
    "§0.5 Shadow",
    "§1 Target Resolution",
    "§3 Caller Impact",
    "§4 Callee",
    "§5 Shared State",
    "§7 Mock",
    "§8 Test",
    "§10",
    "§11 Rare",
    "§12 Runtime Optimization",
    "§16 Unknowns",
    "§17 Claim Ledger",
    "§18 Falsification",
    "§19 Paste-Ready",
]
for section in required_sections:
    if section not in txt:
        errors.append(f"REPORT.md missing section marker: {section}")

# Scrub local paths and platform artifact markers in every shareable output file.
banned_patterns = [
    r"/(?:Users|home)/[^\s`]+",
    r"/mnt/(?:data|sandbox)[^\s`]*",
    r"\.claude/projects",
    r"\.codex/",
    r"sandbox\:",
    r"file_[0-9a-fA-F]{3,}",
    r"__MAC" + r"OSX",
    r"\\.DS" + r"_Store",
]
scan_files: list[Path] = []
if report.exists():
    scan_files.append(report)
if summary.exists():
    scan_files.append(summary)
if evidence.exists():
    scan_files.extend([p for p in evidence.rglob("*") if p.is_file()])

for path in scan_files:
    body = read(path)
    for pattern in banned_patterns:
        if re.search(pattern, body):
            errors.append(f"{path.relative_to(root)} contains non-shareable marker matching pattern: {pattern}")

# Claim-ledger quality checks.
claim_ledger = read(evidence / "claim-ledger.md") if evidence.exists() else ""
negative_claims = read(evidence / "negative-claims.md") if evidence.exists() else ""
if claim_ledger:
    if "unsupported" in claim_ledger.lower() and not any(x in claim_ledger.lower() for x in ["caveat", "out of scope", "blocked"]):
        errors.append("claim-ledger.md contains unsupported claims without caveat/out-of-scope/blocked marker")
else:
    errors.append("Missing or empty evidence/claim-ledger.md")

if negative_claims:
    required_negative_fields = ["pattern", "scope", "match", "caveat"]
    for field in required_negative_fields:
        if field not in negative_claims.lower():
            warnings.append(f"negative-claims.md may be missing field: {field}")

# Protocol completion check if present.
protocol = read(evidence / "protocol-completion.md") if evidence.exists() else ""
if protocol and "[ ]" in protocol:
    errors.append("protocol-completion.md contains incomplete checklist items")

if errors:
    print("FAIL")
    for e in errors:
        print(f" - {e}")
    raise SystemExit(1)

if warnings:
    print("WARN")
    for w in warnings:
        print(f" - {w}")

print("OK: Change Impact Pro report consistency verified")
