# Tool Health Sentinel

Record:

```text
repo/commit
RubberDuck codebase intelligence status
semantic intelligence status
before/after analysis IDs
parser degradation
unsupported language
dynamic dispatch
unresolved calls
source-only fallback
runtime/test availability
tool failures
```

Tool degradation affects verdict confidence.

If tool health blocks path comparison, use:

```text
UNDECIDABLE
```

or:

```text
HEURISTIC_ONLY
```

not `PROVEN_EQUIVALENT_UNDER_CONTRACT`.
