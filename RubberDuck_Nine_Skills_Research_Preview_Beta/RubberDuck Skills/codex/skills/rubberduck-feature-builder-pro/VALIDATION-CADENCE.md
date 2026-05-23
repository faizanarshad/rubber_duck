# Validation Cadence

Run `validate_generated_diff`:

```text
every pulse_cadence writes
after high-risk writes
before crossing from tests to production
before final seal
```

Prefer event-based cadence over wall-clock cadence.
