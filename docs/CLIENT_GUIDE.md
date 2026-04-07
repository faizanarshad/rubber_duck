# Client guide

If you just need to run the thing: put your CSV in place, use a venv, run the commands below from the repo root. You don’t need to read the Python unless something breaks.

### What you get

Train a classifier that maps product text to `ADG_CODE`, check numbers on a held-out slice, run predictions on new lines, or look up “which brand/category shows up most often for this ADG” straight from the spreadsheet (that last part is counting rows, not the neural net).

### Setup

Python 3.9+. Open a terminal in `brand_detection_armenian_data`, then:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install -e .
```

Tests (optional): `pip install -e ".[dev]"` then `pytest`.

### Data

File: `data/brand_task.csv`  
Columns: `ADG_CODE`, `GOOD_NAME`, `BRAND`, `CATEGORY`.

### Commands (venv on, cwd = repo root)

Train — writes models and side files under `artifacts/`:

```bash
python -m brand_classification.train
```

Evaluate — prints metrics, writes `artifacts/evaluation_report.txt`:

```bash
python -m brand_classification.evaluate
```

Predict — example:

```bash
python -m brand_classification.predict -n "Product Name" -b "Brand" -c "Category" --top-k 5
```

Lookup by ADG (counts in the CSV):

```bash
python -m brand_classification.adg_lookup 2101
```

After you replace the CSV, refresh the lookup cache:

```bash
python -m brand_classification.adg_lookup --rebuild-cache
```

### Where things live

`data/` = input. `src/brand_classification/` = code. `artifacts/` = outputs (models, reports). `docs/` = these notes.

### When something goes wrong

`python` missing → try `python3`.  
Predict/evaluate complains about a missing model → run train first (or drop a `bilstm_best.keras` into `artifacts/` if someone gave you one).  
You changed the data and numbers look stale → train again; for lookup only, `--rebuild-cache`.

For the technical picture (metrics, split, files), see `CODE_OVERVIEW.md`.
