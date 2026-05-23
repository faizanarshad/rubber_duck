#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("sealed_plan")
    ap.add_argument("auth_json")
    args=ap.parse_args()
    errors=[]
    if not Path(args.sealed_plan).exists():
        errors.append("sealed plan file missing")
    if not Path(args.auth_json).exists():
        errors.append("SIGNOFF.json or AUTO_AUTHORIZATION.json missing")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    plan=json.loads(Path(args.sealed_plan).read_text())
    auth=json.loads(Path(args.auth_json).read_text())
    for key in ["repo","base_commit","planned_files","off_limits_files","acceptance_criteria","test_diff_path"]:
        if key not in plan:
            errors.append(f"sealed plan missing {key}")
    if "user_signoff_received" in plan:
        errors.append("sealed plan contains mutable signoff state")
    if auth.get("invoked_under") not in ["USER","AUTO_MODE"]:
        errors.append("auth invoked_under invalid")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: build inputs valid")
if __name__=="__main__":
    main()
