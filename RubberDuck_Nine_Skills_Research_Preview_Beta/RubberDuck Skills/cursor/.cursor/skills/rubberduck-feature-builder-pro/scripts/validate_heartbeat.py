#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

BLOCKING = {"RED","BLOCKED","YELLOW_UNACKED"}
PASSING = {"GREEN","YELLOW_ACCEPTED","NOT_APPLICABLE"}
VALID = BLOCKING | PASSING | {"UNAVAILABLE"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("heartbeat")
    args=ap.parse_args()
    data=json.loads(Path(args.heartbeat).read_text())
    errors=[]
    dims=data.get("dimensions",{})
    if not dims:
        errors.append("dimensions empty")
    for name,d in dims.items():
        st=d.get("status")
        if st not in VALID:
            errors.append(f"{name}: invalid status {st}")
        if st=="GREEN" and not d.get("evidence"):
            errors.append(f"{name}: GREEN without evidence")
    if data.get("all_green") and any(d.get("status") in BLOCKING or d.get("status")=="UNAVAILABLE" for d in dims.values()):
        errors.append("all_green true with blocking/unavailable dimensions")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: heartbeat validates")
if __name__=="__main__":
    main()
