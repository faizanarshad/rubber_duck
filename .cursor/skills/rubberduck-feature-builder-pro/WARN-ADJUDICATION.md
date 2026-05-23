# WARN Adjudication

Every WARN from `validate_generated_diff` becomes RED until adjudicated.

Create:

```text
WARN_ADJUDICATION.json
```

Each warning:

```text
warning_id
class
verdict: false_positive | accepted_risk | must_fix
evidence
blocks_completion
```
