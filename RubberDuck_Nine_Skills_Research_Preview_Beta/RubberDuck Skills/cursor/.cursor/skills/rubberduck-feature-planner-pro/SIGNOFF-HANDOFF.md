# Signoff Handoff

PLAN mode ends with a signoff handoff.

Generate:

```text
SIGNOFF_TEMPLATE.json
```

Example:

```json
{
  "sealed_plan_path": "./uc06/<slug>/sealed_plan.json",
  "sealed_plan_sha256": "<computed>",
  "approved": false,
  "approved_by": "USER",
  "approved_at": "",
  "invoked_under": "USER"
}
```

BUILD mode requires `SIGNOFF.json` or `AUTO_AUTHORIZATION.json`.
