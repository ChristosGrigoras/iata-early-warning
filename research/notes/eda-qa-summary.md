---
authors: [OP48]
primary: OP48
---

# EDA QA summary (Phase 2)

Generated from `production/build/01-eda.ipynb` against `data/processed/asrs.parquet`. [OP48]

## Dataset sanity

- Raw rows: **80,047**
- QA analysis window rows (2011-01..2025-12): **79,577**
- Unique ACNs in QA window: **79,577** (no duplicate ACNs inside window)
- Trimmed outside-window rows: **470** (mostly Jan-2026 overlap edge + rare out-of-window dates)

## Key QA findings

- **Top anomaly class:** `Aircraft Equipment Problem Critical` (**6,577** reports in QA window).
- Missingness is heavily concentrated in:
  - Aircraft-2 fields (expected for single-aircraft reports),
  - UAS-specific fields (sparse by design in mixed-era data),
  - trailing unnamed column (`Unnamed: 125_level_1`) = all-empty artifact from export schema.
- Reporting volume shows clear month-to-month volatility with noticeable spike periods (see `monthly_spikes_top10.csv`).
- Text quality is high enough for NLP:
  - `Report 1 | Narrative` complete in all rows in the combined dataset pipeline,
  - `Synopsis` effectively complete.

## Produced artifacts

In `production/output/eda/`:

- `monthly_volume_trend.png`
- `top_anomalies.png`
- `phase_model_concentration.png`
- `reporting_bias_proxies.png`
- `missingness_top25.csv`
- `monthly_spikes_top10.csv`
- `qa_summary.csv`

## Known caveat — multi-label categorical fields [OP48]

`Anomaly` is **multi-valued**: 77.8% of reports carry `; `-joined labels. The Phase-2 `top_anomalies.png` chart groups **exact-string combinations**, so it understates true category frequency and mis-ranks. After splitting on `; `, the true top categories are:

1. `Deviation / Discrepancy - Procedural …` ≈ 40,327
2. `Aircraft Equipment Problem Critical` ≈ 19,185 (vs. 6,577 as an exact string)
3. `ATC Issue All Types` ≈ 16,150
4. `Aircraft Equipment Problem Less Severe` ≈ 13,845
5. `Inflight Event / Encounter Weather/Turbulence` ≈ 6,824; `Conflict NMAC` ≈ 5,921

The same multi-label structure applies to `Contributing Factors / Situations`, `Human Factors`, and `Flight Phase`. **Phase 3/4 must split these on `; ` before counting or building category time series.**

## Implication for Phase 3

The data is sufficiently stable for signal-method design. Priority next step is to formalize:

1. baseline normalization choices for volume anomalies (to reduce reporting-bias effects),
2. category-level signal thresholds (statistical + operational),
3. narrative-theme emergence criteria (growth + persistence + interpretability).
