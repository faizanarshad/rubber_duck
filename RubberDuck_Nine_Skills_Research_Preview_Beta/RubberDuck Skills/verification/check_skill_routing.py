#!/usr/bin/env python3
"""Deterministic routing checks for the RubberDuck nine-skill bundle."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROUTING_CASES = [
    ("Get to know this repo and map the architecture.", "rubberduck-codebase-atlas-pro"),
    ("Run a security audit of this repository.", "rubberduck-security-audit"),
    ("What breaks if I modify this function?", "rubberduck-change-impact-pro"),
    ("Find duplicate behavior or duplicate intent in this repo.", "rubberduck-doppelganger-hunt-pro"),
    ("Can I replace this implementation with that one?", "rubberduck-mirror-pro"),
    ("Find drift between DB schema, code types, and API contracts.", "rubberduck-schema-code-api-drift-pro"),
    ("Plan tests first for this feature.", "rubberduck-feature-planner-pro"),
    ("Build from this sealed_plan.json.", "rubberduck-feature-builder-pro"),
    ("Run plan and build under this autonomy envelope.", "rubberduck-autonomous-feature-mode"),
]


DOCS = [
    "ROUTING_DECISION.md",
    "codex/AGENTS_SNIPPET.md",
    "claude-code/CLAUDE.md_SNIPPET.md",
    "cursor/AGENTS.md_SNIPPET.md",
]


PRECEDENCE_MARKERS = [
    ("sealed_plan.json", "rubberduck-feature-builder-pro"),
    ("autonomy envelope", "rubberduck-autonomous-feature-mode"),
    ("equivalence", "rubberduck-mirror-pro"),
    ("duplicate intent", "rubberduck-doppelganger-hunt-pro"),
    ("schema", "rubberduck-schema-code-api-drift-pro"),
    ("security audit", "rubberduck-security-audit"),
    ("change impact", "rubberduck-change-impact-pro"),
    ("tests-first", "rubberduck-feature-planner-pro"),
    ("architecture", "rubberduck-codebase-atlas-pro"),
]


def route_prompt(prompt: str) -> str | None:
    text = prompt.casefold()

    has_build = any(term in text for term in ["build", "implement", "implementation", "production code"])
    if "sealed_plan.json" in text and has_build:
        return "rubberduck-feature-builder-pro"

    if any(term in text for term in ["autonomy envelope", "autonomous", "auto mode", "plan and build"]):
        return "rubberduck-autonomous-feature-mode"

    if any(term in text for term in ["equivalent", "equivalence", "replace", "replacement", "refactor preserves", "behavior drift", "before/after"]):
        return "rubberduck-mirror-pro"

    if any(term in text for term in ["duplicate intent", "duplicate behavior", "behavior twins", "doppelganger", "semantic duplicate"]):
        return "rubberduck-doppelganger-hunt-pro"

    if any(term in text for term in ["schema", "api contract", "code types", "db ", "database", "nullability", "generated client", "validation drift"]):
        return "rubberduck-schema-code-api-drift-pro"

    if any(term in text for term in ["security audit", "vulnerability", "pentest", "cwe", "cve", "scanner finding", "defensible security"]):
        return "rubberduck-security-audit"

    if any(term in text for term in ["what breaks", "modify this function", "change impact", "blast radius", "callers", "callees", "tests to run", "safe change order"]):
        return "rubberduck-change-impact-pro"

    if any(term in text for term in ["plan tests first", "tests first", "tests-first", "feature planning", "sealed plan", "signoff-ready"]):
        return "rubberduck-feature-planner-pro"

    if any(term in text for term in ["get to know", "map the architecture", "architecture", "entry points", "call chains", "data flow", "onboarding", "codebase atlas"]):
        return "rubberduck-codebase-atlas-pro"

    return None


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Extracted package root")
    parser.add_argument("--write", default="", help="Optional path to write JSON results")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures: list[str] = []
    cases = []

    for prompt, expected in ROUTING_CASES:
        actual = route_prompt(prompt)
        ok = actual == expected
        cases.append({"prompt": prompt, "expected": expected, "actual": actual, "passed": ok})
        if not ok:
            failures.append(f"routing mismatch for {prompt!r}: expected {expected}, got {actual}")

    for doc in DOCS:
        path = root / doc
        if not path.exists():
            failures.append(f"missing routing doc/snippet: {doc}")
            continue
        text = read(path).casefold()
        for marker, skill in PRECEDENCE_MARKERS:
            if marker.casefold() not in text:
                failures.append(f"{doc} missing routing marker {marker!r}")
            if skill.casefold() not in text:
                failures.append(f"{doc} missing skill reference {skill}")

    results = {"cases": cases, "failures": failures, "tests_run": len(cases)}
    if args.write:
        out = Path(args.write)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps({"tests_run": len(cases), "failures": len(failures)}, indent=2))
    if failures:
        print("FAILURES:")
        for failure in failures:
            print(f" - {failure}")
        return 2
    print("OK: skill routing checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

