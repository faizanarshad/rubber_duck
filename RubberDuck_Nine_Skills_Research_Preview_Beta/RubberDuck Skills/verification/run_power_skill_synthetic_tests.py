#!/usr/bin/env python3
"""Run synthetic validator tests for Plan/Build/Autonomous power skills.

This is a package-level regression test. It creates temporary positive and
negative fixtures, then verifies that the validators accept good artifacts and
reject known-bad artifacts.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import runpy
import sys
import tempfile
from pathlib import Path


def run_script(script: Path, argv: list[str]) -> dict:
    old_argv = sys.argv[:]
    old_path = sys.path[:]
    out = io.StringIO()
    err = io.StringIO()
    code = 0
    try:
        sys.argv = [str(script)] + argv
        sys.path.insert(0, str(script.parent))
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as e:
                if isinstance(e.code, int):
                    code = e.code
                elif e.code is None:
                    code = 0
                else:
                    code = 1
                    print(str(e.code), file=err)
    except Exception as e:
        code = 99
        print(repr(e), file=err)
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
    return {"exit_code": code, "stdout": out.getvalue(), "stderr": err.getvalue()}


def write_json(path: Path, data: dict | list) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def base_plan() -> dict:
    return {
        "schema_version": "1.0",
        "plan_type": "FEATURE_PLAN",
        "repo": "owner/repo",
        "base_commit": "abc123",
        "feature_title": "Synthetic feature",
        "feature_description": "Synthetic feature for validator tests",
        "session_id": "cg_test",
        "fit_pack_id": "fit_test",
        "planned_files": [{"path": "src/example.py", "role": "MODIFY"}],
        "off_limits_files": [{"path": "src/off_limits.py", "why": "synthetic"}],
        "reusable_symbols": [{"symbol": "ExistingHelper", "module": "pkg"}],
        "existing_patterns": [{"symbol": "Pattern", "path": "src/pattern.py"}],
        "acceptance_criteria": [{"id": "AC-1", "criterion": "works", "test": "test_works"}],
        "test_plan": [{"test": "test_works", "file": "tests/test_example.py"}],
        "test_diff_path": "test_diff.patch",
        "effect_manifest": {"allowed_effects": [], "forbidden_effects": [], "new_side_effects": []},
        "command_plan": {"tests": ["pytest tests/test_example.py"], "typecheck": [], "lint": []},
        "generation_constraints": ["minimal"],
        "negative_scope": ["no new dependencies"],
        "tool_health": {"status": "synthetic"},
        "sealed_at": "2026-05-22T00:00:00Z",
        "plan_sha256": "synthetic",
    }


def write_repo_backed_evidence(build_dir: Path) -> None:
    evidence = build_dir / "evidence"
    evidence.mkdir(exist_ok=True)
    (evidence / "github-publish.md").write_text(
        "branch codex/synthetic\ncommit abc123\npushed remote origin\nPR URL none\nstaged file list src/example.py\nsecret-scan result PASS\n",
        encoding="utf-8",
    )
    (evidence / "repo-backed-rubberduck-validation.md").write_text(
        "detailed_repo_analysis repo owner/repo branch codex/synthetic commit abc123 semantic_mode=\"full\" indexing status complete validation PASS\n",
        encoding="utf-8",
    )
    (evidence / "indexed-files-coverage.md").write_text(
        "changed files src/example.py\nnew files src/new_example.py\nloaded patterns *.py\ncoverage complete\n",
        encoding="utf-8",
    )


def write_security_delta_evidence(
    build_dir: Path,
    *,
    new_findings: list[dict] | None = None,
    pre_existing_findings: list[dict] | None = None,
    fixed_findings: list[dict] | None = None,
    adjudicated_false_positives: list[dict] | None = None,
    unresolved_blockers: list[dict] | None = None,
) -> None:
    evidence = build_dir / "evidence"
    evidence.mkdir(exist_ok=True)
    delta = {
        "base": {"branch": "main", "commit": "base123", "analysis_id": "base_analysis"},
        "head": {"branch": "codex/synthetic", "commit": "abc123", "analysis_id": "head_analysis"},
        "new_findings": new_findings or [],
        "pre_existing_findings": pre_existing_findings or [],
        "fixed_findings": fixed_findings or [],
        "adjudicated_false_positives": adjudicated_false_positives or [],
        "unresolved_blockers": unresolved_blockers or [],
    }
    write_json(evidence / "security-delta.json", delta)
    (evidence / "security-baseline-rubberduck.md").write_text("base detailed_repo_analysis complete\n", encoding="utf-8")
    (evidence / "security-pr-head-rubberduck.md").write_text("head detailed_repo_analysis complete\n", encoding="utf-8")
    (evidence / "security-delta.md").write_text("security delta summary\n", encoding="utf-8")
    write_json(evidence / "security-fix-loop-history.json", [])
    write_json(evidence / "finding-adjudication.json", adjudicated_false_positives or [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package_root", nargs="?", default=".")
    args = ap.parse_args()
    root = Path(args.package_root).resolve()

    codex = root / "codex" / "skills"
    planner = codex / "rubberduck-feature-planner-pro" / "scripts"
    builder = codex / "rubberduck-feature-builder-pro" / "scripts"
    auto = codex / "rubberduck-autonomous-feature-mode" / "scripts"

    tests: list[dict] = []

    def expect(name: str, script: Path, argv: list[str], should_pass: bool) -> None:
        res = run_script(script, argv)
        passed = (res["exit_code"] == 0) if should_pass else (res["exit_code"] != 0)
        tests.append({
            "name": name,
            "script": str(script.relative_to(root)),
            "expected": "pass" if should_pass else "fail",
            "exit_code": res["exit_code"],
            "passed": passed,
            "stdout": res["stdout"],
            "stderr": res["stderr"],
        })

    with tempfile.TemporaryDirectory(prefix="rubberduck_power_skill_tests_") as td:
        t = Path(td)

        # Planner fixtures.
        plan = base_plan()
        plan_path = t / "sealed_plan.json"
        write_json(plan_path, plan)
        bad_plan = dict(plan)
        bad_plan["user_signoff_received"] = True
        bad_plan_path = t / "bad_sealed_plan.json"
        write_json(bad_plan_path, bad_plan)

        test_diff = t / "test_diff.patch"
        test_diff.write_text("diff --git a/tests/test_example.py b/tests/test_example.py\n+def test_works():\n+    assert True\n", encoding="utf-8")
        bad_diff = t / "bad_diff.patch"
        bad_diff.write_text("diff --git a/src/example.py b/src/example.py\n+def impl():\n+    return 1\n", encoding="utf-8")

        expect("planner valid sealed plan", planner / "validate_sealed_plan.py", [str(plan_path)], True)
        expect("planner rejects mutable signoff", planner / "validate_sealed_plan.py", [str(bad_plan_path)], False)
        expect("planner valid test diff", planner / "validate_test_diff_contract.py", [str(test_diff)], True)
        expect("planner rejects non-test diff", planner / "validate_test_diff_contract.py", [str(bad_diff)], False)

        # Builder fixtures.
        signoff = {
            "sealed_plan_sha256": sha(plan_path),
            "approved": True,
            "invoked_under": "USER",
        }
        signoff_path = t / "SIGNOFF.json"
        write_json(signoff_path, signoff)
        missing_signoff_path = t / "MISSING_SIGNOFF.json"
        bad_signoff = dict(signoff)
        bad_signoff["sealed_plan_sha256"] = "wrong"
        bad_signoff_path = t / "BAD_SIGNOFF.json"
        write_json(bad_signoff_path, bad_signoff)

        heartbeat = {
            "iteration": 1,
            "all_green": True,
            "dimensions": {
                "H1_acceptance_criteria": {"status": "GREEN", "evidence": ["tests/test_example.py:1"]},
                "H4_avoid_list_integrity": {"status": "GREEN", "evidence": ["git diff --name-only"]},
            },
        }
        heartbeat_path = t / "HEARTBEAT.json"
        write_json(heartbeat_path, heartbeat)
        bad_heartbeat = {
            "iteration": 1,
            "all_green": True,
            "dimensions": {
                "H1_acceptance_criteria": {"status": "GREEN", "evidence": []},
            },
        }
        bad_heartbeat_path = t / "BAD_HEARTBEAT.json"
        write_json(bad_heartbeat_path, bad_heartbeat)

        audit_path = t / "AUDIT.json"
        write_json(audit_path, [{"iteration": 1, "action": "synthetic", "heartbeat_snapshot": heartbeat}])
        bad_audit_path = t / "BAD_AUDIT.json"
        write_json(bad_audit_path, [{"iteration": 1, "action": "synthetic"}])

        build_dir = t / "build"
        build_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "synthetic PR_READY.diff",
                    "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
                    "Security delta status: NOT_RUN_LOCAL_ONLY",
                    "Local build complete; repo-backed RubberDuck validation is pending.",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (build_dir / name).write_text(text, encoding="utf-8")
        full_build_dir = t / "full_build"
        full_build_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (full_build_dir / name).write_text(text, encoding="utf-8")
        write_repo_backed_evidence(full_build_dir)
        write_security_delta_evidence(full_build_dir)
        bad_full_dir = t / "bad_full"
        bad_full_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (bad_full_dir / name).write_text(text, encoding="utf-8")
        bad_claim_dir = t / "bad_local_claim"
        bad_claim_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
                    "Security delta status: NOT_RUN_LOCAL_ONLY",
                    "Local build complete; repo-backed RubberDuck validation is pending.",
                    "fully RubberDuck validated",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (bad_claim_dir / name).write_text(text, encoding="utf-8")
        bad_build_dir = t / "bad_build"
        bad_build_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json"]:
            text = "\n".join([
                "mentions PR_READY.diff",
                "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
                "Security delta status: NOT_RUN_LOCAL_ONLY",
                "Local build complete; repo-backed RubberDuck validation is pending.",
            ]) if name == "BUILD.md" else "{}"
            (bad_build_dir / name).write_text(text, encoding="utf-8")
        bad_pr_ready_dir = t / "bad_pr_ready"
        bad_pr_ready_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            text = "\n".join([
                "synthetic PR_READY.diff",
                "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
                "Security delta status: NOT_RUN_LOCAL_ONLY",
                "Local build complete; repo-backed RubberDuck validation is pending.",
            ]) if name == "BUILD.md" else "{}"
            (bad_pr_ready_dir / name).write_text(text, encoding="utf-8")
        bad_off_limits_dir = t / "bad_off_limits"
        bad_off_limits_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "synthetic PR_READY.diff",
                    "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
                    "Security delta status: NOT_RUN_LOCAL_ONLY",
                    "Local build complete; repo-backed RubberDuck validation is pending.",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (bad_off_limits_dir / name).write_text(text, encoding="utf-8")
        write_json(bad_off_limits_dir / "sealed_plan.json", plan)
        write_json(bad_off_limits_dir / "changed-files.json", ["src/off_limits.py"])

        missing_security_dir = t / "missing_security_delta"
        missing_security_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (missing_security_dir / name).write_text(text, encoding="utf-8")
        write_repo_backed_evidence(missing_security_dir)

        blocked_security_dir = t / "blocked_security_delta"
        blocked_security_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (blocked_security_dir / name).write_text(text, encoding="utf-8")
        write_repo_backed_evidence(blocked_security_dir)
        write_security_delta_evidence(
            blocked_security_dir,
            new_findings=[{"severity": "HIGH", "status": "OPEN", "in_changed_code": True, "file": "src/example.py"}],
            unresolved_blockers=[{"severity": "HIGH", "why": "synthetic unresolved"}],
        )

        preexisting_high_dir = t / "preexisting_high"
        preexisting_high_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
                    "the PR security delta is clean",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (preexisting_high_dir / name).write_text(text, encoding="utf-8")
        write_repo_backed_evidence(preexisting_high_dir)
        write_security_delta_evidence(
            preexisting_high_dir,
            pre_existing_findings=[{"severity": "HIGH", "status": "PRE_EXISTING", "file": "src/legacy.py"}],
        )

        adjudicated_dir = t / "adjudicated_security_delta"
        adjudicated_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: NEW_FINDINGS_ADJUDICATED",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (adjudicated_dir / name).write_text(text, encoding="utf-8")
        write_repo_backed_evidence(adjudicated_dir)
        write_security_delta_evidence(
            adjudicated_dir,
            new_findings=[{"severity": "HIGH", "status": "ADJUDICATED_FALSE_POSITIVE", "in_changed_code": True, "file": "src/example.py"}],
            adjudicated_false_positives=[{"severity": "HIGH", "status": "ADJUDICATED_FALSE_POSITIVE", "evidence": "synthetic"}],
        )

        repo_clean_claim_dir = t / "repo_clean_claim"
        repo_clean_claim_dir.mkdir()
        for name in ["BUILD.md","AUDIT.json","HEARTBEAT.json","heartbeat-history.json","validation-history.json","WARN_ADJUDICATION.json","PR_READY.diff"]:
            if name == "BUILD.md":
                text = "\n".join([
                    "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
                    "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
                    "repo is clean",
                    "synthetic PR_READY.diff",
                ])
            elif name == "validation-history.json":
                text = json.dumps({"final_verdict": "PASS"})
            else:
                text = "{}"
            (repo_clean_claim_dir / name).write_text(text, encoding="utf-8")
        write_repo_backed_evidence(repo_clean_claim_dir)
        write_security_delta_evidence(
            repo_clean_claim_dir,
            pre_existing_findings=[{"severity": "HIGH", "status": "PRE_EXISTING", "file": "src/legacy.py"}],
        )

        expect("builder valid signoff", builder / "validate_signoff.py", [str(plan_path), str(signoff_path)], True)
        expect("builder rejects missing signoff", builder / "validate_build_inputs.py", [str(plan_path), str(missing_signoff_path)], False)
        expect("builder rejects bad signoff hash", builder / "validate_signoff.py", [str(plan_path), str(bad_signoff_path)], False)
        expect("builder valid heartbeat", builder / "validate_heartbeat.py", [str(heartbeat_path)], True)
        expect("builder rejects green without evidence", builder / "validate_heartbeat.py", [str(bad_heartbeat_path)], False)
        expect("builder valid audit log", builder / "validate_audit_log.py", [str(audit_path)], True)
        expect("builder rejects incomplete audit log", builder / "validate_audit_log.py", [str(bad_audit_path)], False)
        expect("builder valid local-pending final package", builder / "validate_final_build_package.py", [str(build_dir)], True)
        expect("builder valid full repo-backed final package", builder / "validate_final_build_package.py", [str(full_build_dir)], True)
        expect("builder rejects full validation without repo evidence", builder / "validate_final_build_package.py", [str(bad_full_dir)], False)
        expect("builder rejects local pending with full-validation claim", builder / "validate_final_build_package.py", [str(bad_claim_dir)], False)
        expect("builder rejects missing security delta evidence", builder / "validate_final_build_package.py", [str(missing_security_dir)], False)
        expect("builder rejects PR_READY with blocked security delta", builder / "validate_final_build_package.py", [str(blocked_security_dir)], False)
        expect("builder accepts pre-existing high as non-blocking", builder / "validate_final_build_package.py", [str(preexisting_high_dir)], True)
        expect("builder accepts adjudicated new finding", builder / "validate_final_build_package.py", [str(adjudicated_dir)], True)
        expect("builder rejects repo-clean claim with pre-existing findings", builder / "validate_final_build_package.py", [str(repo_clean_claim_dir)], False)
        expect("builder rejects missing PR_READY", builder / "validate_final_build_package.py", [str(bad_build_dir)], False)
        expect("builder rejects PR_READY without PASS validation", builder / "validate_final_build_package.py", [str(bad_pr_ready_dir)], False)
        expect("builder rejects off-limits touched file", builder / "validate_final_build_package.py", [str(bad_off_limits_dir)], False)
        expect("builder valid build inputs", builder / "validate_build_inputs.py", [str(plan_path), str(signoff_path)], True)
        expect("builder rejects mutable plan in inputs", builder / "validate_build_inputs.py", [str(bad_plan_path), str(signoff_path)], False)

        # Autonomous fixtures.
        envelope = {
            "repo": "owner/repo",
            "base_commit": "abc123",
            "feature_description": "Synthetic",
            "tier": "STANDARD",
            "max_iterations": 50,
            "max_files_touched": 12,
            "max_new_dependencies": 0,
            "allowed_file_globs": [],
            "off_limits_file_globs": [],
            "require_final_user_review": True,
        }
        envelope_path = t / "AUTONOMY_ENVELOPE.json"
        write_json(envelope_path, envelope)
        bad_envelope = dict(envelope)
        bad_envelope["tier"] = "FAST"
        bad_envelope_path = t / "BAD_AUTONOMY_ENVELOPE.json"
        write_json(bad_envelope_path, bad_envelope)
        zero_iter_envelope = dict(envelope)
        zero_iter_envelope["max_iterations"] = 0
        zero_iter_envelope_path = t / "ZERO_ITER_AUTONOMY_ENVELOPE.json"
        write_json(zero_iter_envelope_path, zero_iter_envelope)

        auto_audit = {
            "autonomy_envelope": envelope,
            "planner": {"status": "complete"},
            "sealed_plan_sha256": sha(plan_path),
            "builder": {"validation_passed": True},
            "final_status": "complete",
        }
        auto_audit_path = t / "AUTO_AUDIT.json"
        write_json(auto_audit_path, auto_audit)
        security_envelope = dict(envelope)
        security_envelope["security_delta_required"] = True
        security_auto_audit = dict(auto_audit)
        security_auto_audit["autonomy_envelope"] = security_envelope
        security_auto_audit["security_delta_required"] = True
        security_auto_audit["security_delta"] = {"status": "CLEAN_NO_NEW_CRITICAL_HIGH", "unresolved_blockers": []}
        security_auto_audit_path = t / "SECURITY_AUTO_AUDIT.json"
        write_json(security_auto_audit_path, security_auto_audit)
        bad_auto_audit = dict(auto_audit)
        bad_auto_audit["builder"] = {"validation_passed": False}
        bad_auto_audit_path = t / "BAD_AUTO_AUDIT.json"
        write_json(bad_auto_audit_path, bad_auto_audit)
        bad_planner_audit = dict(auto_audit)
        bad_planner_audit["planner"] = {"status": "incomplete"}
        bad_planner_audit_path = t / "BAD_PLANNER_AUTO_AUDIT.json"
        write_json(bad_planner_audit_path, bad_planner_audit)
        off_limits_envelope = dict(envelope)
        off_limits_envelope["off_limits_file_globs"] = ["src/off_limits.py"]
        bad_off_limits_audit = dict(auto_audit)
        bad_off_limits_audit["autonomy_envelope"] = off_limits_envelope
        bad_off_limits_audit["builder"] = {"validation_passed": True, "files_touched": ["src/off_limits.py"]}
        bad_off_limits_audit_path = t / "BAD_OFF_LIMITS_AUTO_AUDIT.json"
        write_json(bad_off_limits_audit_path, bad_off_limits_audit)
        bad_missing_security_audit = dict(security_auto_audit)
        bad_missing_security_audit.pop("security_delta")
        bad_missing_security_audit_path = t / "BAD_MISSING_SECURITY_AUTO_AUDIT.json"
        write_json(bad_missing_security_audit_path, bad_missing_security_audit)
        bad_blocked_security_audit = dict(security_auto_audit)
        bad_blocked_security_audit["security_delta"] = {
            "status": "BLOCKED_NEW_UNRESOLVED_FINDINGS",
            "unresolved_blockers": [{"severity": "HIGH", "why": "synthetic"}],
        }
        bad_blocked_security_audit_path = t / "BAD_BLOCKED_SECURITY_AUTO_AUDIT.json"
        write_json(bad_blocked_security_audit_path, bad_blocked_security_audit)

        expect("auto valid envelope", auto / "validate_autonomy_envelope.py", [str(envelope_path)], True)
        expect("auto rejects invalid envelope", auto / "validate_autonomy_envelope.py", [str(bad_envelope_path)], False)
        expect("auto rejects zero max_iterations", auto / "validate_autonomy_envelope.py", [str(zero_iter_envelope_path)], False)
        expect("auto valid audit", auto / "validate_auto_audit.py", [str(auto_audit_path)], True)
        expect("auto valid audit with security delta", auto / "validate_auto_audit.py", [str(security_auto_audit_path)], True)
        expect("auto rejects complete without builder validation", auto / "validate_auto_audit.py", [str(bad_auto_audit_path)], False)
        expect("auto rejects complete without planner completion", auto / "validate_auto_audit.py", [str(bad_planner_audit_path)], False)
        expect("auto rejects off-limits touched file", auto / "validate_auto_audit.py", [str(bad_off_limits_audit_path)], False)
        expect("auto rejects missing required security delta", auto / "validate_auto_audit.py", [str(bad_missing_security_audit_path)], False)
        expect("auto rejects blocked security delta completion", auto / "validate_auto_audit.py", [str(bad_blocked_security_audit_path)], False)

    failures = [x for x in tests if not x["passed"]]
    print(json.dumps({
        "tests_run": len(tests),
        "passed": len(tests) - len(failures),
        "failed": len(failures),
        "tests": tests,
    }, indent=2, sort_keys=True))

    if failures:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
