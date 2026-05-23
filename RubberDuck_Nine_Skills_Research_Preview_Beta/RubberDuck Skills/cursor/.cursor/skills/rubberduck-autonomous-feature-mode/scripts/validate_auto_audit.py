#!/usr/bin/env python3
from pathlib import Path
import argparse, fnmatch, json, sys

def off_limit_violations(data: dict) -> list[str]:
    envelope = data.get("autonomy_envelope", {})
    patterns = envelope.get("off_limits_file_globs", []) or []
    touched = data.get("files_touched") or data.get("builder", {}).get("files_touched") or []
    violations = []
    for path in touched:
        for pattern in patterns:
            if path == pattern or fnmatch.fnmatch(path, pattern):
                violations.append(path)
                break
    return violations

def security_delta_errors(data: dict) -> list[str]:
    errors: list[str] = []
    required = bool(data.get("security_delta_required") or data.get("autonomy_envelope", {}).get("security_delta_required"))
    security = data.get("security_delta") or data.get("builder", {}).get("security_delta") or {}
    status = security.get("status") or data.get("security_delta_status")
    allowed_complete = {"CLEAN_NO_NEW_CRITICAL_HIGH", "NEW_FINDINGS_ADJUDICATED"}
    blocked = {"BLOCKED_NEW_UNRESOLVED_FINDINGS", "NOT_RUN_LOCAL_ONLY"}
    if required and not status:
        errors.append("security_delta_required without security_delta.status")
        return errors
    if data.get("final_status") == "complete" and required and status not in allowed_complete:
        errors.append("complete final_status without clean/adjudicated security delta")
    if data.get("final_status") == "complete" and status in blocked:
        errors.append(f"complete final_status with blocked security delta: {status}")
    if status == "NEW_FINDINGS_ADJUDICATED":
        fixed = security.get("fixed_findings") or []
        adjudicated = security.get("adjudicated_false_positives") or []
        if not fixed and not adjudicated:
            errors.append("adjudicated security delta without fixed/adjudicated findings")
    if security.get("unresolved_blockers") and data.get("final_status") == "complete":
        errors.append("complete final_status with security_delta.unresolved_blockers")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("auto_audit")
    args=ap.parse_args()
    data=json.loads(Path(args.auto_audit).read_text())
    errors=[]
    for k in ["autonomy_envelope","planner","sealed_plan_sha256","builder","final_status"]:
        if k not in data:
            errors.append(f"missing {k}")
    if data.get("final_status") == "complete" and not data.get("builder",{}).get("validation_passed"):
        errors.append("complete final_status without builder.validation_passed")
    if data.get("final_status") == "complete" and data.get("planner",{}).get("status") != "complete":
        errors.append("complete final_status without planner.status complete")
    errors.extend(security_delta_errors(data))
    for path in off_limit_violations(data):
        errors.append(f"off-limits file touched: {path}")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: auto audit validates")
if __name__=="__main__":
    main()
