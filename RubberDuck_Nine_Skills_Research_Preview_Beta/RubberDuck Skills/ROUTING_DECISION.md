# RubberDuck Skill Routing Decision

Use the first matching rule in this precedence order when a prompt could trigger multiple RubberDuck skills:

1. `sealed_plan.json` plus a build/implementation request -> `rubberduck-feature-builder-pro`
2. autonomy envelope, autonomous plan-and-build, or bounded auto mode -> `rubberduck-autonomous-feature-mode`
3. equivalence, replacement, refactor preservation, or before/after behavior drift -> `rubberduck-mirror-pro`
4. duplicate intent, duplicate behavior, behavior twins, or doppelganger search -> `rubberduck-doppelganger-hunt-pro`
5. schema, type, database, API contract, generated client, nullability, or validation drift -> `rubberduck-schema-code-api-drift-pro`
6. security audit, vulnerability hunt, pentest, CWE/CVE, scanner-finding validation, or defensible security report -> `rubberduck-security-audit`
7. target change impact, blast radius, affected callers/callees, tests to run, or safe change order -> `rubberduck-change-impact-pro`
8. feature planning, tests-first planning, sealed plan creation, or signoff-ready plan -> `rubberduck-feature-planner-pro`
9. codebase understanding, architecture map, entry points, call chains, data flow, onboarding, or Codebase Atlas -> `rubberduck-codebase-atlas-pro`

Deterministic QA prompts:

| Prompt | Expected skill |
|---|---|
| Get to know this repo and map the architecture. | `rubberduck-codebase-atlas-pro` |
| Run a security audit of this repository. | `rubberduck-security-audit` |
| What breaks if I modify this function? | `rubberduck-change-impact-pro` |
| Find duplicate behavior or duplicate intent in this repo. | `rubberduck-doppelganger-hunt-pro` |
| Can I replace this implementation with that one? | `rubberduck-mirror-pro` |
| Find drift between DB schema, code types, and API contracts. | `rubberduck-schema-code-api-drift-pro` |
| Plan tests first for this feature. | `rubberduck-feature-planner-pro` |
| Build from this sealed_plan.json. | `rubberduck-feature-builder-pro` |
| Run plan and build under this autonomy envelope. | `rubberduck-autonomous-feature-mode` |

