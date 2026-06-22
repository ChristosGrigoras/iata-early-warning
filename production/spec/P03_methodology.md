---
authors: [OP48]
primary: OP48
---

# Methodology spec — early-warning signal detection (Phase 3)

Defines *exactly* what we compute and what counts as a "signal," so Phase 4 implementation is mechanical. Builds on `production/brief/P00_early-warning-brief.md` and `research/notes/P02_eda-qa-summary.md`. [OP48]

## 1. Unit of analysis & time base

- **Grain:** monthly series indexed by `ym` (YYYYMM), incident `Date`.
- **Window:** 2011-01 … 2025-12 (79,577 reports).
- **Endpoint caveat:** ASRS has a ~60-day processing lag; the **last 2–3 months are under-reported**. Trailing months are excluded from "signal fired" claims (shown but greyed in plots).

## 2. Data dictionary

Source: `data/processed/asrs.parquet` — **80,047** reports, **127** columns (deduped by `ACN`, 2011–2025 window). Fill rates below are non-empty string counts. [CMP25]

### 2.1 Temporal & geographic limitations (read first)

| Question | Answer |
|----------|--------|
| Exact flight datetime? | **No.** `Date` is **YYYYMM only** (month grain, 100% filled). No day, no clock time. |
| Time-of-day? | **Coarse only.** `Local Time Of Day` is a 6-hour bucket (`0001-0600`, `1201-1800`, …), 89% filled — categorical, not a timestamp. |
| Origin & destination? | **No.** No city-pair, no airport codes, no route endpoints. ASRS de-identifies by design. |
| Where did the event occur? | **Partially.** `Locale Reference` (93%) = facility code (`ZNY.ARTCC`, `ZZZ.Tower`; `ZZZ` = de-identified). `State Reference` (93%) = US state or `US`. |
| Route / approach info? | **Not O&D.** `Aircraft 1 \| Route In Use` (34%) = approach/route *type* (`STAR LLEEO`, `Visual Approach`, `Vectors`), not airports. |

**Implication:** monthly series are the finest temporal grain; no airport-pair or exact-date analysis is possible.

### 2.2 Column groups — well-populated & usable

**Time & place**
| Column | Fill | Notes |
|--------|------|-------|
| `Date` | 100% | YYYYMM — primary time index |
| `Local Time Of Day` | 89% | 6-hour bucket |
| `Locale Reference` | 93% | Facility / ARTCC / tower code |
| `State Reference` | 93% | US state or `US` |

**Event — what went wrong** (core structured signal carriers; several are multi-label — see §3)
| Column | Fill | Notes |
|--------|------|-------|
| `Anomaly` | 99.9% | Multi-label; `; `-joined taxonomy codes |
| `Contributing Factors / Situations` | 99.7% | Multi-label causes |
| `Primary Problem` | 99.7% | Single dominant cause |
| `Person 1 \| Human Factors` | 78% | Multi-label |
| `Detector` | 98% | Who/what detected the event |
| `When Detected` | 93% | Detection timing category |
| `Result` | 96% | Outcome category |

**Aircraft 1** (primary aircraft; `Aircraft 2` ~15% filled, for conflicts only)
| Column | Fill | Notes |
|--------|------|-------|
| `Aircraft 1 \| Make Model Name` | 99.8% | e.g. `B757-200`, `CRJ200` |
| `Aircraft 1 \| Flight Phase` | 96.7% | Multi-label (`Climb`, `Taxi`, …) |
| `Aircraft 1 \| Operating Under FAR Part` | 94% | e.g. `Part 121`, `Part 91` |
| `Aircraft 1 \| Aircraft Operator` | 93% | e.g. `Air Carrier`, `Personal` |
| `Aircraft 1 \| Mission` | 84% | e.g. `Passenger` |
| `Aircraft 1 \| Flight Plan` | 86% | IFR/VFR etc. |
| `Aircraft 1 \| Airspace` | 57% | Airspace class/type |

**Reporter** (reporting-bias checks)
| Column | Fill | Notes |
|--------|------|-------|
| `Person 1 \| Reporter Organization` | 98% | e.g. `Government`, `Air Carrier` |
| `Person 1 \| Function` | 99% | e.g. `Captain`, `Enroute` |
| `Person 1 \| Qualification` | 91% | |
| `Person 1 \| Experience` | 51% | Sparse but usable |

**Free text** (NLP / zero-shot labeller fuel)
| Column | Fill | Notes |
|--------|------|-------|
| `Report 1 \| Narrative` | 100% | Primary narrative — Signal B input |
| `Synopsis` | 100% | Short summary |
| `Report 2 \| Narrative` | 23% | Second reporter when present |

**Metadata**
| Column | Fill | Notes |
|--------|------|-------|
| `ACN` | 100% | Accession number — dedup key |
| `src_year` | 100% | Source CSV year (pipeline-added) |

### 2.3 Column groups — sparse or ignore

- **Entire `(UAS)` block** (~0–1% filled) — drone-specific fields; not viable for this window.
- **`Aircraft 2` maintenance / cabin fields** — near-zero fill.
- **`Latitude / Longitude (UAS)`**, **`Aircraft 1 | Aircraft Zone`** — 0% filled.
- **Altitude, weather detail** — partial (`Altitude.MSL` 43%, `Flight Conditions` 58%, `Ceiling` 16%, `RVR` <1%); usable for sub-slices only, not primary signals.
- **`Person 2` block** — ~20% filled; secondary reporter only.
- **`Unnamed: 125_level_1`** — junk column from trailing CSV comma; drop.

### 2.4 Slicing dimensions available (no O&D)

Because O&D is absent, geographic/route analysis is limited to:
- `State Reference` — US state
- `Locale Reference` — facility type (Tower vs ARTCC vs TRACON)
- `Aircraft 1 | Operating Under FAR Part` — Part 121 air carrier vs Part 91 GA
- `Aircraft 1 | Make Model Name` — aircraft family concentration checks

## 3. Multi-label categorical handling (mandatory)

`Anomaly`, `Contributing Factors / Situations`, `Human Factors`, and `Flight Phase` are `; `-joined multi-label fields (77.8% of `Anomaly` rows are multi-label). For each, **split on `"; "` and explode**, so one report contributes to every category it lists. All category series are built on the exploded form. (The Phase-2 `P02_top_anomalies.png` used exact-string combos and will be regenerated on the exploded form.)

## 4. Reporting-bias normalization (the credibility core)

Raw counts conflate *how much gets reported* with *what is happening*. Total monthly volume swings widely (2019 peak, 2020 COVID trough). Therefore:

- **Primary metric = category share** `s_c(t) = count_c(t) / total_reports(t)` (proportion of that month's reports mentioning category `c`).
- A signal is a **shift in share**, not a shift in raw count — this controls for overall reporting propensity.
- Raw count is retained as a context/secondary view and for the minimum-volume floor.

## 5. Signal A — structured-category share anomaly

For each category `c` with sufficient volume:

- **Min-volume floor:** category must average **≥ 20 reports/month** over the window (drop micro-categories that produce noise).
- **Baseline:** trailing **24-month** window of `s_c`; robust center/scale via **median and MAD** (resistant to spikes).
- **Score:** robust z `= (s_c(t) − median_24) / (1.4826 · MAD_24)`.
- **Thresholds:** `|z| ≥ 2` = *watch*; `|z| ≥ 3` = *strong*.
- **Persistence:** fires only if the threshold is met for **≥ 3 consecutive months** (kills one-off blips).
- **Direction:** early-warning focuses on **rising** share (z > 0); falling shares logged but secondary.
- **Corroboration (optional):** changepoint detection (e.g., Pettitt / `ruptures`) on the share series to date the regime shift.

### 5.1 Bias guards (mandatory before a fire counts)

These rule out the three ways a share shift can be an artifact rather than a real signal. [OP48]

1. **Taxonomy-change guard.** A category whose **first non-zero month is after 2011-01** may reflect an ASRS code being *introduced/renamed* mid-window, not a real rise. Flag any such category (`taxonomy_suspect = true`) and **gate it from "signal" claims** — it may only appear as context with an explicit caveat.
2. **Seasonality guard (YoY).** A 24-month MAD z-score can read a recurring seasonal bump as a signal. Before a fire counts, require the **year-over-year share change** (same month, prior year) to also be positive — i.e. the rise is not explained by the usual same-season pattern. (Transparent and slide-friendly; STL deseasonalization is a heavier fallback if YoY proves too noisy.)
3. **Multiple-testing framing.** With ~30 categories × ~180 months, z≥3 will produce chance hits. Persistence (§5) mitigates, but outputs are framed as **"ranked candidates for human review," not "alarms."** Rank by `peak_z × months_sustained`; the deck presents a shortlist, not automated verdicts.

### 5.2 Output

Per-category table — `category, latest_share, z, yoy_share_delta, taxonomy_suspect, first_fire_ym, months_sustained, peak_z, rank`.

## 6. Signal B — narrative risk signals (NLP)

Independent, free-text view that can surface issues *before* they get a taxonomy code. **Two complementary passes:** a zero-shot labeller (precise, interpretable, the core) and an unsupervised discovery pass (anti-confirmation-bias guard). Text input for both: `Report 1 | Narrative` (100% populated), lightly cleaned (strip ASRS de-identification tokens like `ZZZ`, `[date]`, ACN refs). [OP48]

### 6.1 Core — zero-shot risk classification

> **Implementation update (realized build).** This spec planned a *local GLiNER2* labeller (CPU, free, 205M params) as the zero-shot core. At full-coverage implementation that path measured **~66 h for 80k narratives on CPU** (see `research/notes/P04_signalB-scale-cost.md`), so the labeller was instead run via **OpenRouter → DeepSeek V4 Flash** (`deepseek/deepseek-v4-flash`), concurrent batched calls, across all **79,572** narratives. Only the labelling *engine* changed; everything downstream — the §5 share → robust-z → persistence → bias-guard logic — is identical. Output artifacts keep the `gliner_label_*` filename for historical continuity.

- **Method:** define **~10–15 candidate risk labels** in plain English (e.g. `runway incursion / ground conflict` (the locked headline — see `research/notes/P04_signal-interpretation.md`), `GPS interference / jamming`, `lithium battery / thermal`, `unstabilized approach`, `UAS / drone encounter`, `fatigue`, `automation surprise / mode confusion`, `laser strike`, `wake turbulence`, `ATC staffing / workload`). Zero-shot, no training required (the pilot ran GLiNER2 on CPU with no external API; the realized full run used the hosted DeepSeek V4 Flash labeller — see the §6.1 note).
- **Trend:** for each label, build the **monthly share** of narratives tagged with it → apply the §5 anomaly/persistence/bias-guard logic identically.
- **Why core:** interpretable ("share of reports mentioning X over time"), cheap, on-theme for responsible AI. **Limitation, stated up front:** only finds what we name → confirmation-bias risk, which §6.2 defends against.
- **Calibration:** eyeball ~30 narratives per label to set `cls_threshold` before trusting the series.

#### Verified integration (gliner2 1.3.1, checked 2026-06-19) — *pilot path, superseded at scale by the §6.1 note above* [OP48 | 2026-06-19T00:34+03:00 | P0006]

- **Install:** `pip install "gliner2[local]"` — the `[local]` extra pulls in torch/transformers for local inference (base `pip install gliner2` is cloud-API-client only, **no torch**). Apache-2.0, Python ≥3.8, CPU-first, 205M params.
- **Load:** `from gliner2 import GLiNER2; m = GLiNER2.from_pretrained("fastino/gliner2-base-v1")` (or `gliner2-large-v1`, 340M).
- **Multi-label classify (our use):**
  ```python
  m.classify_text(text,
      {"risk": {"labels": RISK_LABELS, "multi_label": True, "cls_threshold": 0.4}},
      include_confidence=True)
  ```
  Returns per-label hits with confidences; a narrative can carry multiple risk labels (→ same `"; "`-style multi-label handling as §3).
- **Scale:** confirmed `batch_extract_entities(..., batch_size=8)`; for classification, chunk narratives manually (loop batches). On 80k CPU rows this is the runtime-sensitive step — sample stratified-by-year (30–40k) if needed, exactly as §6.2.
- **Pin** the resolved version in `requirements.txt` once installed.

### 6.2 Discovery guard — unsupervised topic pass

- **Method:** sentence-transformer embeddings (`all-MiniLM-L6-v2`, CPU-feasible on 80k; stratified-by-year sample to 30–40k if slow) → lightweight clustering / topic model (BERTopic if install is clean, else `KMeans` + c-TF-IDF).
- **Purpose:** surface themes we *didn't* think to label. Any emergent cluster with persistent positive growth that isn't covered by a §6.1 label becomes a **new candidate label** fed back into the zero-shot labeller.
- **Emergence criterion:** cluster **near-absent in first 2–3 yrs** + **persistent positive growth** with recent acceleration; ranked by growth slope × recency.
- **Interpretability gate:** every reported theme/label needs human-readable top terms **and** 2–3 representative narratives.

**Pipeline:** unsupervised discovery → surfaces candidates → the zero-shot labeller quantifies + trends them (plus the pre-named labels) across all 80k narratives.

## 7. Combining the two views

Strongest early signal = a **narrative theme rising in share that maps onto a rising structured category** (two independent methods agreeing). This cross-validation is the headline the deck should aim for.

## 8. Framing & validation (feeds Phase 5)

**Headline framing = retrospective lead-time proof + a caveated current watchlist.**

- **(a) Retrospective spine (headline):** pick a risk that demonstrably rose, show the detector would have flagged it *months before* it was widely recognized, and validate against external events. Falsifiable and defensible — this is the core story.
- **(b) Current watchlist (one slide):** run the detector on 2024–25 and present the top emerging candidates **clearly caveated** (the ~60-day reporting lag makes the freshest 2 months soft; framed as candidates, not verdicts).

**Validation steps:**

1. **Retrospective lead-time:** for the headline signal, show its share inflected *before* the issue became widely recognized; quantify the lead time.
2. **External corroboration:** Firecrawl pull of NTSB/FAA/news for the candidate theme/time window.
3. **Bias rule-out:** confirm the §5.1 guards pass (not a taxonomy artifact, not seasonal, survives multiple-testing framing) and it isn't a total-volume swing (already mitigated by share-based metric).

## 9. Parameter defaults (single source of truth)

| Param | Default |
|------|---------|
| analysis window | 2011-01 … 2025-12 |
| trailing months excluded from "fired" | last 2 |
| multi-label split token | `"; "` |
| primary metric | monthly category share |
| min avg volume / month | 20 |
| baseline window | 24 months |
| robust score | median + MAD (z) |
| watch / strong z | 2 / 3 |
| persistence | ≥ 3 consecutive months |
| taxonomy-change guard | gate categories with first non-zero month > 2011-01 |
| seasonality guard | require positive YoY share change before a fire counts |
| multiple-testing stance | ranked candidates for human review (not alarms); rank = peak_z × months_sustained |
| narrative core | zero-shot LLM, ~10 risk labels — realized: OpenRouter DeepSeek V4 Flash (`deepseek/deepseek-v4-flash`); pilot: local GLiNER2 |
| narrative discovery guard | embeddings (all-MiniLM-L6-v2) + BERTopic/KMeans |
| embeddings | all-MiniLM-L6-v2 |

## 10. Phase 4 build plan (notebooks)

- `P04_02-structured-signals.ipynb` — Signal A: exploded category share series, robust-z anomaly + persistence + §5.1 bias guards, ranked candidate table + plots. **(Build first.)**
- `P04_03-narrative-signals.ipynb` — Signal B: zero-shot LLM labels (realized: OpenRouter DeepSeek V4 Flash; see §6.1 note) → monthly share trends (§6.1), plus unsupervised discovery pass (§6.2) for unnamed emergents.
- `04-combine-validate.ipynb` — cross-view agreement, retrospective lead-time headline + current watchlist, external corroboration.

## Decisions log

- **Share over raw count** — chosen to neutralize reporting-volume bias (the central caveat); raw counts kept only as context.
- **Robust z (median/MAD) over mean/std** — baseline must not be inflated by the very spikes we hunt.
- **Persistence ≥ 3 months** — favors *sustained emergence* over noise; aligns with "early-warning," not "alarm."
- **Three bias guards (taxonomy-change, YoY seasonality, ranked-candidates framing)** — rule out the artifacts a skeptic will probe; "candidates not alarms" is honest and on-theme for responsible AI. [OP48]
- **Retrospective headline + caveated watchlist** — proves the method on a falsifiable past signal, then shows it runs live. [OP48]
- **Signal B = zero-shot-LLM-led core + unsupervised discovery guard** — interpretable, with the unsupervised pass defending against "only finds what you name." Lighter than full BERTopic tuning. [OP48]
- **Pilot → scale pivot (Signal B labeller)** — spec'd on local GLiNER2 (free, CPU) for the method demo; at full coverage the ~66 h CPU runtime made it impractical, so the labeller was run via **OpenRouter DeepSeek V4 Flash** for all 79,572 narratives. Cheap hosted inference, not local CPU, was the right tool once full coverage mattered; the detector logic is unchanged either way. [OP48]
