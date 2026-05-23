#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

REQUIRED = [
    "schema_version","plan_type","repo","base_commit","feature_title","feature_description",
    "session_id","fit_pack_id","planned_files","off_limits_files","reusable_symbols",
    "existing_patterns","acceptance_criteria","test_plan","test_diff_path","effect_manifest",
    "command_plan","generation_constraints","negative_scope","tool_health","sealed_at","plan_sha256"
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("sealed_plan")
    args=ap.parse_args()
    data=json.loads(Path(args.sealed_plan).read_text())
    missing=[k for k in REQUIRED if k not in data]
    errors=[]
    if missing: errors.append(f"missing fields: {missing}")
    if "user_signoff_received" in data:
        errors.append("sealed_plan contains mutable user_signoff_received; use SIGNOFF.json")
    if data.get("plan_type") not in ["FEATURE_PLAN", "TESTS_FIRST_FEATURE_PLAN"]:
        errors.append("plan_type must be FEATURE_PLAN or TESTS_FIRST_FEATURE_PLAN")
    if not data.get("acceptance_criteria"):
        errors.append("acceptance_criteria empty")
    if errors:
        print("FAIL")
        [print(" -", e) for e in errors]
        sys.exit(2)
    print("OK: sealed_plan contract validated")
if __name__=="__main__":
    main()
