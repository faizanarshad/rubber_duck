# RubberDuck Security Delta Gate

Use this gate for GitHub-validated feature builds and autonomous builds before marking a PR ready.

## Goal

Prevent a feature PR from being called ready when it introduces untriaged Critical or High RubberDuck security findings, without turning every feature branch into a broad cleanup of pre-existing repository debt.

Default standard:

```text
No new untriaged Critical findings.
No new untriaged High findings in changed or newly created code.
All true-positive new Critical/High findings are fixed.
All false positives are adjudicated with evidence.
Pre-existing findings are separated into a baseline section.
The whole repo does not need to be clean unless the user explicitly asks for that policy.
```

## Trigger

Run this gate when any of these are true:

- The build used `GITHUB_VALIDATED_BUILD` or `AUTO_GITHUB_VALIDATED_BUILD`.
- The user asks for a security sweep, RubberDuck security validation, PR security validation, or a clean PR.
- The Skill Advisor selection says to run the security delta loop.
- RubberDuck Codebase Intelligence reports Critical or High findings on the pushed branch.
- The feature touches auth, persistence, SQL, filesystem, subprocess, network, deserialization, secrets, tokens, permissions, or externally reachable handlers.

For `LOCAL_BUILD_ONLY`, do not run the gate and use:

```text
Security delta status: NOT_RUN_LOCAL_ONLY
```

## Required flow

```text
1. Pin base branch and commit.
2. Pin PR branch and head commit.
3. Run RubberDuck Codebase Intelligence on base.
4. Run RubberDuck Codebase Intelligence on PR head.
5. Normalize findings into stable keys.
6. Diff PR findings against base findings.
7. Classify findings:
   - new_findings
   - pre_existing_findings
   - fixed_findings
   - adjudicated_false_positives
   - unresolved_blockers
8. Auto-fix true-positive new Critical/High findings in changed or newly created code when inside the authorized mutation envelope.
9. Re-run local tests and RubberDuck.
10. Repeat until clean, adjudicated, or max_security_fix_iterations is reached.
```

Do not auto-fix all scanner findings. Pre-existing repo-wide findings and broad static-analysis false positives are documented, not silently folded into the feature patch.

## Required artifacts

```text
uc07/<slug>/evidence/security-baseline-rubberduck.md
uc07/<slug>/evidence/security-pr-head-rubberduck.md
uc07/<slug>/evidence/security-delta.json
uc07/<slug>/evidence/security-delta.md
uc07/<slug>/evidence/security-fix-loop-history.json
uc07/<slug>/evidence/finding-adjudication.json
```

`security-delta.json` must include:

```json
{
  "base": {"branch": "main", "commit": "...", "analysis_id": "..."},
  "head": {"branch": "codex/...", "commit": "...", "analysis_id": "..."},
  "new_findings": [],
  "pre_existing_findings": [],
  "fixed_findings": [],
  "adjudicated_false_positives": [],
  "unresolved_blockers": []
}
```

Each finding should include severity, title, file, line when available, source tool, stable key, status, and evidence pointer.

## Security delta status labels

Every Builder or Autonomous final answer must include exactly one:

```text
Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH
Security delta status: NEW_FINDINGS_ADJUDICATED
Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS
Security delta status: NOT_RUN_LOCAL_ONLY
```

Use `CLEAN_NO_NEW_CRITICAL_HIGH` only when no new untriaged Critical/High findings remain.

Use `NEW_FINDINGS_ADJUDICATED` only when new Critical/High findings exist but all are either fixed or adjudicated with evidence and no unresolved blocker remains.

Use `BLOCKED_NEW_UNRESOLVED_FINDINGS` when a new Critical/High finding remains unresolved, evidence is insufficient, RubberDuck cannot produce a comparable baseline/head result, or the authorized mutation envelope prevents a needed fix.

Use `NOT_RUN_LOCAL_ONLY` only for local-only builds that did not push/index a GitHub branch.

## PR readiness rule

`PR_READY.diff` and ready-for-review PR promotion are allowed only with:

```text
Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH
```

or:

```text
Security delta status: NEW_FINDINGS_ADJUDICATED
```

`Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS` must keep the PR draft or blocked.

Never claim "repo is clean" when `pre_existing_findings` is non-empty. Say "the PR security delta is clean" instead.
