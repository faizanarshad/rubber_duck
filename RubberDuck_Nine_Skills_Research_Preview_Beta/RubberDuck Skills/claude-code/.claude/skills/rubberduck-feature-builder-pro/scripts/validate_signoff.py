#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, sys

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("sealed_plan")
    ap.add_argument("signoff")
    args=ap.parse_args()
    errors=[]
    if not Path(args.sealed_plan).exists():
        errors.append("sealed plan file missing")
    if not Path(args.signoff).exists():
        errors.append("SIGNOFF.json or AUTO_AUTHORIZATION.json missing")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    plan_hash=sha(args.sealed_plan)
    data=json.loads(Path(args.signoff).read_text())
    if data.get("sealed_plan_sha256") != plan_hash:
        errors.append("sealed_plan_sha256 mismatch")
    if not (data.get("approved") or data.get("authorized")):
        errors.append("signoff/authorization not approved")
    if data.get("invoked_under") not in ["USER","AUTO_MODE"]:
        errors.append("invoked_under must be USER or AUTO_MODE")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: signoff/authorization validates sealed plan hash")
if __name__=="__main__":
    main()
