# Feature Atlas Mode

Use `FEATURE_ATLAS` when the user specifies a feature, endpoint, module, behavior, issue, user journey, class, function, or file.

Default remains `WHOLE_REPO_ATLAS`.

## Operating rule

Do not run the entire deep whole-repo Atlas first when the user asks only for a feature. Gather enough repo intelligence to avoid tunnel vision, then center the Atlas on the requested feature.

## Required output

```text
feature description
feature entry points
symbols involved
call chains
data flow
state/config/dependencies
tests likely covering it
external integrations
unsupported surfaces affecting the feature
what to read first
confidence
unknowns
falsification recipes
```

## Evidence expectations

Use:

```text
search_code for feature names, routes, handlers, symbols, tests
symbols_overview on feature files and immediate neighbors
call_chain for feature entry points
trace_variable for feature request/state/config/data objects
read_source only for compact anchors
tool-health and unsupported-surface checks scoped to the feature
```

The feature report still needs:

```text
not-a-security-audit framing when security-sensitive flows appear
evidence/evidence-manifest.md
evidence/atlas-summary.json
evidence/falsification-recipes.md
claim ledger and negative claims
```

