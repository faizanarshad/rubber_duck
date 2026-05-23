# Sealed Plan Schema

`sealed_plan.json` is immutable after PLAN mode.

Required top-level fields:

```text
schema_version
plan_type
repo
base_commit
feature_title
feature_description
session_id
fit_pack_id
fit_pack_sha256
planned_files
off_limits_files
planned_symbols
reusable_symbols
existing_patterns
pattern_anchors
acceptance_criteria
test_plan
test_diff_path
effect_manifest
command_plan
generation_constraints
negative_scope
fit_pack_gaps
tool_health
amendments
sealed_at
plan_sha256
```

No mutable signoff state belongs in the sealed plan.
