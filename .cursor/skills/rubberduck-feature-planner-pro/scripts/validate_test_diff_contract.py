#!/usr/bin/env python3
from pathlib import Path
import argparse, sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("test_diff")
    args=ap.parse_args()
    txt=Path(args.test_diff).read_text(errors="replace")
    errors=[]
    if "diff --git" not in txt and "--- " not in txt:
        errors.append("not a recognizable diff")
    if not any(token in txt.lower() for token in ["test", "assert", "expect", "pytest", "unittest"]):
        errors.append("diff does not appear to contain tests")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: test_diff contract looks tests-first")
if __name__=="__main__":
    main()
