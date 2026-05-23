#!/usr/bin/env python3
"""Run all installation/runtime QA checks for the all-platform RubberDuck skills bundle.

This verifier is intentionally single-process: it executes skill structure/smoke
scripts with runpy instead of spawning dozens of nested Python processes. That
saves runtime in cloud/agent sandboxes and avoids repeated interpreter-startup
noise.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import runpy
import sys
from pathlib import Path


PLATFORMS = {
    "codex": Path("codex/skills"),
    "claude-code": Path("claude-code/.claude/skills"),
    "cursor": Path("cursor/.cursor/skills"),
}

SKILLS = [
    "rubberduck-codebase-atlas-pro",
    "rubberduck-security-audit",
    "rubberduck-change-impact-pro",
    "rubberduck-doppelganger-hunt-pro",
    "rubberduck-mirror-pro",
    "rubberduck-schema-code-api-drift-pro",
    "rubberduck-feature-planner-pro",
    "rubberduck-feature-builder-pro",
    "rubberduck-autonomous-feature-mode",
]

TOP_LEVEL_REQUIRED = [
    "README.md",
    "SETUP_PROMPT.md",
    "START_REPO_SESSION_PROMPT.md",
    "USE_PROMPTS.md",
    "RUBBERDUCK-CI-BOOTSTRAP.md",
    "RUBBERDUCK-RESPONSE-MARKER.md",
    "RUBBERDUCK-SKILL-ADVISOR.md",
    "RUBBERDUCK-SECURITY-DELTA-GATE.md",
    "ROUTING_DECISION.md",
    "INSTALL_CODEX.md",
    "INSTALL_CLAUDE_CODE.md",
    "INSTALL_CURSOR.md",
    "verification/PROTOCOL_EQUIVALENCE.md",
    "verification/check_skill_routing.py",
    "verification/verify_installed_skills.py",
    "verification/run_power_skill_synthetic_tests.py",
]

CURSOR_RULES = [
    "cursor/.cursor/rules/rubberduck-codebase-atlas-pro.mdc",
    "cursor/.cursor/rules/rubberduck-security-audit.mdc",
    "cursor/.cursor/rules/rubberduck-change-impact-pro.mdc",
    "cursor/.cursor/rules/rubberduck-doppelganger-hunt-pro.mdc",
    "cursor/.cursor/rules/rubberduck-mirror-pro.mdc",
    "cursor/.cursor/rules/rubberduck-schema-code-api-drift-pro.mdc",
    "cursor/.cursor/rules/rubberduck-feature-planner-pro.mdc",
    "cursor/.cursor/rules/rubberduck-feature-builder-pro.mdc",
    "cursor/.cursor/rules/rubberduck-autonomous-feature-mode.mdc",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def run_script(script: Path, argv: list[str], cwd: Path | None = None) -> dict:
    old_argv = sys.argv[:]
    old_path = sys.path[:]
    old_cwd = Path.cwd()
    out = io.StringIO()
    err = io.StringIO()
    exit_code = 0
    try:
        sys.argv = [str(script)] + argv
        sys.path.insert(0, str(script.parent))
        if cwd is not None:
            import os
            os.chdir(cwd)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as e:
                if isinstance(e.code, int):
                    exit_code = e.code
                elif e.code is None:
                    exit_code = 0
                else:
                    exit_code = 1
                    print(str(e.code), file=err)
    except Exception as e:
        exit_code = 99
        print(repr(e), file=err)
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
        if cwd is not None:
            import os
            os.chdir(old_cwd)
    return {"exit_code": exit_code, "stdout": out.getvalue(), "stderr": err.getvalue()}


def hash_dir(path: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(path.rglob("*")):
        if not p.is_file():
            continue
        if "__pycache__" in p.parts:
            continue
        rel = p.relative_to(path).as_posix()
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def safe_scan(root: Path) -> list[dict]:
    markers = [
        "__" + "MACOSX",
        ".DS" + "_Store",
        "/" + "Users/",
        "C:" + "\\\\" + "Users" + "\\\\",
        "/" + "home/" + "ec2-user/",
        "/" + "mnt/" + "data",
        "sandbox" + ":/",
        "file_" + "000",
        "expected " + "findings",
        "private " + "benchmark",
        "Bento" + "ML",
        "Trust" + "Claw",
        "trust" + "claw",
        "Composio" + "HQ",
        "hermes" + "-agent",
    ]
    hits = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if "__pycache__" in p.parts:
            continue
        # Skip generated verifier output files: failed prior runs may contain
        # marker strings from captured diagnostics. Packaged skill/docs/source
        # files and final zips are still scanned separately in QA.
        if p.name in {
            "deep_qa_results.json",
            "package_verification_results.json",
            "qa_run_all_checks.json",
            "routing_qa_results.json",
            "final_qa_results.json",
            "installed_codex_results.json",
            "installed_claude_results.json",
            "installed_cursor_results.json",
            "installed_codex_qa_results.json",
            "installed_claude_qa_results.json",
            "installed_cursor_qa_results.json",
        }:
            continue
        try:
            txt = read_text(p)
        except Exception:
            continue
        rel = p.relative_to(root).as_posix()
        for marker in markers:
            if marker in txt or marker in rel:
                hits.append({"file": rel, "marker": marker})
    return hits



def doc_sanity(root: Path) -> list[str]:
    """Check install/use docs reference every skill with exact usable paths."""
    failures: list[str] = []
    skills = SKILLS
    docs = {
        "README.md": read_text(root / "README.md") if (root / "README.md").exists() else "",
        "USE_PROMPTS.md": read_text(root / "USE_PROMPTS.md") if (root / "USE_PROMPTS.md").exists() else "",
        "INSTALL_CODEX.md": read_text(root / "INSTALL_CODEX.md") if (root / "INSTALL_CODEX.md").exists() else "",
        "INSTALL_CLAUDE_CODE.md": read_text(root / "INSTALL_CLAUDE_CODE.md") if (root / "INSTALL_CLAUDE_CODE.md").exists() else "",
        "INSTALL_CURSOR.md": read_text(root / "INSTALL_CURSOR.md") if (root / "INSTALL_CURSOR.md").exists() else "",
        "codex/AGENTS_SNIPPET.md": read_text(root / "codex/AGENTS_SNIPPET.md") if (root / "codex/AGENTS_SNIPPET.md").exists() else "",
        "claude-code/CLAUDE.md_SNIPPET.md": read_text(root / "claude-code/CLAUDE.md_SNIPPET.md") if (root / "claude-code/CLAUDE.md_SNIPPET.md").exists() else "",
        "cursor/AGENTS.md_SNIPPET.md": read_text(root / "cursor/AGENTS.md_SNIPPET.md") if (root / "cursor/AGENTS.md_SNIPPET.md").exists() else "",
    }
    for name, text in docs.items():
        if not text:
            failures.append(f"missing doc text: {name}")
            continue
        for skill in skills:
            if skill not in text:
                failures.append(f"doc {name} does not mention {skill}")

    cursor_doc = docs["INSTALL_CURSOR.md"]
    for skill in skills:
        exact_rule = f".cursor/rules/{skill}.mdc"
        exact_skill = f".cursor/skills/{skill}/SKILL.md"
        if exact_rule not in cursor_doc:
            failures.append(f"INSTALL_CURSOR.md missing exact rule path {exact_rule}")
        if exact_skill not in cursor_doc:
            failures.append(f"INSTALL_CURSOR.md missing exact skill path {exact_skill}")
    if "TARGET_REPO" not in cursor_doc:
        failures.append("INSTALL_CURSOR.md must use TARGET_REPO to avoid copying into the package root by mistake")
    if "--cursor-rules-root" not in cursor_doc:
        failures.append("INSTALL_CURSOR.md missing installed Cursor rules verifier flag")

    for fname in ["INSTALL_CODEX.md", "INSTALL_CLAUDE_CODE.md", "INSTALL_CURSOR.md"]:
        text = docs[fname]
        if "verify_installed_skills.py" not in text:
            failures.append(f"{fname} missing installed-target verifier command")
        if "run_all_checks.py" not in text:
            failures.append(f"{fname} missing package verifier command")

    return failures


def ci_bootstrap_sanity(root: Path) -> list[str]:
    """Enforce the mirror-first CI bootstrap contract across the package."""
    failures: list[str] = []
    bootstrap = root / "RUBBERDUCK-CI-BOOTSTRAP.md"
    if not bootstrap.exists():
        return ["missing RUBBERDUCK-CI-BOOTSTRAP.md"]

    text = read_text(bootstrap)
    required_markers = [
        "GitHub mirror",
        "gh repo create",
        "RubberDuck GitHub App",
        "detailed_repo_analysis",
        'semantic_mode="full"',
        "Codebase Intelligence Phase 2",
        "not a substitute",
        "post-CI fallback",
        "load_code",
        "instance_id",
        "max_files=2000",
    ]
    for marker in required_markers:
        if marker not in text:
            failures.append(f"RUBBERDUCK-CI-BOOTSTRAP.md missing marker: {marker}")

    docs = [
        "README.md",
        "START_REPO_SESSION_PROMPT.md",
        "USE_PROMPTS.md",
        "INSTALL_CODEX.md",
        "INSTALL_CLAUDE_CODE.md",
        "INSTALL_CURSOR.md",
        "codex/AGENTS_SNIPPET.md",
        "claude-code/CLAUDE.md_SNIPPET.md",
        "cursor/AGENTS.md_SNIPPET.md",
    ]
    for rel in docs:
        p = root / rel
        if not p.exists():
            failures.append(f"bootstrap doc check missing file: {rel}")
            continue
        doc_text = read_text(p)
        doc_lower = doc_text.lower()
        if "RUBBERDUCK-CI-BOOTSTRAP.md" not in doc_text:
            failures.append(f"{rel} does not reference RUBBERDUCK-CI-BOOTSTRAP.md")
        if "local indexing" not in doc_lower or "post-ci fallback" not in doc_lower:
            failures.append(f"{rel} does not preserve local-indexing fallback boundary")

    for platform, rel_root in PLATFORMS.items():
        for skill in SKILLS:
            skill_dir = root / rel_root / skill
            if not skill_dir.exists():
                continue
            skill_bootstrap = skill_dir / "RUBBERDUCK-CI-BOOTSTRAP.md"
            if not skill_bootstrap.exists():
                failures.append(f"missing skill bootstrap: {platform}:{skill}")
            elif skill_bootstrap.read_bytes() != bootstrap.read_bytes():
                failures.append(f"skill bootstrap differs from package bootstrap: {platform}:{skill}")

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill_text = read_text(skill_md)
                skill_lower = skill_text.lower()
                if "RUBBERDUCK-CI-BOOTSTRAP.md" not in skill_text:
                    failures.append(f"SKILL.md missing bootstrap gate: {platform}:{skill}")
                if "local-only" not in skill_text or "authorized GitHub" not in skill_text:
                    failures.append(f"SKILL.md missing mirror trigger language: {platform}:{skill}")
                if "local indexing" not in skill_lower or "post-ci fallback" not in skill_lower:
                    failures.append(f"SKILL.md missing post-CI local fallback boundary: {platform}:{skill}")
                if "local/repo" in skill_text:
                    failures.append(f"SKILL.md uses local/repo as primary repo placeholder: {platform}:{skill}")

            workflow = skill_dir / "RUBBERDUCK-WORKFLOW.md"
            if workflow.exists():
                workflow_text = read_text(workflow)
                workflow_lower = workflow_text.lower()
                if "RUBBERDUCK-CI-BOOTSTRAP.md" not in workflow_text:
                    failures.append(f"workflow missing bootstrap gate: {platform}:{skill}")
                if "local indexing" not in workflow_lower or "not a substitute for codebase intelligence phase 2" not in workflow_lower:
                    failures.append(f"workflow missing post-CI fallback boundary: {platform}:{skill}")
                if "local/repo" in workflow_text:
                    failures.append(f"workflow uses local/repo as primary repo placeholder: {platform}:{skill}")

    for rel in CURSOR_RULES:
        rule = root / rel
        if not rule.exists():
            continue
        rule_text = read_text(rule)
        if "RUBBERDUCK-CI-BOOTSTRAP.md" not in rule_text:
            failures.append(f"Cursor rule missing bootstrap reference: {rel}")
        rule_lower = rule_text.lower()
        if "local indexing" not in rule_lower or "post-ci fallback" not in rule_lower:
            failures.append(f"Cursor rule missing local-indexing boundary: {rel}")

    return failures


def has_wrong_duck_name(text: str) -> bool:
    lowered = text.lower()
    compact = "robot" + "duck"
    spaced = "robot" + " " + "duck"
    return compact in lowered or spaced in lowered


def response_marker_sanity(root: Path) -> list[str]:
    """Enforce the RubberDuck response marker contract across the package."""
    failures: list[str] = []
    marker = root / "RUBBERDUCK-RESPONSE-MARKER.md"
    if not marker.exists():
        return ["missing RUBBERDUCK-RESPONSE-MARKER.md"]

    marker_text = read_text(marker)
    marker_lower = marker_text.lower()
    for required in ["🦆", "RubberDuck", "first visible character"]:
        if required not in marker_text:
            failures.append(f"RUBBERDUCK-RESPONSE-MARKER.md missing marker: {required}")
    if has_wrong_duck_name(marker_lower):
        failures.append("RUBBERDUCK-RESPONSE-MARKER.md contains wrong duck-name wording")

    docs = [
        "README.md",
        "START_REPO_SESSION_PROMPT.md",
        "USE_PROMPTS.md",
        "RESEARCH_PREVIEW.md",
        "codex/AGENTS_SNIPPET.md",
        "claude-code/CLAUDE.md_SNIPPET.md",
        "cursor/AGENTS.md_SNIPPET.md",
    ]
    for rel in docs:
        p = root / rel
        if not p.exists():
            failures.append(f"response marker doc check missing file: {rel}")
            continue
        doc_text = read_text(p)
        doc_lower = doc_text.lower()
        if "RUBBERDUCK-RESPONSE-MARKER.md" not in doc_text:
            failures.append(f"{rel} does not reference RUBBERDUCK-RESPONSE-MARKER.md")
        if "🦆" not in doc_text:
            failures.append(f"{rel} does not include duck response marker")
        if has_wrong_duck_name(doc_lower):
            failures.append(f"{rel} contains wrong duck-name wording")

    for platform, rel_root in PLATFORMS.items():
        for skill in SKILLS:
            skill_dir = root / rel_root / skill
            if not skill_dir.exists():
                continue
            skill_marker = skill_dir / "RUBBERDUCK-RESPONSE-MARKER.md"
            if not skill_marker.exists():
                failures.append(f"missing skill response marker: {platform}:{skill}")
            elif skill_marker.read_bytes() != marker.read_bytes():
                failures.append(f"skill response marker differs from package marker: {platform}:{skill}")

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill_text = read_text(skill_md)
                skill_lower = skill_text.lower()
                if "RUBBERDUCK-RESPONSE-MARKER.md" not in skill_text:
                    failures.append(f"SKILL.md missing response marker reference: {platform}:{skill}")
                if "🦆" not in skill_text:
                    failures.append(f"SKILL.md missing duck response marker: {platform}:{skill}")
                if has_wrong_duck_name(skill_lower):
                    failures.append(f"SKILL.md contains wrong duck-name wording: {platform}:{skill}")

    for rel in CURSOR_RULES:
        rule = root / rel
        if not rule.exists():
            continue
        rule_text = read_text(rule)
        rule_lower = rule_text.lower()
        if "RUBBERDUCK-RESPONSE-MARKER.md" not in rule_text:
            failures.append(f"Cursor rule missing response marker reference: {rel}")
        if "🦆" not in rule_text:
            failures.append(f"Cursor rule missing duck response marker: {rel}")
        if has_wrong_duck_name(rule_lower):
            failures.append(f"Cursor rule contains wrong duck-name wording: {rel}")

    return failures


def skill_advisor_sanity(root: Path) -> list[str]:
    """Enforce the multi-skill advisor contract across the package."""
    failures: list[str] = []
    advisor = root / "RUBBERDUCK-SKILL-ADVISOR.md"
    setup = root / "SETUP_PROMPT.md"
    start = root / "START_REPO_SESSION_PROMPT.md"
    if not advisor.exists():
        return ["missing RUBBERDUCK-SKILL-ADVISOR.md"]
    if not setup.exists():
        failures.append("missing SETUP_PROMPT.md")
    if not start.exists():
        failures.append("missing START_REPO_SESSION_PROMPT.md")

    text = read_text(advisor)
    setup_text = read_text(setup) if setup.exists() else ""
    start_text = read_text(start) if start.exists() else ""
    required_markers = [
        "I need help from the RubberDuck Advisor.",
        "RubberDuck Skill Recommendation",
        "review each phase",
        "planning",
        "signoff",
        "Autonomous mode",
        "explicit envelope",
        "Local build only",
        "GitHub-validated build, step-by-step",
        "GitHub-validated build, autonomous bounded",
        "LOCAL_BUILD_ONLY",
        "GITHUB_VALIDATED_BUILD",
        "AUTO_GITHUB_VALIDATED_BUILD",
        "rubberduck-codebase-atlas-pro",
        "rubberduck-feature-planner-pro",
        "rubberduck-feature-builder-pro",
        "rubberduck-autonomous-feature-mode",
        "Please approve A, B, or C",
    ]
    for marker in required_markers:
        if marker not in text:
            failures.append(f"RUBBERDUCK-SKILL-ADVISOR.md missing marker: {marker}")
    for marker in [
        "You are installing the RubberDuck Nine Skills Research Preview Beta package",
        "Source package:",
        "verification/run_all_checks.py",
        "verification/verify_installed_skills.py",
        "TARGET_REPO",
        "Do not run RubberDuck analysis during installation",
        "START_REPO_SESSION_PROMPT.md",
        "I need help from the RubberDuck Advisor.",
    ]:
        if marker not in setup_text:
            failures.append(f"SETUP_PROMPT.md missing marker: {marker}")
    for marker in [
        "I need help from the RubberDuck Advisor.",
        "Use the RubberDuck Skill Advisor",
        "RUBBERDUCK-SKILL-ADVISOR.md",
        "RUBBERDUCK-CI-BOOTSTRAP.md",
        "RUBBERDUCK-SECURITY-DELTA-GATE.md",
        "GitHub-validated build",
        "Security Delta Gate",
        "Do not start a long multi-skill workflow",
    ]:
        if marker not in start_text:
            failures.append(f"START_REPO_SESSION_PROMPT.md missing marker: {marker}")

    docs = [
        "README.md",
        "START_REPO_SESSION_PROMPT.md",
        "USE_PROMPTS.md",
        "RESEARCH_PREVIEW.md",
        "codex/AGENTS_SNIPPET.md",
        "claude-code/CLAUDE.md_SNIPPET.md",
        "cursor/AGENTS.md_SNIPPET.md",
    ]
    for rel in docs:
        p = root / rel
        if not p.exists():
            failures.append(f"skill advisor doc check missing file: {rel}")
            continue
        doc_text = read_text(p)
        doc_lower = doc_text.lower()
        if "RUBBERDUCK-SKILL-ADVISOR.md" not in doc_text:
            failures.append(f"{rel} does not reference RUBBERDUCK-SKILL-ADVISOR.md")
        if "autonomous" not in doc_lower or "signoff" not in doc_lower:
            failures.append(f"{rel} missing advisor control-mode language")

    for platform, rel_root in PLATFORMS.items():
        for skill in SKILLS:
            skill_dir = root / rel_root / skill
            if not skill_dir.exists():
                continue
            skill_advisor = skill_dir / "RUBBERDUCK-SKILL-ADVISOR.md"
            if not skill_advisor.exists():
                failures.append(f"missing skill advisor: {platform}:{skill}")
            elif skill_advisor.read_bytes() != advisor.read_bytes():
                failures.append(f"skill advisor differs from package advisor: {platform}:{skill}")

            skill_start = skill_dir / "START_REPO_SESSION_PROMPT.md"
            if not skill_start.exists():
                failures.append(f"missing start repo session prompt: {platform}:{skill}")
            elif start.exists() and skill_start.read_bytes() != start.read_bytes():
                failures.append(f"start repo session prompt differs from package prompt: {platform}:{skill}")

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill_text = read_text(skill_md)
                if "RUBBERDUCK-SKILL-ADVISOR.md" not in skill_text:
                    failures.append(f"SKILL.md missing skill advisor reference: {platform}:{skill}")
                if skill == "rubberduck-codebase-atlas-pro" and "I need help from the RubberDuck Advisor." not in skill_text:
                    failures.append(f"Codebase Atlas missing advisor activation phrase: {platform}:{skill}")

    for rel in CURSOR_RULES:
        rule = root / rel
        if not rule.exists():
            continue
        rule_text = read_text(rule)
        if "RUBBERDUCK-SKILL-ADVISOR.md" not in rule_text:
            failures.append(f"Cursor rule missing skill advisor reference: {rel}")

    return failures


def builder_github_gate_sanity(root: Path) -> list[str]:
    """Enforce Builder's repo-backed validation claim firewall."""
    failures: list[str] = []
    builder = root / "codex" / "skills" / "rubberduck-feature-builder-pro"
    files = [
        "SKILL.md",
        "BUILD-WORKFLOW.md",
        "PR-READY-DIFF.md",
        "REPORT-TEMPLATE.md",
        "GITHUB-PUBLISH-REINDEX-GATE.md",
        "GITHUB-VALIDATION-SELF-CHECK.md",
        "scripts/validate_final_build_package.py",
    ]
    required = [
        "GitHub Publish/Re-index Gate",
        "LOCAL_BUILD_ONLY",
        "GITHUB_VALIDATED_BUILD",
        "AUTO_GITHUB_VALIDATED_BUILD",
        "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
        "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
        "Validation status: BLOCKED_BEFORE_REPO_BACKED_VALIDATION",
        "Local build complete; repo-backed RubberDuck validation is pending.",
        "git status --short",
        "secret scan",
        ".env.local",
        "git reset --hard",
        "destructive checkout",
        "detailed_repo_analysis",
        'semantic_mode="full"',
        "instance_id",
        "max_files=2000",
        "github-publish.md",
        "repo-backed-rubberduck-validation.md",
        "indexed-files-coverage.md",
    ]
    combined = ""
    for rel in files:
        p = builder / rel
        if not p.exists():
            failures.append(f"builder missing GitHub gate file: {rel}")
            continue
        combined += "\n" + read_text(p)
    for marker in required:
        if marker not in combined:
            failures.append(f"builder GitHub gate missing marker: {marker}")

    validator = builder / "scripts" / "validate_final_build_package.py"
    if validator.exists():
        validator_text = read_text(validator)
        for marker in [
            "FULL_REPO_BACKED_RUBBERDUCK_VALIDATED requires repo-backed evidence",
            "BUILD.md must contain exactly one validation status label",
            "non-full validation label cannot claim full RubberDuck validation",
            "repo-backed RubberDuck validation is pending",
            "github-publish.md",
            "repo-backed-rubberduck-validation.md",
            "indexed-files-coverage.md",
        ]:
            if marker not in validator_text:
                failures.append(f"builder validator missing marker: {marker}")

    tests = root / "verification" / "run_power_skill_synthetic_tests.py"
    if tests.exists():
        test_text = read_text(tests)
        for marker in [
            "builder valid local-pending final package",
            "builder valid full repo-backed final package",
            "builder rejects full validation without repo evidence",
            "builder rejects local pending with full-validation claim",
        ]:
            if marker not in test_text:
                failures.append(f"builder synthetic tests missing marker: {marker}")

    return failures


def security_delta_gate_sanity(root: Path) -> list[str]:
    """Enforce the PR security delta gate across build/security/auto surfaces."""
    failures: list[str] = []
    gate = root / "RUBBERDUCK-SECURITY-DELTA-GATE.md"
    if not gate.exists():
        return ["missing RUBBERDUCK-SECURITY-DELTA-GATE.md"]
    gate_text = read_text(gate)
    for marker in [
        "No new untriaged Critical findings",
        "No new untriaged High findings",
        "pre_existing_findings",
        "security-delta.json",
        "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
        "Security delta status: NEW_FINDINGS_ADJUDICATED",
        "Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS",
        "Security delta status: NOT_RUN_LOCAL_ONLY",
        "PR_READY.diff",
        "Never claim \"repo is clean\"",
    ]:
        if marker not in gate_text:
            failures.append(f"RUBBERDUCK-SECURITY-DELTA-GATE.md missing marker: {marker}")

    docs = [
        "README.md",
        "START_REPO_SESSION_PROMPT.md",
        "USE_PROMPTS.md",
        "RESEARCH_PREVIEW.md",
        "codex/AGENTS_SNIPPET.md",
        "claude-code/CLAUDE.md_SNIPPET.md",
        "cursor/AGENTS.md_SNIPPET.md",
    ]
    for rel in docs:
        p = root / rel
        if not p.exists():
            failures.append(f"security delta doc check missing file: {rel}")
            continue
        text = read_text(p)
        if "RUBBERDUCK-SECURITY-DELTA-GATE.md" not in text:
            failures.append(f"{rel} does not reference RUBBERDUCK-SECURITY-DELTA-GATE.md")
        if "pre-existing" not in text.lower() or "Critical/High" not in text:
            failures.append(f"{rel} missing security-delta baseline/new finding language")

    relevant = {
        "rubberduck-feature-builder-pro",
        "rubberduck-autonomous-feature-mode",
        "rubberduck-security-audit",
    }
    for platform, rel_root in PLATFORMS.items():
        for skill in relevant:
            skill_dir = root / rel_root / skill
            skill_gate = skill_dir / "RUBBERDUCK-SECURITY-DELTA-GATE.md"
            if not skill_gate.exists():
                failures.append(f"missing security delta gate: {platform}:{skill}")
            elif skill_gate.read_bytes() != gate.read_bytes():
                failures.append(f"security delta gate differs from package gate: {platform}:{skill}")
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill_text = read_text(skill_md)
                if "RUBBERDUCK-SECURITY-DELTA-GATE.md" not in skill_text:
                    failures.append(f"SKILL.md missing security delta reference: {platform}:{skill}")
                if "CLEAN_NO_NEW_CRITICAL_HIGH" not in skill_text:
                    failures.append(f"SKILL.md missing security delta status: {platform}:{skill}")

    for rel in [
        "cursor/.cursor/rules/rubberduck-feature-builder-pro.mdc",
        "cursor/.cursor/rules/rubberduck-autonomous-feature-mode.mdc",
        "cursor/.cursor/rules/rubberduck-security-audit.mdc",
    ]:
        rule = root / rel
        if not rule.exists():
            continue
        rule_text = read_text(rule)
        if "RUBBERDUCK-SECURITY-DELTA-GATE.md" not in rule_text:
            failures.append(f"Cursor rule missing security delta reference: {rel}")

    builder_validator = root / "codex" / "skills" / "rubberduck-feature-builder-pro" / "scripts" / "validate_final_build_package.py"
    if builder_validator.exists():
        validator_text = read_text(builder_validator)
        for marker in [
            "BUILD.md must contain exactly one security delta status label",
            "PR_READY.diff exists but security delta is blocked",
            "BUILD.md claims repo is clean while pre_existing_findings are present",
            "security-delta.json missing",
        ]:
            if marker not in validator_text:
                failures.append(f"builder validator missing security delta marker: {marker}")

    tests = root / "verification" / "run_power_skill_synthetic_tests.py"
    if tests.exists():
        test_text = read_text(tests)
        for marker in [
            "builder rejects missing security delta evidence",
            "builder rejects PR_READY with blocked security delta",
            "builder accepts pre-existing high as non-blocking",
            "builder accepts adjudicated new finding",
            "builder rejects repo-clean claim with pre-existing findings",
            "auto rejects blocked security delta completion",
        ]:
            if marker not in test_text:
                failures.append(f"synthetic tests missing security delta marker: {marker}")

    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".", help="Extracted package root")
    ap.add_argument("--write", default="", help="Optional path to write JSON results")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    results: dict = {
        "root": "<package_root>",
        "top_level": {},
        "cursor_rules": {},
        "ci_bootstrap": {},
        "response_marker": {},
        "skill_advisor": {},
        "builder_github_gate": {},
        "security_delta_gate": {},
        "skill_hashes": {},
        "checks": {},
        "safety_hits": [],
        "failures": [],
    }

    for rel in TOP_LEVEL_REQUIRED:
        ok = (root / rel).exists()
        results["top_level"][rel] = ok
        if not ok:
            results["failures"].append(f"missing top-level file: {rel}")

    for rel in CURSOR_RULES:
        rule_path = root / rel
        ok = rule_path.exists()
        results["cursor_rules"][rel] = ok
        if not ok:
            results["failures"].append(f"missing Cursor rule: {rel}")
        else:
            rule_text = read_text(rule_path)
            if not rule_text.startswith("---"):
                results["failures"].append(f"Cursor rule missing frontmatter: {rel}")
            skill_slug = Path(rel).stem
            if skill_slug not in rule_text:
                results["failures"].append(f"Cursor rule missing skill slug reference: {rel}")

    doc_failures = doc_sanity(root)
    for failure in doc_failures:
        results["failures"].append(failure)

    bootstrap_failures = ci_bootstrap_sanity(root)
    results["ci_bootstrap"] = {
        "checked": True,
        "failures": bootstrap_failures,
    }
    for failure in bootstrap_failures:
        results["failures"].append(failure)

    marker_failures = response_marker_sanity(root)
    results["response_marker"] = {
        "checked": True,
        "failures": marker_failures,
    }
    for failure in marker_failures:
        results["failures"].append(failure)

    advisor_failures = skill_advisor_sanity(root)
    results["skill_advisor"] = {
        "checked": True,
        "failures": advisor_failures,
    }
    for failure in advisor_failures:
        results["failures"].append(failure)

    builder_gate_failures = builder_github_gate_sanity(root)
    results["builder_github_gate"] = {
        "checked": True,
        "failures": builder_gate_failures,
    }
    for failure in builder_gate_failures:
        results["failures"].append(failure)

    security_delta_failures = security_delta_gate_sanity(root)
    results["security_delta_gate"] = {
        "checked": True,
        "failures": security_delta_failures,
    }
    for failure in security_delta_failures:
        results["failures"].append(failure)

    for skill in SKILLS:
        results["skill_hashes"][skill] = {}
        expected_hash = None
        for platform, rel_root in PLATFORMS.items():
            skill_dir = root / rel_root / skill
            if not skill_dir.exists():
                results["failures"].append(f"missing skill folder: {platform}:{skill}")
                continue
            digest = hash_dir(skill_dir)
            results["skill_hashes"][skill][platform] = digest
            if expected_hash is None:
                expected_hash = digest
            elif digest != expected_hash:
                results["failures"].append(f"hash mismatch for {skill}: {platform}")

            for script_name in ["verify_skill_structure.py", "smoke_test_skill.py"]:
                script = skill_dir / "scripts" / script_name
                key = f"{platform}:{skill}:{script_name}"
                if not script.exists():
                    results["checks"][key] = {"exit_code": 1, "stdout": "", "stderr": "missing script"}
                    results["failures"].append(f"missing script: {key}")
                    continue
                res = run_script(script, [str(skill_dir)], cwd=skill_dir)
                results["checks"][key] = res
                if res["exit_code"] != 0:
                    results["failures"].append(f"check failed: {key}")

    synthetic_script = root / "verification/run_power_skill_synthetic_tests.py"
    if synthetic_script.exists():
        key = "verification:run_power_skill_synthetic_tests.py"
        res = run_script(synthetic_script, [str(root)], cwd=root)
        results["checks"][key] = res
        if res["exit_code"] != 0:
            results["failures"].append(f"check failed: {key}")
    else:
        results["failures"].append("missing verification/run_power_skill_synthetic_tests.py")

    routing_script = root / "verification/check_skill_routing.py"
    if routing_script.exists():
        key = "verification:check_skill_routing.py"
        res = run_script(routing_script, [str(root)], cwd=root)
        results["checks"][key] = res
        if res["exit_code"] != 0:
            results["failures"].append(f"check failed: {key}")
    else:
        results["failures"].append("missing verification/check_skill_routing.py")

    hits = safe_scan(root)
    results["safety_hits"] = hits
    if hits:
        results["failures"].append(f"safety scan hits: {len(hits)}")

    if args.write:
        out = Path(args.write)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps({
        "root": "<package_root>",
        "checks_run": len(results["checks"]),
        "failures": len(results["failures"]),
        "safety_hits": len(hits),
        "skills": SKILLS,
        "platforms": list(PLATFORMS),
    }, indent=2))
    if results["failures"]:
        print("FAILURES:")
        for failure in results["failures"]:
            print(f" - {failure}")
        return 2
    print("OK: all platform skill checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
