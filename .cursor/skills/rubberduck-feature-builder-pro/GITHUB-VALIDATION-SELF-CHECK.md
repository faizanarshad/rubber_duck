# GitHub Validation Self-check

Before finalizing Builder changes, confirm these cases are covered by instructions or validators:

```text
[ ] local semantic failure triggers GitHub Publish/Re-index Gate
[ ] final response cannot claim full validation when GitHub indexing was skipped
[ ] autonomous mode can push only after AUTO_AUTHORIZATION.json or explicit external GitHub mutation approval
[ ] dirty worktree requires scoped staging and unrelated files are excluded
[ ] secrets are excluded from staged changes
[ ] destructive git reset or checkout is forbidden
[ ] final answer contains exactly one validation status label
[ ] final answer contains exactly one security delta status label
[ ] GitHub-validated builds run base-vs-PR RubberDuck security delta before PR-ready promotion
[ ] new Critical/High findings in changed code block completion until fixed or adjudicated
[ ] pre-existing High findings do not block by default
[ ] repo-clean claims are rejected when pre-existing findings remain
```

The deterministic package tests should cover the claim firewall:

```text
LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING can pass with local evidence
FULL_REPO_BACKED_RUBBERDUCK_VALIDATED fails without repo-backed evidence
FULL_REPO_BACKED_RUBBERDUCK_VALIDATED passes only with github-publish, repo-backed validation, and indexed-file coverage evidence
Security delta CLEAN/ADJUDICATED passes only with security delta artifacts
Security delta BLOCKED rejects PR_READY.diff
```
