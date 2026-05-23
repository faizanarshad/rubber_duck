# Build Report Template

```markdown
# BUILD — <feature title>

## §0 Envelope
## §1 Final Spec Heartbeat
## §2 Acceptance Criteria Satisfaction
## §3 Iteration Summary
## §4 Files Touched
## §5 Doppelganger Gates Triggered
## §6 Drift Events
## §7 Reverts
## §8 Validation History
## §9 Final Command Gate
## §10 GitHub Publish/Re-index Gate
## §11 Repo-backed RubberDuck Validation
## §12 Security Delta Gate
## §13 Validation Status Label
## §14 Security Delta Status Label
## §15 Paste-Ready PR Description
## §16 Open Issues
## §17 Tool Health and Gaps
```

`§12` must contain exactly one:

```text
Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED
Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING
Validation status: BLOCKED_BEFORE_REPO_BACKED_VALIDATION
```

`§14` must contain exactly one:

```text
Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH
Security delta status: NEW_FINDINGS_ADJUDICATED
Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS
Security delta status: NOT_RUN_LOCAL_ONLY
```
