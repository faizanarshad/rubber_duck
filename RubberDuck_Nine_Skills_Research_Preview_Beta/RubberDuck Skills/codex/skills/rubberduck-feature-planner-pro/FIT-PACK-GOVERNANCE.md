# Fit Pack Governance

Fit Pack output is high-value but can be lexically biased.

Always record:

```text
fit_pack_id
session_id
raw fit_pack path
suggested locations
suggested reusable symbols
duplicate risks
generation constraints
locations to avoid
```

Then challenge it with semantic enrichment:

```text
search_code for similar functionality
symbols_overview for integration files
call_chain on candidate integration points
trace_variable for core state/config values
read_source for canonical patterns
```

Report:

```text
Fit Pack suggested:
Semantic enrichment added:
Fit Pack missed:
Final decision:
```
