# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BhuvanFitter** — distribution fitting + Truncation Index (TI) toolkit for CRISPR/transposon overexpression screen data. Runs in Google Colab as a `.ipynb` notebook.

The primary source of truth is `bhuvanfitterpierce.py`. The `.ipynb` version is generated from it (via `convert_to_nb.py`) only when pushing to GitHub.

## Workflow

Edit the project as `bhuvanfitterpierce.py`. To save a versioned snapshot to GitHub, run:

```
/checkpoint
```

This converts the `.py` to `.ipynb`, commits both with a descriptive message, and pushes to `origin/main`.

## Generating the Notebook

```bash
python convert_to_nb.py bhuvanfitterpierce.py bhuvanfitterpierce.ipynb
```

Requires only the Python standard library. The script parses Colab-style standalone triple-quoted strings as Markdown cells and all other top-level code as code cells.

## Architecture

All logic lives in `bhuvanfitterpierce.py`, structured as 15 notebook sections:

**Core library (§1–6):** Pure Python/NumPy — no Colab dependency.
- `_fourparam_gaussian` — module-level (required by `curve_fit`)
- `_truncated_gaussian_nll`, `_fit_mle_truncated` — MLE internals
- `BhuvanFitter` class — main API; takes `(data, gene_name, bins, x_max)`
- `has_minus_one_peak` — sentinel detection
- `compute_mle_table`, `compute_fourparam_table` — batch runners

**Fitting models:**
- `"fourparam"` — 4-param Gaussian on histogram counts (NLS/TRF, `soft_l1` loss). Fast; biased because fit anchors to truncated data.
- `"mle"` — right-truncated Gaussian on raw values (Nelder-Mead + BFGS fallback). Recovers true μ, σ.

**Truncation Index naming convention (parallel across both models):**

| Metric | fourparam | mle |
|---|---|---|
| σ-distance | `ti_fourparam_sigma_dist` | `ti_mle_sigma_dist` |
| Height ratio | `ti_fourparam_height_ratio` | `ti_mle_height_ratio` |

**Colab runtime sections (§7–15):** Contain Drive mounts, CSV/parquet loads, single-gene examples, batch runs, gene-set lists, and isoform analysis. These sections import `google.colab` — they cannot run outside Colab.

## Key Constraints

- `_fourparam_gaussian` must stay at module scope — `curve_fit` cannot pickle instance methods.
- MLE optimises `log(σ)` to enforce σ > 0 without box constraints.
- Genes with < 10 observations are skipped (`fit_success=False`) in batch functions.
- Sentinel value `-1` means "not expressed"; use `has_minus_one_peak` to flag genes where ≥ 20% of values ≤ −0.75 before fitting.

## Required Google Drive Files (Colab only)

| File | Drive Path |
|---|---|
| `Supplementary Data 1_csv.csv` | `MyDrive/` |
| `Supplementary Data 1 trunc 20250702.xlsx` | `MyDrive/` |
| `fourparam_table.parquet` | `MyDrive/bhuvan research project/` |
| `mle_table.parquet` | `MyDrive/bhuvan research project/` |
| `genes_of_interest.json` | `MyDrive/bhuvan research project/` |
