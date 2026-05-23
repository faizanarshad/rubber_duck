#!/usr/bin/env python3
"""Evidence-pack and protocol-completion checker for RubberDuck Security Audit.

This checker enforces evidence-pack completeness. Missing files may be acceptable only if the
report explicitly marks itself targeted, post-CI graph-degraded, partial, or blocked. CI semantic full absence is never an acceptable degraded fallback.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

RECOMMENDED = [
    "REPORT.md",
    "SCOPE.md",
    "TRACE.md",
    "ledgers/r-ledger.md",
    "ledgers/file-inventory.md",
    "ledgers/sink-census.md",
    "ledgers/route-file-census.md",
    "ledgers/api-response-file-census.md",
    "ledgers/subprocess-census.md",
    "ledgers/secrets-logging-census.md",
    "ledgers/network-fetch-census.md",
    "ledgers/auth-session-census.md",
    "ledgers/deserialization-archive-census.md",
    "ledgers/crypto-census.md",
    "ledgers/h-ledger.md",
    "ledgers/m-ledger.md",
    "ledgers/f-ledger.md",
    "ledgers/claim-ledger.md",
    "ledgers/negative-claims.md",
    "ledgers/coverage-gaps.md",
    "ledgers/protocol-completion.md",
    "ledgers/defense-ledger.md",
    "evidence/repo_intelligence_brief.md",
    "evidence/compiled_audit_prompt.md",
    "evidence/source-snippets.md",
    "evidence/tool-health.md",
    "evidence/coverage_governance.md",
    "evidence/open_coverage_gaps.md",
    "evidence/rootcause_dedup.md",
    "evidence/unsupported_surfaces.md",
    "evidence/defense_verification.md",
]

REQUIRED_CLOSEOUT_ROWS = [
    "scope and commit pinned",
    "RubberDuck CI semantic full completed with `detailed_repo_analysis(..., semantic_mode=\"full\")`",
    "semantic source loaded or post-CI unsupported/degraded status documented",
    "full file inventory and deterministic sink census completed",
    "all privileged census rows triaged or blocked with evidence",
    "route/file and API-response/file matrices completed",
    "coverage governance written and open gaps classified",
    "impossible zero-file/zero-node tool states ruled out or documented",
    "Repo Intelligence Brief written",
    "repo-specific audit prompt compiled",
    "capability graph written",
    "universal baseline sweeps run",
    "selected specialist playbooks run",
    "unsupported and uncovered surfaces routed",
    "critical-surface coverage plan executed or gap recorded",
    "negative claims backed by search/scope evidence",
    "prior-run candidates reconciled",
    "High/Critical prior-reviewed downgrades have dedicated downgrade notes or preserve prior severity",
    "per-finding protocol matrix completed or exceptions documented",
    "P0/P1 Tier-2 attempted or blocker documented",
    "important defenses validated and bypass-checked",
    "root-cause variants preserved",
    "final claims pass claim firewall",
    "exhaustive completion checker passed or report marked incomplete",
]

REQUIRED_PROTOCOL_TERMS = [
    "read_source",
    "control_guards",
    "call_chain",
    "def_sites",
    "trace_variable",
    "simulate_paths",
    "infer_intent",
    "explain_finding",
    "get_evidence_pack",
]

PLACEHOLDER_RE = re.compile(r"^\s*(?:placeholder|tbd|todo|n/?a|none|-+|not\s+run|missing)\s*$", re.I)
BAD_CONTENT_RE = re.compile(r"\b(?:TBD|TODO|PLACEHOLDER)\b", re.I)
COMPLETE_STATUSES = {"complete", "complete-with-accepted-gaps"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_complete_status(report: str) -> bool:
    return bool(
        re.search(r"audit status\s*\|?\s*complete\b", report, re.I)
        or re.search(r"audit status:\s*complete\b", report, re.I)
    )


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def row_cells(line: str) -> list[str]:
    if "|" not in line:
        return []
    cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
    if cells and all(re.fullmatch(r":?-+:?", c) for c in cells):
        return []
    return cells


def row_status(line: str) -> str | None:
    for cell in row_cells(line):
        value = cell.lower()
        if value in COMPLETE_STATUSES:
            return value
    match = re.search(r"\bstatus\s*[:=]\s*(complete-with-accepted-gaps|complete)\b", line, re.I)
    return match.group(1).lower() if match else None


def evidence_refs(line: str) -> list[str]:
    refs = re.findall(
        r"(?:^|[\s|`])((?:evidence|ledgers|logs)/[A-Za-z0-9._/-]+|SCOPE\.md|TRACE\.md|REPORT\.md)(?=$|[\s|`:,;.)])",
        line,
    )
    return [r.rstrip(".,;:)") for r in refs]


def is_substantive_file(root: Path, rel_path: str) -> bool:
    text = read(root / rel_path)
    stripped = text.strip()
    if len(stripped) < 20:
        return False
    if PLACEHOLDER_RE.fullmatch(stripped):
        return False
    if BAD_CONTENT_RE.search(stripped):
        return False
    return True


def matching_line(protocol: str, item: str) -> str | None:
    target = normalize(item)
    candidates: list[str] = []
    for line in protocol.splitlines():
        if target and target in normalize(line):
            candidates.append(line)
    if not candidates:
        return None
    for line in candidates:
        if row_status(line) or evidence_refs(line):
            return line
    return candidates[0]


def validate_scope(root: Path, report: str, errors: list[str]) -> None:
    scope = read(root / "SCOPE.md")
    if not is_substantive_file(root, "SCOPE.md"):
        errors.append("SCOPE.md is missing, too short, or placeholder-like")
        return
    if not re.search(r"\b[0-9a-f]{12,40}\b", scope, re.I):
        errors.append("SCOPE.md does not contain a pinned commit hash")
    if not re.search(r"\b[0-9a-f]{12,40}\b", report, re.I):
        errors.append("REPORT.md does not contain a pinned commit hash")


def validate_required_rows(root: Path, protocol: str) -> list[str]:
    errors: list[str] = []
    for item in REQUIRED_CLOSEOUT_ROWS:
        line = matching_line(protocol, item)
        if not line:
            errors.append(f"Protocol-completion matrix missing required row: {item}")
            continue
        status = row_status(line)
        if status not in COMPLETE_STATUSES:
            errors.append(f"Protocol row has no acceptable complete status: {item}")
        refs = evidence_refs(line)
        if not refs:
            errors.append(f"Protocol row has no evidence file pointer: {item}")
            continue
        if not any((root / ref).exists() and is_substantive_file(root, ref) for ref in refs):
            errors.append(f"Protocol row evidence is missing or placeholder-like: {item}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)

    report = read(root / "REPORT.md")
    protocol = read(root / "ledgers" / "protocol-completion.md")
    coverage = read(root / "evidence" / "open_coverage_gaps.md") + "\n" + read(root / "ledgers" / "coverage-gaps.md")
    says_complete = has_complete_status(report)
    errors: list[str] = []

    missing = [p for p in RECOMMENDED if not (root / p).exists()]
    partial_ok = any(s in report.lower() for s in [
        "targeted",
        "draft",
        "partial",
        "runtime-validation incomplete",
        "tooling-blocked",
        "post-CI source-confirmed",
        "complete-with-accepted-gaps",
    ])

    if missing:
        print("Recommended evidence-pack files missing:")
        for p in missing:
            print(f" - {p}")
        if not partial_ok:
            errors.append("Missing recommended evidence files but report is not marked targeted/post-CI partial/blocked.")
        print("Allowed only because report is marked targeted/post-CI partial/blocked.")

    if protocol:
        missing_terms = [
            t for t in REQUIRED_PROTOCOL_TERMS
            if t not in protocol and t not in report
        ]
        if missing_terms:
            print("Protocol-completion matrix missing tool/status terms:")
            for t in missing_terms:
                print(f" - {t}")
            errors.append("Required per-finding validation terms are missing from the protocol matrix.")
        if says_complete:
            errors.extend(validate_required_rows(root, protocol))
    elif says_complete:
        errors.append("Report claims Complete but ledgers/protocol-completion.md is missing.")

    if says_complete:
        validate_scope(root, report, errors)

    has_blocking_gap = (
        re.search(r"blocks complete\?\s*\|?.*(yes|true|blocking)", coverage, re.I)
        or re.search(r"open coverage gaps", coverage, re.I)
        or re.search(r"\bnot covered\b", coverage, re.I)
    )
    if has_blocking_gap and says_complete and "complete-with-accepted-gaps" not in report.lower():
        errors.append("Report claims Complete while open/blocking coverage gaps are present.")

    if errors:
        print("ERROR: evidence-pack/protocol completion check failed.")
        for error in errors:
            print(f" - {error}")
        return 2

    print("OK: evidence-pack/protocol completion check passed or acceptable partial status documented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
