# Code reference (one page)

Quick map of the `brand_classification` package: what each part does, what goes in and out, how we score the model, and what the tests cover.

## Modules

| File | What it does |
|------|----------------|
| `config.py` | `PROJECT_ROOT`, `DATA_CSV` → `data/brand_task.csv`, `ARTIFACT_DIR` → `artifacts/`. |
| `preprocessing.py` | `clean_text()` fixes whitespace and punctuation; empty string if the value is missing. |
| `data_loader.py` | Reads the CSV (tries a few encodings). Keeps rows with a valid `ADG_CODE` and non-empty `GOOD_NAME`, drops duplicate rows on name+brand+category+code, drops ADG codes with fewer than 2 rows (`MIN_PER_CLASS`) so stratified split works. Builds `text_input` as: `GOOD_NAME [BRAND] … [CAT] …`. |
| `train.py` | Encodes `ADG_CODE` as class indices. Split: 85% train / 15% val, `random_state=42`, stratified. Stack: string input → `TextVectorization` (length 120, lower+strip punctuation) → embedding → bidirectional LSTM(64) → dropout → softmax over classes. Loss: sparse categorical crossentropy. Adam 1e-3. Class weights from sklearn `compute_class_weight("balanced")`. Early stopping on val accuracy; best checkpoint → `artifacts/bilstm_best.keras`. Also saves `bilstm_final.keras`, `label_encoder_classes.json`, `cleaned_training_data.csv`. |
| `evaluate.py` | Loads the frozen cleaned CSV + class JSON, rebuilds the **same** 85/15 split as training. Loads `bilstm_best.keras`, gets softmax probs on the val set. Accuracy = sklearn `accuracy_score` on argmax vs true index. Macro and weighted precision/recall/F1 from `precision_recall_fscore_support` (`zero_division=0`). Top-3: sklearn `top_k_accuracy_score` when it works; otherwise checks by hand if the true class is in the top 3 probs. Also prints train-set accuracy the same way (only to spot overfit). Writes `evaluation_report.txt` with sklearn’s `classification_report`. |
| `predict.py` | Loads best model + classes; builds the same `text_input` shape as training (or you pass `-t`). Returns top-k codes and probabilities. |
| `adg_lookup.py` | Ignores the model. Groups `brand_task.csv` by `ADG_CODE`, counts brands and categories, optional JSON cache under `artifacts/`. |

## Commands → inputs / outputs

| Run | Needs | Produces |
|-----|--------|----------|
| `python -m brand_classification.train` | `data/brand_task.csv` | `bilstm_best.keras`, `bilstm_final.keras`, `label_encoder_classes.json`, `cleaned_training_data.csv` in `artifacts/` |
| `python -m brand_classification.evaluate` | those artifacts | Console + `evaluation_report.txt` |
| `python -m brand_classification.predict` | model + class JSON | stdout |
| `python -m brand_classification.adg_lookup` | CSV (cache optional) | stdout or JSON |

## Metrics (plain language)

**Accuracy:** share of validation rows where the highest softmax score hits the right class index.

**Macro F1 (etc.):** average across classes, each class counted equally; rare classes pull the average down.

**Weighted F1 (etc.):** average weighted by how many validation rows each class has.

**Top-3:** share of rows where the true class is in the three largest probabilities.

Evaluation uses the **same** pseudo-random split as training (same seed and stratify), so it matches that run — it is not a separate randomly drawn test set.

## Dependencies

See `pyproject.toml` (pandas, numpy, scikit-learn, tensorflow). Dev extra adds pytest.

## Tests

`tests/test_smoke.py` only checks imports, paths, `clean_text`, and that `data/brand_task.csv` exists. It does not load TensorFlow or check model accuracy. Run with `pytest` after `pip install -e ".[dev]"`.

## Ops

`.keras` files are usually not in git; after clone you train or copy artifacts in. If column names or layout change, fix `data_loader.py` and retrain. After CSV edits, rebuild ADG lookup cache if you care about those counts.
