#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("audit")
    args=ap.parse_args()
    data=json.loads(Path(args.audit).read_text())
    records=data if isinstance(data,list) else data.get("iterations",[])
    errors=[]
    if not records:
        errors.append("audit has no iteration records")
    for i,r in enumerate(records):
        for k in ["iteration","action","heartbeat_snapshot"]:
            if k not in r:
                errors.append(f"record {i} missing {k}")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: audit log validates")
if __name__=="__main__":
    main()
