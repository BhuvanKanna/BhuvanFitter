# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BhuvanFitter** — distribution fitting + Truncation Index (TI) toolkit for CRISPR/transposon overexpression screen data. The code runs in Google Colab; the source of truth is `bhuvanfitterpierce.py`, treated as a regular Python file.

## Git Hygiene

Commit and push to GitHub regularly during any work session — after each meaningful change, not just at the end. This ensures work is never lost and the history is readable.

- Commit after completing each logical unit of work (a new function, a bug fix, a refactor).
- Write specific commit messages that describe what changed and why (e.g. "Fix baseline subtraction in ti_fourparam_height_ratio", not "Update code").
- Never leave a session with uncommitted changes to `bhuvanfitterpierce.py`.

## Architecture

All logic lives in `bhuvanfitterpierce.py`, structured as 15 sections:

**Core library (§1–7):** Pure Python/NumPy — no Colab dependency.
- `_fourparam_gaussian` — module-level (required by `curve_fit`)
- `_truncated_gaussian_nll`, `_fit_mle_truncated` — MLE internals
- `BhuvanFitter` class — main API; takes `(data, gene_name, bins, x_max)`
- `has_minus_one_peak` — sentinel detection
- `compute_mle_table`, `compute_fourparam_table` — batch runners
- `plot_truncation_index_distribution` — histogram + ranked bar chart of `ti_mle_sigma_dist` across all genes

**Fitting models:**
- `"fourparam"` — 4-param Gaussian on histogram counts (NLS/TRF, `soft_l1` loss). Fast; biased because fit anchors to truncated data.
- `"mle"` — right-truncated Gaussian on raw values (Nelder-Mead + BFGS fallback). Recovers true μ, σ.

**Truncation Index naming convention (parallel across both models):**

| Metric | fourparam | mle |
|---|---|---|
| σ-distance | `ti_fourparam_sigma_dist` | `ti_mle_sigma_dist` |
| Height ratio | `ti_fourparam_height_ratio` | `ti_mle_height_ratio` |

**Colab runtime sections (§8–15):** Contain Drive mounts, CSV/parquet loads, single-gene examples, batch runs, gene-set lists, and isoform analysis (`analyze_best_isoforms`). These sections import `google.colab` — they cannot run outside Colab.

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
