---
authors: [OP48]
primary: OP48
---

# ASRS — data source notes

## What it is

NASA **Aviation Safety Reporting System (ASRS)**: a voluntary, confidential, non-punitive incident-reporting system. Reports are submitted by aviation professionals — pilots, air traffic controllers, dispatchers, maintenance, cabin crew — describing safety-related events and concerns.

- **Search / database:** https://asrs.arc.nasa.gov/search/database.html
- **Output:** structured fields (date, location, aircraft, flight phase, event type, contributing factors, etc.) + a rich **free-text narrative** and **synopsis** per report.

## Why it suits "early-warning"

- Narratives often describe *near-misses* and *latent hazards* before they cause accidents — a leading indicator vs. lagging accident statistics.
- Free text → NLP (embeddings, clustering, topic modelling) can surface **emerging themes** as they rise in frequency.
- Structured fields → time-series **trend / anomaly detection** on counts by category, aircraft, phase of flight.

## Caveats (must state in the analysis)

- **Reporting bias:** counts reflect *who chooses to report*, not true incident rates. Spikes can be reporting-driven (awareness campaigns, policy changes), not safety-driven.
- **Voluntary & de-identified:** dates/locations can be coarse; no exhaustive coverage.
- Use as **signal**, not ground truth — corroborate with external sources where possible (NTSB, FAA, weather).

## Data access decision (verified 2026-06-18)

**Use the native DBOL CSV export — not scraping/Firecrawl — for the core dataset.** [OP48]

- **DBOL** supports direct export to **CSV / XLS / Word** with user-selected fields (structured codes + sanitized narratives). Source: https://asrs.arc.nasa.gov/search/database.html and /search/dbol/strategies.html
- **Limit: 10,000 records per download** → chunk large pulls by **date range** (or category) and concatenate.
- **Report Sets** (30 topic PDFs, 50 records each, https://asrs.arc.nasa.gov/search/reportsets.html) — qualitative context only, not bulk analysis.
- ⚠️ NASA is **changing the underlying DB structure** (user-input window closed 2026-06-10). **Pin the export date and archive the raw CSVs** for reproducibility; schema may shift later.
- **Firecrawl** (we have a subscription) is reserved for **Phase 5 external corroboration** (NTSB, FAA, news, weather), not the primary ASRS pull. Automating DBOL itself is fiddly (pop-up form app) — only if manual export becomes a bottleneck.

## Export recipe (DBOL) — broad pull, ~2011–2025

**Target:** all categories, Jan 2011 – Dec 2025, structured fields + narratives. [OP48]

**Where:** ASRS Database Online → https://asrs.arc.nasa.gov/search/database.html (turn off pop-up blocker).

**Query:** filter on **Date of Incident** only (no other coded filters → "all categories"). Leave all other fields blank.

**Chunking (10k-record cap):**
1. Start with a candidate window (e.g. 1 year). Run the search; note the result count.
2. If a window returns **> 10,000**, halve it (year → 6 months → quarter) until each chunk is ≤10k.
3. Cover 2011–2025 with contiguous, non-overlapping chunks. Record each chunk's exact date range + count.

**Fields to export:** select a consistent field set across *every* chunk (so schemas concatenate cleanly). Minimum:
- Date (year/month), Locale/region (if available)
- Aircraft (make/model, operator type), Flight phase
- Event type / Anomaly, Contributing factors, Detector, Result
- **Synopsis** and **Narrative** (free text — required for the NLP signal)

**Format:** **CSV**. Export each chunk; name `asrs_<startYYYYMM>_<endYYYYMM>.csv`.

**Reproducibility:** record **export date** and a note that NASA may change the DB structure; archive raw CSVs unchanged.

## VERIFIED extraction method (2026-06-18) [OP48]

Validated end-to-end on Jan 2025 (**926 reports → 2.45 MB CSV**, saved `data/raw/asrs_202501.csv`).

1. **Query Wizard:** `https://asrs.arc.nasa.gov/search/dbol.html` → redirects to `https://akama.arc.nasa.gov/ASRSDBOnline/QueryWizard_Filter.aspx`.
2. Click the **Date of Incident** `[date]` placeholder → popup `QueryWizard_DatePopup.aspx`; set Begin/End year+month; Save (`input[name=SaveButton]`).
3. **Run Search** (`input[src*=RunSearchButton]`; ASP.NET image button — submit form with synthetic `<name>.x/.y` fields). → `QueryWizard_Results.aspx` shows the ACN count.
4. **Export:** in the same session, `fetch('https://akama.arc.nasa.gov/ASRSDBOnline/QueryWizard_ExportExcel.aspx?ExportType=CSV', {credentials:'include'}).then(r=>r.text())`. **Session-dependent** — direct hit without a prior search errors out.

### CSV schema
- **126 columns, TWO header rows:** row 1 = category group (Time, Place, Environment, Aircraft 1, Component, Aircraft 2, Person 1, Person 2, Events, Assessments, Report 1, Report 2); row 2 = field names. Data starts after a blank line.
- **Key fields:** `ACN`, `Date` (YYYYMM), `Flight Phase`, `Make Model Name`, `Anomaly`, `Detector`, `When Detected`, `Result`, `Contributing Factors / Situations`, `Primary Problem`, `Human Factors`, `Narrative`, `Synopsis`. Note duplicate field names across Aircraft 1/2 and Person 1/2 groups — disambiguate using the group header row.

### Volume / chunking
- ~460–930 reports/month → **chunk at ~6 months** to stay under the 10k export cap (~30 chunks for 2011–2025).

## Storage

- Raw chunks → `data/raw/` (gitignored). Combined → `data/processed/asrs.parquet`.
- A loader (Polars) concatenates `data/raw/*.csv`, normalises columns, dedupes by record id, writes the parquet — see Phase 2 (CDX53 task).

## Acquired dataset (2026-06-18) [OP48]

- **15 yearly CSV chunks** (Jan Y → Jan Y+1, 1-month overlap) in `data/raw/asrs_2011.csv … asrs_2025.csv` (~224 MB). Export counts: 2011=6109, 2012=5397, 2013=4741, 2014=5031, 2015=6472, 2016=5921, 2017=5660, 2018=6213, 2019=6830, 2020=5459, 2021=5005, 2022=5845, 2023=4996, 2024=5867, 2025=6585.
- **Combined → `data/processed/asrs.parquet`**: built by `production/build/P01_build_dataset.py` (pandas 2-row-header parse → flatten → dedupe ACN → Parquet). **80,047 unique reports, 127 columns.**
- **Coverage:** incident `Date` (YYYYMM) spans 2011–2025 (+ Jan-2026 overlap edge, 469; one stray 2002-dated late report). `Synopsis` 100% populated; **`Report 1 | Narrative` 100%**, `Report 2 | Narrative` 22.8%.
- **Column naming:** duplicate field names across groups are prefixed, e.g. `Report 1 | Narrative`, `Report 2 | Narrative`, `Aircraft 1`/`Aircraft 2` fields. `ACN`, `Date`, `Synopsis` are unprefixed (globally unique). Added `src_year` (source chunk).
- **Rebuild:** `. .venv/bin/activate && python production/build/P01_build_dataset.py`.

## TODO (data acquisition) — DONE

- [x] Phase 0 scope: broad, 2011–2025.
- [x] Chunked CSV exports (browser + in-session fetch); counts logged above.
- [x] Loader run; combined = 80,047 unique ACNs, 127 cols → `data/processed/asrs.parquet`.
