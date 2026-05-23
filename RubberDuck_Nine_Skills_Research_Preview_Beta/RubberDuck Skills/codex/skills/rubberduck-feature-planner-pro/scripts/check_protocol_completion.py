#!/usr/bin/env python3
from pathlib import Path
import argparse, sys

REQUIRED = ["Fit Pack", "Where This Feature Belongs", "Tests", "Acceptance Criteria", "Signoff"]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("plan_md")
    args=ap.parse_args()
    txt=Path(args.plan_md).read_text(errors="replace")
    missing=[x for x in REQUIRED if x.lower() not in txt.lower()]
    if missing:
        print("FAIL: missing protocol sections")
        for m in missing: print(" -", m)
        sys.exit(2)
    if "production code" in txt.lower() and "no production code" not in txt.lower():
        print("WARN: verify PLAN did not generate production code")
    print("OK: Feature Planner protocol completion present")
if __name__=="__main__":
    main()
