# Signoff and Authorization

USER mode requires `SIGNOFF.json`.

AUTO_MODE requires `AUTO_AUTHORIZATION.json`.

GitHub branch creation, commit, push, PR creation, or repo-backed RubberDuck re-indexing requires either explicit user approval in the current conversation or `AUTO_AUTHORIZATION.json` with external GitHub mutation allowed. `AUTO_AUTHORIZATION.json` must name the allowed remote/repo scope and branch prefix before `AUTO_GITHUB_VALIDATED_BUILD` can push.

Both must include:

```text
sealed_plan_path
sealed_plan_sha256
invoked_under
approved or authorized
timestamp
```

Do not mutate `sealed_plan.json`.
