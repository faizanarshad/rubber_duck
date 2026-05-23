# Import and Module Context

Equivalent bodies can behave differently because imports or ambient module context differ.

Inspect:

```text
imported functions/classes
aliased imports
module-level constants
global mutable state
export/public status
runtime/framework decorators
ambient environment reads
test helpers
resource constructors
```

Output table:

```text
Name | BEFORE binding | AFTER binding | Behavior relevance | Evidence
```

Required if:

```text
before and after live in different files
different language/module
different test/prod boundary
different imports
helper names are same but bindings differ
```
