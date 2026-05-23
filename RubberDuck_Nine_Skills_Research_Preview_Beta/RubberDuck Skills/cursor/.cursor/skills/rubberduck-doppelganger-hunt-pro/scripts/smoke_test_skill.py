#!/usr/bin/env python3
"""Smoke tests for RubberDuck Doppelganger Hunt Pro.

This script avoids spawning nested Python processes so it remains reliable in agent/cloud sandboxes.
It verifies:
- required skill files are present,
- a synthetic complete bundle passes core consistency logic,
- synthetic broken bundles fail the intended gates.
"""
from __future__ import annotations
import json
import tempfile
from pathlib import Path

REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "DOPPELGANGER-WORKFLOW.md",
    "CANDIDATE-GENERATORS.md",
    "GRAPH-FINGERPRINTS.md",
    "INLINE-DOPPELGANGERS.md",
    "COMMENT-CONTRACT-MINING.md",
    "CLUSTER-ROLE-CLASSIFICATION.md",
    "DIVERGENCE-MATRIX.md",
    "MERGEABILITY-AND-UNIFICATION.md",
    "CHANGE-IMPACT-PREFLIGHT.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "REPORT-TEMPLATE.md",
]

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

PROTOCOL_TERMS = [
    "Mode declared",
    "Candidate generators run",
    "Graph dimension coverage recorded",
    "Inline implementations searched",
    "Comment contracts searched",
    "Cluster roles assigned",
    "Mergeability classified",
    "Change-impact preflight complete",
    "Negative results enumerated",
    "Falsification recipes written",
]

def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def make_bundle(root: Path, bad_included_dimension: bool = False, omit_role: bool = False):
    write(root / "REPORT.md", """
# Doppelganger Hunt — sample

## §0 Envelope
Mode declared: SEEDED
## §1 Sightings
## §2 Candidate Generation Ledger
## §3 Cluster Lineage
## §4 Call-Path / Context Map
## §5 Graph Dimension Coverage
## §6 Divergence Matrix
## §7 Inline Implementations
## §8 Comment Contract Findings
## §9 Cluster Role Classification
## §10 Mergeability Classification
## §11 Change-Impact Preflight
## §12 Unification Plan
## §13 Negative Results
## §14 Tool Health and Coverage Gaps
## §15 Falsification Recipes
""")
    ev = root / "evidence"
    contents = {
        "candidate-generators.md": "| G1 | Lexical | q | all | 2 | 1 | 1 | ok |",
        "function-inventory.md": "Status: available",
        "cluster-members.md": "member rows",
        "fingerprint-matrix.csv": "pair,F1,F2\nA-B,0.9,0.8\n",
        "graph-dimension-coverage.md": "F1 COMPUTED\nF2 APPROXIMATED\nF5 SKIPPED not included\n",
        "divergence-matrix.md": "differences",
        "source-snippets.md": "snippets",
        "inline-implementations.md": "inline searched",
        "comment-contracts.md": "comments searched",
        "call-path-map.md": "call paths",
        "negative-results.md": "negative results",
        "mergeability.md": "SAFE_TO_MERGE",
        "change-impact-preflight.md": "preflight",
        "unification-plan.md": "plan",
        "tool-health.md": "health",
        "falsification-recipes.md": "recipes",
        "protocol-completion.md": "\n".join(PROTOCOL_TERMS),
    }
    for name, text in contents.items():
        write(ev / name, text)
    roles = {"a": "CANONICAL", "b": "INLINE_COPY"}
    if omit_role:
        roles = {"a": "CANONICAL"}
    included = ["F1", "F2"] if not bad_included_dimension else ["F1", "F5"]
    summary = {
        "mode": "SEEDED",
        "repo": "sample",
        "commit": "abc",
        "seed_or_concept": "seed",
        "candidate_generators": [{"id": "G1"}],
        "clusters": [{
            "id": "C1",
            "concept": "sample",
            "named_members": ["a"],
            "inline_members": ["b"],
            "roles": roles,
            "dimension_coverage": {"F1": "COMPUTED", "F2": "APPROXIMATED", "F5": "SKIPPED"},
            "included_dimensions": included,
            "composite_score": 0.88,
            "mergeability": "SAFE_TO_MERGE",
            "unification_recommended": True,
        }],
        "limitations": []
    }
    write(ev / "cluster-summary.json", json.dumps(summary, indent=2))

def check_bundle(root: Path) -> list[str]:
    errors: list[str] = []
    report = (root / "REPORT.md").read_text(encoding="utf-8", errors="replace") if (root / "REPORT.md").exists() else ""
    for sec in REQUIRED_REPORT_SECTIONS:
        if sec not in report:
            errors.append(f"missing report section {sec}")
    ev = root / "evidence"
    if not ev.exists():
        errors.append("missing evidence directory")
    for rel in REQUIRED_EVIDENCE:
        if not (ev / rel).exists():
            errors.append(f"missing evidence/{rel}")
    proto = (ev / "protocol-completion.md").read_text(encoding="utf-8", errors="replace") if (ev / "protocol-completion.md").exists() else ""
    for term in PROTOCOL_TERMS:
        if term not in proto:
            errors.append(f"missing protocol term {term}")
    if (ev / "cluster-summary.json").exists():
        data = json.loads((ev / "cluster-summary.json").read_text(encoding="utf-8", errors="replace"))
        for c in data.get("clusters", []):
            members = list(c.get("named_members", [])) + list(c.get("inline_members", []))
            roles = c.get("roles", {})
            for m in members:
                if m not in roles:
                    errors.append(f"missing role for {m}")
            dims = c.get("dimension_coverage", {})
            for dim in c.get("included_dimensions", []):
                if str(dims.get(dim, "")).upper() not in {"COMPUTED", "APPROXIMATED"}:
                    errors.append(f"included dimension {dim} is not computed/approximated")
    return errors

def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED_SKILL_FILES if not (skill_root / p).exists()]
    if missing:
        print("FAIL: missing skill files")
        for p in missing:
            print(f" - {p}")
        return 2
    skill = (skill_root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    for token in ["semantic_mode=\"full\"", "SEEDED", "CONCEPT", "UNCONSTRAINED", "candidate-generator", "graph-dimension", "comment-contract", "change-impact preflight"]:
        if token not in skill:
            print(f"FAIL: SKILL.md missing token {token}")
            return 2
    with tempfile.TemporaryDirectory() as d:
        good = Path(d) / "good"
        make_bundle(good)
        good_errors = check_bundle(good)
        if good_errors:
            print("FAIL: good fixture failed")
            for e in good_errors:
                print(f" - {e}")
            return 2
        bad1 = Path(d) / "bad_included_dimension"
        make_bundle(bad1, bad_included_dimension=True)
        if not any("included dimension" in e for e in check_bundle(bad1)):
            print("FAIL: bad included-dimension fixture did not fail")
            return 2
        bad2 = Path(d) / "bad_missing_role"
        make_bundle(bad2, omit_role=True)
        if not any("missing role" in e for e in check_bundle(bad2)):
            print("FAIL: bad missing-role fixture did not fail")
            return 2

        bad3 = Path(d) / "bad_missing_evidence"
        make_bundle(bad3)
        (bad3 / "evidence" / "function-inventory.md").unlink()
        if not any("function-inventory" in e for e in check_bundle(bad3)):
            print("FAIL: missing evidence fixture did not fail")
            return 2

        bad4 = Path(d) / "bad_protocol"
        make_bundle(bad4)
        (bad4 / "evidence" / "protocol-completion.md").write_text("Mode declared only", encoding="utf-8")
        if not any("missing protocol term" in e for e in check_bundle(bad4)):
            print("FAIL: bad protocol fixture did not fail")
            return 2
    print("OK: smoke tests passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
