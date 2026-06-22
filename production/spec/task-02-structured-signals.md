---
authors: [OP48]
primary: OP48
---

# Task brief — build `02-structured-signals.ipynb` (Signal A)

**For:** CDX53 (implementation). **Spec of record:** `production/spec/methodology.md` §3–§5 + §9 parameter table. This brief is the build checklist; the spec wins on any conflict. [OP48]

## Inputs / outputs

- **Input:** `data/processed/asrs.parquet` (80,047 reports, 127 cols; `Date` = YYYYMM string).
- **Notebook:** `production/build/02-structured-signals.ipynb` (Polars-first, matplotlib).
- **Artifacts → `production/output/signals/`:**
  - `signal_candidates.csv` — ranked table (schema below)
  - `category_share_series.parquet` — tidy long series for reuse by `04`
  - one trend PNG per top-ranked candidate (share + baseline band + fire markers)
  - `signalA_summary.md` — 5–8 bullet plain-English readout
- **Provenance:** first cell `# provenance: primary=OP48 authors=[OP48, CDX53]` (CDX53 wrote the code, OP48 specified it).

## Robust ROOT pattern (reuse from 01-eda)

```python
from pathlib import Path
ROOT = Path.cwd()
if not (ROOT / "data" / "processed" / "asrs.parquet").exists():
    ROOT = ROOT.parent.parent
```

## Steps

1. **Load + window.** Read parquet; parse `Date`→`ym` (YYYYMM int) and a datetime for plotting; keep 2011-01…2025-12. Compute `total_reports(t)` per `ym`.
2. **Explode multi-label fields.** For each of `Anomaly`, `Contributing Factors / Situations`, `Person 1 | Human Factors`, `Aircraft 1 | Flight Phase`: split on `"; "`, trim, drop empties, explode. Process each field as its own category family (keep a `field` column so they don't collide).
3. **Monthly share series.** For each (field, category): `count_c(t)` then `s_c(t) = count_c(t) / total_reports(t)`. Emit tidy long frame `field, category, ym, count, share`.
4. **Min-volume floor.** Keep categories averaging **≥ 20 reports/month** over the window.
5. **Robust-z anomaly.** Trailing **24-month** rolling median + MAD of `share`; `z = (share − median) / (1.4826·MAD)` (guard MAD==0 → z=0/NaN, don't divide by zero).
6. **Persistence + thresholds.** Flag months with `z ≥ 2` (watch) / `z ≥ 3` (strong), **rising only** (z>0). A category "fires" when threshold met **≥ 3 consecutive months**; record `first_fire_ym`, `months_sustained`, `peak_z`.
7. **Bias guards (§5.1).**
   - `taxonomy_suspect = (first non-zero month > 2011-01)` → keep but gate from headline claims.
   - `yoy_share_delta = share(t) − share(t-12)`; require **> 0** at the fire month for the fire to "count."
   - Exclude trailing **2 months** from "fired" claims (still plot them, greyed).
8. **Rank.** `rank` by `peak_z × months_sustained` (desc). Build `signal_candidates.csv` with:
   `field, category, latest_share, z_latest, yoy_share_delta, taxonomy_suspect, first_fire_ym, months_sustained, peak_z, rank`.
9. **Plots.** For the top ~6 non-taxonomy-suspect rising candidates: share line + 24-mo median band + fire-month markers; clean year x-axis (reuse the `mdates.YearLocator` fix from 01-eda); greyed trailing 2 months.
10. **Readout.** `signalA_summary.md`: top candidates, which fired, which are taxonomy-suspect, any seasonal rejections — framed as **candidates for human review, not alarms**.

## Acceptance checks

- Shares per `ym` per field sum to ≥1 (multi-label, so >1 expected) — sanity, not equality.
- No divide-by-zero; MAD==0 handled.
- Re-running is deterministic; artifacts land in `production/output/signals/`.
- Notebook executes clean via `nbconvert --execute` → commit `02-structured-signals.executed.ipynb`.

## Out of scope (later notebooks)

- NLP / GLiNER2 (→ `03`), cross-view + external corroboration (→ `04`). Do **not** pull these in.

## Open implementation choices (CDX53 decides, note them)

- Rolling MAD impl (manual vs `rolling_map`) — pick what's clean in Polars.
- Whether to require a **minimum baseline length** (e.g. skip fires before month 24 where the 24-mo window is incomplete) — recommended yes; note the cutoff.
