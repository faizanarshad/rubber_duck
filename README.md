# rubber_duck

Product–brand classification data: retail goods with normalized brand labels and high-level categories.

## Data

| File | Description |
|------|-------------|
| `brand_task.csv` | Rows of product lines with codes, display names, inferred **brand**, and **category**. |

### Columns

- **ADG_CODE** — Product or line code (may be empty for some rows).
- **GOOD_NAME** — Product description / label.
- **BRAND** — Brand name (or `Unknown` when not assigned).
- **CATEGORY** — Coarse category (e.g. Beverages, Food Products, Household).

## Usage

Open `brand_task.csv` in any spreadsheet tool, or load it in Python/pandas for modeling or evaluation.

```python
import pandas as pd

df = pd.read_csv("brand_task.csv")
print(df.head())
```

## License

Add a license if you redistribute this dataset publicly.
