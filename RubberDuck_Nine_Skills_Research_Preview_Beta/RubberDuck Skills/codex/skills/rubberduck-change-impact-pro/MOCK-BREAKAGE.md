# Mock Breakage Taxonomy

Classify test/mock impacts by break mode.

## Mock/site types

```text
auto-mock module path
factory mock with explicit exports
vi.mocked(symbol).mockResolvedValue(...)
jest.mocked(symbol)
post-import symbol mock
spyOn(object, "method")
manual fake implementation
snapshot / fixture
```

## Break taxonomy

```text
breaks loudly
breaks silently
survives with alias
requires factory update
requires import update
requires fixture update
```

## Output

```text
§7 Mock Breakage Taxonomy
```

Table:

| Test/mock site | Type | Current symbol | Break mode | Required change |
|---|---|---|---|---|
