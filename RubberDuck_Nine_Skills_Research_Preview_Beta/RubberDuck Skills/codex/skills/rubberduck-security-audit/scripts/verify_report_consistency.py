#!/usr/bin/env python3
"""Report consistency checker for RubberDuck Security Audit.

The checker flags contradictions and missing evidence links. It does not decide exploitability.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def ids(text: str, prefix: str = "F") -> set[str]:
    return set(re.findall(rf"\b{prefix}-\d{{3}}\b", text))


def has_complete_status(report: str) -> bool:
    return bool(
        re.search(r"audit status\s*\|?\s*complete\b", report, re.I)
        or re.search(r"audit status:\s*complete\b", report, re.I)
    )


def placeholder_like(text: str) -> bool:
    stripped = text.strip()
    return (
        len(stripped) < 20
        or bool(re.fullmatch(r"(?:placeholder|tbd|todo|n/?a|none|-+|missing)\s*", stripped, re.I))
        or bool(re.search(r"\b(?:TBD|TODO|PLACEHOLDER)\b", stripped, re.I))
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)

    report = read(root / "REPORT.md")
    scope = read(root / "SCOPE.md")
    f_ledger = read(root / "ledgers" / "f-ledger.md")
    p_ledger = read(root / "ledgers" / "p-ledger.md")
    claim_ledger = read(root / "ledgers" / "claim-ledger.md")
    negative = read(root / "ledgers" / "negative-claims.md")
    protocol = read(root / "ledgers" / "protocol-completion.md")
    coverage_gap_ledger = read(root / "ledgers" / "coverage-gaps.md")
    defense_ledger = read(root / "ledgers" / "defense-ledger.md")
    severity_downgrades = read(root / "evidence" / "severity_downgrade_notes.md")
    severity_downgrades += "\n" + read(root / "ledgers" / "severity-downgrades.md")

    dedup = read(root / "evidence" / "rootcause_dedup.md")
    tier2 = read(root / "evidence" / "tier2_validation.md")
    tool_health = read(root / "evidence" / "tool-health.md")
    unsupported = read(root / "evidence" / "unsupported_surfaces.md")
    coverage = read(root / "evidence" / "coverage_governance.md")
    open_gaps = read(root / "evidence" / "open_coverage_gaps.md")
    defense = read(root / "evidence" / "defense_verification.md")
    sink_census = read(root / "ledgers" / "sink-census.md")
    route_file_census = read(root / "ledgers" / "route-file-census.md")
    api_file_census = read(root / "ledgers" / "api-response-file-census.md")

    errors: list[str] = []
    warnings: list[str] = []

    if not report:
        errors.append("Missing REPORT.md")
    complete_status = has_complete_status(report)
    if complete_status:
        if placeholder_like(scope):
            errors.append("Report claims Complete but SCOPE.md is missing, too short, or placeholder-like")
        elif not re.search(r"\b[0-9a-f]{12,40}\b", scope, re.I):
            errors.append("Report claims Complete but SCOPE.md does not contain a pinned commit hash")
        if not re.search(r"\b[0-9a-f]{12,40}\b", report, re.I):
            errors.append("Report claims Complete but REPORT.md does not contain a pinned commit hash")
    if not f_ledger:
        errors.append("Missing ledgers/f-ledger.md")

    report_f = ids(report, "F")
    ledger_f = ids(f_ledger, "F")
    dedup_f = ids(dedup, "F")

    if ledger_f - report_f:
        errors.append(f"F IDs in f-ledger missing from report: {sorted(ledger_f - report_f)}")
    if report_f - ledger_f:
        errors.append(f"F IDs in report missing from f-ledger: {sorted(report_f - ledger_f)}")
    if ledger_f and dedup and ledger_f - dedup_f:
        warnings.append(f"F IDs absent from rootcause_dedup.md: {sorted(ledger_f - dedup_f)}")

    joined = "\n".join([report, f_ledger])

    # Tier-2 claims
    if re.search(r"Tier[- ]2", joined, re.I):
        if not tier2:
            errors.append("Tier-2 claimed but evidence/tier2_validation.md missing")
        if re.search(r"not attempted", f_ledger, re.I) and tier2:
            errors.append("f-ledger says Tier-2 not attempted while tier2_validation.md exists")
        for poc in re.findall(r"\b(poc_[\w-]+\.py)\b", tier2):
            if not (root / "evidence" / poc).exists():
                errors.append(f"tier2_validation.md references missing PoC: evidence/{poc}")

    # P0/P1 runtime validation status
    if re.search(r"\b(P0|P1|Critical|RCE|code execution|deserialization)\b", joined, re.I):
        if "runtime validation incomplete" in report.lower() or re.search(r"Tier[- ]2", joined, re.I):
            pass
        else:
            warnings.append("High-risk findings present but no Tier-2 status or runtime-validation-incomplete status found")

    # Prior-run regression
    if re.search(r"prior-run|prior report|regression ledger", report, re.I):
        if not p_ledger and "P-ledger" not in report:
            warnings.append("Prior-run regression mentioned but no ledgers/p-ledger.md found")
        if p_ledger:
            statuses = ["promoted", "merged", "ruled out", "weakened", "downgraded", "open", "invalidated", "reproduced", "reused"]
            if not any(s in p_ledger.lower() for s in statuses):
                errors.append("p-ledger exists but no recognized current-status terms found")
            if "tier-2" in p_ledger.lower() and not any(s in p_ledger.lower() for s in ["reproduced", "reused", "invalidated", "runtime-validation incomplete"]):
                errors.append("p-ledger references prior Tier-2 evidence without reproduced/reused/invalidated/incomplete status")

    prior_blob = "\n".join([report, p_ledger])
    prior_reviewed_high = re.search(
        r"(team-reviewed|reviewed prior|prior reviewed|prior report|prior-run|prior finding).{0,160}\b(High|Critical)\b"
        r"|\b(High|Critical)\b.{0,160}(team-reviewed|reviewed prior|prior reviewed|prior report|prior-run|prior finding)",
        prior_blob,
        re.I | re.S,
    )
    prior_downgrade = re.search(
        r"\b(High|Critical)\b\s*(?:->|=>|to)\s*\b(Medium|Low|Info|Informational)\b"
        r"|\b(downgraded?|downgrade|reduced|lowered|weakened|reclassified)\b.{0,180}\b(Medium|Low|Info|Informational)\b",
        prior_blob,
        re.I | re.S,
    )
    if prior_reviewed_high and prior_downgrade:
        inline_note = "\n".join(
            m.group(0)
            for m in re.finditer(r"(?:^|\n)#{1,4}\s*.*downgrade note.*(?:\n.+){0,20}", prior_blob, re.I)
        )
        downgrade_note = "\n".join([severity_downgrades, inline_note])
        if placeholder_like(downgrade_note):
            errors.append("Prior reviewed High/Critical finding appears downgraded without a dedicated downgrade note")
        elif not any(
            re.search(pat, downgrade_note, re.I | re.S)
            for pat in [
                r"vulnerable code changed",
                r"exploit path no longer reaches (?:the )?sink",
                r"reviewed threat model.*out of scope|threat model.*out of scope",
                r"prior report'?s severity basis.*factually wrong|severity basis.*factually wrong",
            ]
        ):
            errors.append("Severity downgrade note lacks an accepted proof basis for lowering prior reviewed High/Critical severity")

    # Claim firewall basics
    if not claim_ledger and "Claim Firewall" in report:
        warnings.append("Report mentions Claim Firewall but no ledgers/claim-ledger.md found")
    if not negative and re.search(r"\bno\s+(unsafe|auth|subprocess|ssrf|deserialization|model|token|eval|shell|critical|high)", report, re.I):
        warnings.append("Report contains negative-looking claims but no ledgers/negative-claims.md found")

    # Unsupported and uncovered surfaces
    if "unsupported surface" in report.lower() and not unsupported:
        warnings.append("Unsupported surfaces mentioned but evidence/unsupported_surfaces.md missing")
    if "open coverage gaps" in report.lower() and not (open_gaps or coverage_gap_ledger):
        warnings.append("Open coverage gaps mentioned but no evidence/open_coverage_gaps.md or ledgers/coverage-gaps.md found")

    combined_coverage = "\n".join([report, coverage, open_gaps, coverage_gap_ledger])
    blocking_gap = (
        re.search(r"blocks complete\??\s*[:|]\s*(yes|true|blocking)", combined_coverage, re.I)
        or re.search(r"open coverage gaps", combined_coverage, re.I)
        or re.search(r"\bnot covered\b", combined_coverage, re.I)
    )
    if blocking_gap and has_complete_status(report) and "complete-with-accepted-gaps" not in report.lower():
        errors.append("Report claims Complete while coverage gaps/not-covered surfaces are present. Use partial/accepted-gaps status.")

    # Exhaustive census basics
    if complete_status:
        if not sink_census:
            errors.append("Report claims Complete but ledgers/sink-census.md is missing")
        if not route_file_census:
            errors.append("Report claims Complete but ledgers/route-file-census.md is missing")
        if not api_file_census:
            errors.append("Report claims Complete but ledgers/api-response-file-census.md is missing")
        census_blob = "\n".join([sink_census, route_file_census, api_file_census])
        if "untriaged" in census_blob.lower():
            errors.append("Report claims Complete while census ledgers still contain untriaged rows")

    # Impossible metrics / empty CPG
    tool_blob = "\n".join([report, tool_health, coverage])
    impossible = (
        re.search(r"\b0\s+files\b", tool_blob, re.I)
        and re.search(r"\b(ready|grade|score|clean|100)", tool_blob, re.I)
        and not re.search(r"(degraded|invalid|impossible|tooling-blocked|partial)", tool_blob, re.I)
    )
    if impossible:
        errors.append("Possible impossible clean metrics: 0 files with ready/clean score and no degradation caveat.")

    if "semantic-only" in report.lower() and "not a security negative" not in report.lower() and "degraded" not in report.lower():
        warnings.append("Semantic-only clean appears without degradation caveat")

    # Protocol completion basics
    if "protocol completion" in report.lower() and not protocol:
        warnings.append("Protocol completion mentioned but no ledgers/protocol-completion.md found")
    if complete_status and not protocol:
        errors.append("Report claims Complete but ledgers/protocol-completion.md is missing")
    if protocol:
        required_terms = ["read_source", "control_guards", "call_chain", "def_sites", "simulate_paths"]
        missing_terms = [t for t in required_terms if t not in protocol and t not in report]
        if missing_terms:
            warnings.append(f"Protocol matrix missing expected validation terms: {missing_terms}")

    # Defense verification
    if re.search(r"(false positive|ruled out|guard|defense)", report, re.I) and not (defense or defense_ledger):
        warnings.append("Report uses defense/FP reasoning but no defense verification ledger/evidence found")

    print("RubberDuck Security Audit consistency check")
    print(f"root: {root}")
    print(f"report F IDs: {sorted(report_f)}")
    print(f"f-ledger F IDs: {sorted(ledger_f)}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f" - {w}")

    if warnings and complete_status and "complete-with-accepted-gaps" not in report.lower():
        errors.append("Report claims Complete while consistency warnings remain unresolved")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f" - {e}")
        return 2

    print("\nOK: no blocking consistency errors found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
