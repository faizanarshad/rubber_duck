# Target Resolution

Resolve the requested change target before impact analysis.

## Inputs

Possible user inputs:

```text
function name
class name
file path
symbol
method
description of behavior
diff/branch/commit
```

## Resolution workflow

1. Search exact symbol:

```python
search_code(pattern="<target>")
```

2. Load candidate file(s):

```python
load_code(file_path="<path>")
```

3. Run symbols:

```python
query_action(action="symbols_overview", analysis_id="<aid>")
```

4. Read target source:

```python
read_source(analysis_id="<aid>", function_name="<target>")
```

5. If multiple candidates exist, rank by:
   - exact name match,
   - file path match,
   - exported/public status,
   - production vs test/dev location,
   - caller count,
   - match to change description.

## Ask-once rule

Ask only if multiple plausible production targets remain and the change cannot proceed safely.

Otherwise proceed with:

```text
Target confidence: high / medium / low
Assumption:
How to refute:
```

## Target resolution output

```text
target symbol
file:line
analysis_id
production/test/dev zone
public/internal status
confidence
alternative candidates
why selected
```
