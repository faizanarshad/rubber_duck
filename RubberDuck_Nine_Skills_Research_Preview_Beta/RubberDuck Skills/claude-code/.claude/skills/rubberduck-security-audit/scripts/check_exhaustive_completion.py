#!/usr/bin/env python3
"""Check exhaustive census closure for Security Audit report bundles."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_LEDGERS = [
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
]

ALLOWED_DISPOSITIONS = {
    "promoted",
    "false-positive",
    "hardening",
    "expected-behavior",
    "fixed",
    "out-of-scope",
    "blocked",
}

INCOMPLETE_MARKERS = {
    "draft",
    "blocked",
    "incomplete",
    "tooling-blocked",
    "post-ci source-confirmed partial",
    "post-ci-source-confirmed-partial",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_complete_status(report: str) -> bool:
    return bool(
        re.search(r"audit status\s*\|?\s*complete\b", report, re.I)
        or re.search(r"audit status:\s*complete\b", report, re.I)
    )


def explicitly_incomplete(report: str) -> bool:
    low = report.lower()
    return any(marker in low for marker in INCOMPLETE_MARKERS)


def cells(line: str) -> list[str]:
    if not line.startswith("|") or line.startswith("|---"):
        return []
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def table_rows(text: str) -> list[tuple[int, list[str]]]:
    rows: list[tuple[int, list[str]]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        row = cells(line)
        if not row:
            continue
        if row[0].lower() in {"id", "file"}:
            continue
        rows.append((lineno, row))
    return rows


def disposition_and_evidence(row: list[str]) -> tuple[str, str]:
    if len(row) < 2:
        return "", ""
    return row[-2].strip().lower(), row[-1].strip()


def is_empty_row(row: list[str]) -> bool:
    joined = " ".join(row).lower()
    return "no matching rows found" in joined or row[0].lower() == "none"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    report = read(root / "REPORT.md")

    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_LEDGERS:
        path = root / rel
        if not path.exists():
            errors.append(f"Missing required census ledger: {rel}")
            continue
        if len(read(path).strip()) < 40:
            errors.append(f"Census ledger is empty or placeholder-like: {rel}")

    for rel in REQUIRED_LEDGERS:
        path = root / rel
        if not path.exists():
            continue
        text = read(path)
        for lineno, row in table_rows(text):
            if is_empty_row(row):
                continue
            disposition, evidence = disposition_and_evidence(row)
            if rel == "ledgers/file-inventory.md":
                # File inventory uses Status/Evidence, not exploit disposition.
                continue
            if disposition == "untriaged":
                errors.append(f"Untriaged census row: {rel}:{lineno}")
                continue
            if disposition not in ALLOWED_DISPOSITIONS:
                errors.append(f"Invalid census disposition '{disposition}' at {rel}:{lineno}")
                continue
            if not evidence:
                errors.append(f"Census row lacks evidence pointer: {rel}:{lineno}")

    p_ledger = read(root / "ledgers" / "p-ledger.md")
    if p_ledger:
        recognized = [
            "still-present",
            "fixed",
            "not-in-current-scope",
            "disproven",
            "merged-into-new-finding",
            "blocked",
            "promoted",
            "ruled out",
            "invalidated",
            "reproduced",
            "reused",
        ]
        if "prior" in (report + p_ledger).lower() and not any(term in p_ledger.lower() for term in recognized):
            errors.append("Prior-finding ledger exists but lacks recognized current statuses.")
        if "untriaged" in p_ledger.lower():
            errors.append("Prior-finding ledger contains untriaged entries.")
    elif "prior" in report.lower() and has_complete_status(report):
        warnings.append("Report mentions prior findings but ledgers/p-ledger.md is missing.")

    if errors:
        print("ERROR: exhaustive census completion check failed.")
        for error in errors[:100]:
            print(f" - {error}")
        if len(errors) > 100:
            print(f" - ... {len(errors) - 100} more errors omitted; triage the census ledgers for full detail.")
        if not has_complete_status(report) or explicitly_incomplete(report):
            print("Report appears non-complete/incomplete; failures document remaining work.")
        return 2

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f" - {warning}")
        if has_complete_status(report) and "complete-with-accepted-gaps" not in report.lower():
            print("ERROR: complete report has unresolved exhaustive warnings.")
            return 2

    print("OK: exhaustive census completion check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
