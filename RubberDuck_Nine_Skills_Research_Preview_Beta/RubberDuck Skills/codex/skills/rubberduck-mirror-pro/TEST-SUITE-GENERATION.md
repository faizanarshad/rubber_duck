# Test Suite Generation

Before generating tests, detect test framework:

```text
package.json
pyproject.toml
pytest.ini
vitest/jest/mocha configs
existing nearby tests
```

If no framework is found, generate standalone pseudo-tests and label them.

Test output:

```text
test name
framework
setup
input
expected BEFORE behavior
expected AFTER behavior
purpose
```

For NOT_EQUIVALENT, include at least one failing replacement test if possible.
