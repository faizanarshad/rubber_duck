# PR Ready Diff

Emit `PR_READY.diff` only when:

```text
Spec Heartbeat permits completion
validate_generated_diff PASS
Final Command Gate passes or is explicitly accepted unavailable
GitHub Publish/Re-index Gate either completed for repo-backed RubberDuck validation or the run is explicitly LOCAL_BUILD_ONLY
Security Delta Gate is either `CLEAN_NO_NEW_CRITICAL_HIGH`, `NEW_FINDINGS_ADJUDICATED`, or `NOT_RUN_LOCAL_ONLY` for explicit local-only builds
```

`PR_READY.diff` can exist for `LOCAL_BUILD_ONLY`, but the final answer and BUILD.md must say:

```text
Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING
Security delta status: NOT_RUN_LOCAL_ONLY
Local build complete; repo-backed RubberDuck validation is pending.
```

Do not emit or promote PR-ready output when:

```text
Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS
```

Otherwise emit BUILD.md with unresolved blockers and do not create PR_READY.diff.
