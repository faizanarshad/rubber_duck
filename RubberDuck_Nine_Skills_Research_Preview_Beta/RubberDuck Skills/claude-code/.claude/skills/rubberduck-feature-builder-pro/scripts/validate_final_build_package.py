#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse, fnmatch, json, sys

REQUIRED = ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json"]
LABELS = [
    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
    "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
    "Validation status: BLOCKED_BEFORE_REPO_BACKED_VALIDATION",
]
FULL_LABEL = LABELS[0]
LOCAL_PENDING_LABEL = LABELS[1]
BLOCKED_LABEL = LABELS[2]
SECURITY_LABELS = [
    "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
    "Security delta status: NEW_FINDINGS_ADJUDICATED",
    "Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS",
    "Security delta status: NOT_RUN_LOCAL_ONLY",
]
SECURITY_CLEAN_LABEL = SECURITY_LABELS[0]
SECURITY_ADJUDICATED_LABEL = SECURITY_LABELS[1]
SECURITY_BLOCKED_LABEL = SECURITY_LABELS[2]
SECURITY_LOCAL_ONLY_LABEL = SECURITY_LABELS[3]

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def validation_has_pass(data) -> bool:
    if isinstance(data, dict):
        for key in ["final_verdict", "verdict", "status", "result"]:
            if str(data.get(key, "")).upper() == "PASS":
                return True
        return any(validation_has_pass(v) for v in data.values())
    if isinstance(data, list):
        return any(validation_has_pass(v) for v in data)
    return False

def extract_paths(items) -> list[str]:
    paths: list[str] = []
    if isinstance(items, list):
        for item in items:
            if isinstance(item, str):
                paths.append(item)
            elif isinstance(item, dict) and item.get("path"):
                paths.append(str(item["path"]))
    return paths

def violates_off_limits(root: Path) -> list[str]:
    changed = extract_paths(load_json(root / "changed-files.json"))
    if not changed:
        return []
    plan = load_json(root / "sealed_plan.json") or {}
    off_limits = extract_paths(plan.get("off_limits_files"))
    off_limits += extract_paths(load_json(root / "off-limits-files.json"))
    violations = []
    for path in changed:
        for pattern in off_limits:
            if path == pattern or fnmatch.fnmatch(path, pattern):
                violations.append(path)
                break
    return violations

def selected_label(text: str) -> str | None:
    present = [label for label in LABELS if label in text]
    if len(present) != 1:
        return None
    return present[0]

def selected_security_label(text: str) -> str | None:
    present = [label for label in SECURITY_LABELS if label in text]
    if len(present) != 1:
        return None
    return present[0]

def evidence_contains(path: Path, markers: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing {path.name}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    missing = []
    for marker in markers:
        if marker.lower() not in lowered:
            missing.append(f"{path.name} missing {marker!r}")
    return missing

def repo_backed_evidence_failures(root: Path) -> list[str]:
    evidence = root / "evidence"
    failures: list[str] = []
    failures += evidence_contains(
        evidence / "github-publish.md",
        ["branch", "commit", "pushed remote", "staged file", "secret-scan"],
    )
    failures += evidence_contains(
        evidence / "repo-backed-rubberduck-validation.md",
        ["detailed_repo_analysis", "semantic_mode=\"full\"", "repo", "branch", "commit", "indexing status", "validation"],
    )
    failures += evidence_contains(
        evidence / "indexed-files-coverage.md",
        ["changed files", "new files", "loaded", "coverage"],
    )
    return failures

def severity_is_critical_high(finding: dict) -> bool:
    return str(finding.get("severity", "")).upper() in {"CRITICAL", "HIGH"}

def finding_status(finding: dict) -> str:
    return str(finding.get("status", "")).upper()

def changed_code_finding(finding: dict) -> bool:
    if "in_changed_code" in finding:
        return bool(finding.get("in_changed_code"))
    if "changed_code" in finding:
        return bool(finding.get("changed_code"))
    return True

def unresolved_critical_high(findings) -> list[dict]:
    unresolved = []
    if not isinstance(findings, list):
        return unresolved
    resolved_statuses = {
        "FIXED",
        "ADJUDICATED_FALSE_POSITIVE",
        "FALSE_POSITIVE",
        "PRE_EXISTING",
        "ACCEPTED",
    }
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        if severity_is_critical_high(finding) and changed_code_finding(finding) and finding_status(finding) not in resolved_statuses:
            unresolved.append(finding)
    return unresolved

def security_delta_evidence_failures(root: Path, security_label: str, build_text: str) -> list[str]:
    if security_label == SECURITY_LOCAL_ONLY_LABEL:
        return []
    evidence = root / "evidence"
    failures: list[str] = []
    for filename in [
        "security-baseline-rubberduck.md",
        "security-pr-head-rubberduck.md",
        "security-delta.md",
        "security-fix-loop-history.json",
        "finding-adjudication.json",
    ]:
        if not (evidence / filename).exists():
            failures.append(f"missing {filename}")
    delta = load_json(evidence / "security-delta.json")
    if not isinstance(delta, dict):
        failures.append("missing or invalid security-delta.json")
        return failures
    for key in ["base", "head", "new_findings", "pre_existing_findings", "fixed_findings", "adjudicated_false_positives", "unresolved_blockers"]:
        if key not in delta:
            failures.append(f"security-delta.json missing {key}")
    if failures:
        return failures
    unresolved_blockers = delta.get("unresolved_blockers") or []
    unresolved_new = unresolved_critical_high(delta.get("new_findings"))
    if security_label == SECURITY_CLEAN_LABEL:
        if unresolved_blockers:
            failures.append("CLEAN security delta has unresolved_blockers")
        if unresolved_new:
            failures.append("CLEAN security delta has unresolved new Critical/High findings")
    if security_label == SECURITY_ADJUDICATED_LABEL:
        if unresolved_blockers:
            failures.append("ADJUDICATED security delta has unresolved_blockers")
        if unresolved_new:
            failures.append("ADJUDICATED security delta has unresolved new Critical/High findings")
        if not (delta.get("fixed_findings") or delta.get("adjudicated_false_positives")):
            failures.append("ADJUDICATED security delta requires fixed or adjudicated findings")
    if security_label == SECURITY_BLOCKED_LABEL:
        if not (unresolved_blockers or unresolved_new):
            failures.append("BLOCKED security delta requires unresolved blockers or unresolved new Critical/High findings")
    pre_existing = delta.get("pre_existing_findings") or []
    if pre_existing and "repo is clean" in build_text.lower():
        failures.append("BUILD.md claims repo is clean while pre_existing_findings are present")
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("build_dir")
    args=ap.parse_args()
    root=Path(args.build_dir)
    missing=[p for p in REQUIRED if not (root/p).exists()]
    if missing:
        print("FAIL: missing build artifacts")
        for m in missing: print(" -", m)
        sys.exit(2)
    txt=(root/"BUILD.md").read_text(errors="replace")
    label = selected_label(txt)
    if not label:
        print("FAIL: BUILD.md must contain exactly one validation status label")
        for item in LABELS:
            print(" -", item)
        sys.exit(2)
    security_label = selected_security_label(txt)
    if not security_label:
        print("FAIL: BUILD.md must contain exactly one security delta status label")
        for item in SECURITY_LABELS:
            print(" -", item)
        sys.exit(2)
    lowered = txt.lower()
    if label != FULL_LABEL and (
        "fully rubberduck validated" in lowered
        or "fully repo-backed rubberduck validated" in lowered
        or "codebase intelligence phase 2 complete" in lowered
    ):
        print("FAIL: non-full validation label cannot claim full RubberDuck validation")
        sys.exit(2)
    if label == LOCAL_PENDING_LABEL and "repo-backed RubberDuck validation is pending" not in txt:
        print("FAIL: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING must state repo-backed RubberDuck validation is pending")
        sys.exit(2)
    if label == FULL_LABEL:
        evidence_failures = repo_backed_evidence_failures(root)
        if evidence_failures:
            print("FAIL: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED requires repo-backed evidence")
            for failure in evidence_failures:
                print(" -", failure)
            sys.exit(2)
        if security_label == SECURITY_LOCAL_ONLY_LABEL:
            print("FAIL: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED cannot use NOT_RUN_LOCAL_ONLY security delta")
            sys.exit(2)
    if label != LOCAL_PENDING_LABEL and security_label == SECURITY_LOCAL_ONLY_LABEL:
        print("FAIL: NOT_RUN_LOCAL_ONLY security delta is only valid for LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING")
        sys.exit(2)
    security_failures = security_delta_evidence_failures(root, security_label, txt)
    if security_failures:
        print("FAIL: security delta evidence/status invalid")
        for failure in security_failures:
            print(" -", failure)
        sys.exit(2)
    pr_ready_exists = (root/"PR_READY.diff").exists()
    if pr_ready_exists and security_label == SECURITY_BLOCKED_LABEL:
        print("FAIL: PR_READY.diff exists but security delta is blocked")
        sys.exit(2)
    if "PR-ready" in txt and security_label == SECURITY_BLOCKED_LABEL:
        print("FAIL: BUILD.md claims PR-ready but security delta is blocked")
        sys.exit(2)
    if "PR_READY.diff" in txt and not (root/"PR_READY.diff").exists():
        print("FAIL: BUILD.md references PR_READY.diff but file absent")
        sys.exit(2)
    if (root/"PR_READY.diff").exists():
        validation = load_json(root/"validation-history.json")
        if not validation_has_pass(validation):
            print("FAIL: PR_READY.diff exists but validation-history.json has no PASS verdict")
            sys.exit(2)
    off_limits = violates_off_limits(root)
    if off_limits:
        print("FAIL: off-limits files touched")
        for path in off_limits:
            print(" -", path)
        sys.exit(2)
    print("OK: final build package validates")
if __name__=="__main__":
    main()
