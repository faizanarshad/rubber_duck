# Input Contracts

## Required fields

```text
before_spec
after_spec
mode
preserved_contract
repo/path/commit
```

## before_spec / after_spec forms

Accept:

```text
file:function
analysis_id:function
commit:path:function
raw code snippet
diff hunk
branch/commit pair
```

If ambiguous, resolve candidates with search and symbols. Ask only if multiple candidates remain plausible after tool resolution.

## Preserved contracts

```text
observable-behavior
outputs-only
side-effects-only
exception-envelope
full-functional
test-suite-compatible
```

If unspecified, default to `observable-behavior` and state the assumption.

## Out-of-scope effects

Allow explicit exclusions, e.g.:

```text
logging differences out of scope
timing differences out of scope
error message exact text out of scope
```

Do not silently exclude effects.
