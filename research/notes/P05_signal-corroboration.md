---
authors: [OP48]
primary: OP48
prov_id: P0010
prov_ts: 2026-06-19T02:58+03:00
---

# Signal corroboration & validation — surface/ground-conflict signal (Phase 5)

Validates the locked headline (`research/notes/P04_signal-interpretation.md`) against external public sources, quantifies the lead time, confirms the cross-view agreement, and records the bias rule-outs. [OP48 | 2026-06-19T02:58+03:00 | P0010]

## The signal (internal, from our pipeline)

- **Signal A (structured share):** `Anomaly → Conflict Ground Conflict` rose ~4–5% (2011–19) → 6.7% (2021) → 7.0% (2022) → **9.0% (2023) → 11.2% (2024)** → 10.5% (2025); corroborated by `Flight Phase → Taxi` (~8–11% → 15.2% 2024). Category is present since 2011 (`taxonomy_suspect = False`) — not an artifact.
- **Signal B (narrative, full 79,572-run via DeepSeek V4 Flash):** label `runway incursion / ground conflict / surface movement` registers a persisted **watch fire with `first_fire_ym = 202106`** (June 2021). Two independent methods agree. [OP48 | 2026-06-19T02:58+03:00 | P0010]

## External corroboration (dated)

| Date | Event / figure | Source |
|------|----------------|--------|
| Early 2023 | "A series of incidents at large commercial airports … aircraft came significantly close on runways." | DOT OIG report (oig.dot.gov/library-item/46745) |
| **Mar 15, 2023** | **FAA Aviation Safety Summit** convened after a string of near-miss/runway-incursion incidents. | aerotime.aero; faa.gov newsroom readout |
| Aug 21, 2023 | NYT: "Airline Close Calls Happen Far More Often Than Previously Known." | nytimes.com |
| 2022 → 2023 | **Serious runway incursions 16 → 23** in the U.S. | Honeywell (citing FAA) |
| FY2023 | ~1,758–1,777 total runway incursions (~5/day); up ~12% vs FY2021. | DOT OIG (3.12.25 report); FAA |
| 2024 | 1,474 total incursions, **down ~17% from 2023**. | FAA / Forbes |

## Lead-time claim (the headline of the deck)

Our ASRS surface-conflict **share** began rising in **2021–2022** and the narrative label fired in **June 2021** — *before* the public inflection: the FAA Summit (Mar 2023) and the NYT exposé (Aug 2023). So the ASRS-derived signal **led the widely-recognized crisis by roughly 12–18 months.** External counts then confirm the rise (serious incursions 16→23 into 2023) and the partial 2024 easing mirrors our share dipping after the 2024 peak. [OP48 | 2026-06-19T02:58+03:00 | P0010]

## Bias rule-outs (stress test)

1. **Reporting-volume bias:** the metric is *share of monthly reports*, not raw count — the rise is not explained by ASRS simply receiving more reports overall.
2. **Reverse causality (post-summit awareness → more reporting):** a real risk for 2023+ data, but our signal **predates** the March 2023 summit (rise visible 2021–22, narrative fire June 2021). Awareness-driven over-reporting would post-date the summit, so it *cannot* explain the leading edge — this strengthens, not weakens, the early-warning claim.
3. **Taxonomy artifact:** `Conflict Ground Conflict` exists from 2011 (`taxonomy_suspect = False`); not a new/renamed code.
4. **Seasonality:** fires require positive YoY share change (§5.1), so a recurring seasonal bump alone would not trigger.
5. **Units mismatch caveat:** external sources count incursions on a **fiscal-year, raw-count** basis; our metric is **calendar-month share**. Directionally consistent, not a like-for-like comparison — stated explicitly in the deck.

## Robustness — does the rise survive traffic normalization? (the "isn't it just post-COVID rebound?" objection)

The single biggest challenge to the signal is: *more flying ⇒ more reports ⇒ more conflicts, mechanically.* External FAA/DOT-OIG figures rule this out on two counts. [OP48 | 2026-06-19T03:30+03:00 | P0011]

**1. Counts returned to pre-pandemic levels while traffic was still below pre-pandemic peak → the *rate* rose.**

| FY | Total runway incursions | Airport operations | Approx. rate /M ops |
|----|------------------------|--------------------|---------------------|
| 2019 (pre-COVID) | 1,760 | ~43.0 M (peak) | ~40.9 |
| 2021 | 1,573 | (recovering) | — |
| 2022 | — | 36.1 M | — |
| 2023 | 1,777 (~5/day) | 37.3 M | **~47.6** |
| 2024 | 1,758 | (still < 43 M peak) | higher than 2019 |

FY2023 had **fewer operations than FY2019 (37.3 M vs ~43 M) yet *more* incursions** → incursions-per-operation ran **~15% above** the pre-pandemic baseline. The rise is **not** explained by traffic volume. (Rates are approximate, FY-grain; sources: FAA *Air Traffic by the Numbers*, DOT OIG 3/12/25.)

**2. Severity — not just frequency — spiked, and traffic cannot explain that.** Category A&B ("serious", collision narrowly avoided) incursions hit **22 in FY2023 — the highest in FY2019–2024** — then fell to **9 in FY2024** (−59%). The *dangerous tail* worsened while operations were still below peak, then eased. This mirrors our share peaking ~2024 and dipping in 2025. [OP48 | 2026-06-19T03:30+03:00 | P0011]

**3. Anchor incidents (deck colour).** JFK (Jan 13 2023, AA777 crossed an active runway into a departing Delta 737, ~1,400 ft, Cat B) and Austin (Feb 4 2023, SWA737/FedEx767 within ~150–170 ft in freezing fog, Cat A) are the events that triggered the March 2023 summit.

**4. Framing bonus.** The FAA's own February 2023 response *"directed a review of the ASIAS database for indicators of emerging trends."* The FAA reached for data-mining of safety reports **reactively, after the crisis**; our method demonstrates the same idea applied **proactively** would have flagged it ~12–18 months earlier. [OP48 | 2026-06-19T03:30+03:00 | P0011]

## Robustness — is the share rise just a denominator / compositional artifact?

A share `s_c = count_c / total_c` can rise for a non-signal reason: the **denominator shrank** or **other categories collapsed**, inflating `c`'s slice while `c` itself is flat. Checked directly against the count series (`category_share_series.parquet`); the rise is in the **numerator**, not the denominator. [OP48 | 2026-06-20T14:21+03:00 | P0020]

| Year | Ground-conflict count (numerator) | Total reports (denominator) | Share |
|----|----|----|----|
| 2011 | 230 | 5,646 | 4.1% |
| 2013 | 135 | 4,478 | 3.0% |
| 2021 | 305 | 4,571 | 6.7% |
| 2023 | 411 | 4,589 | 9.0% |
| 2024 | 606 | 5,427 | 11.2% |
| 2025 | 642 | 6,109 | 10.5% |

- **Numerator ≈ tripled** (≈135–230 → 606–642/yr) while the **denominator stayed in a flat ~4,500–6,100/yr band with no secular trend** → the share rise reflects a real rise in ground-conflict reports, not a shrinking base.
- **Not a closed composition:** `Anomaly` is multi-label (a report carries several tags), so category shares do **not** sum to 100% — one category rising does not mechanically force another down. The naive pie-slice artifact does not apply.
- **External absolute counts** (FAA incursions, raw and per-movement) rose independently — a purely ASRS-internal composition artifact could not produce that agreement.

Chart: `production/output/deck/P07_rawcount_ground_conflict.png` (numerator vs denominator overlay; built by `production/build/P07_make_rawcount_chart.py`). Added to the deck as an appendix / Q&A-backup slide. [OP48 | 2026-06-20T14:21+03:00 | P0020]

## Verdict

The surface/ground-conflict signal is **corroborated and defensible**: two independent ASRS methods agree, the rise predates the public crisis (genuine lead time), external authorities confirm the trend and its reversal, and the main bias mechanisms are ruled out or work in our favor. This is the deck's headline early-warning story. [OP48 | 2026-06-19T02:58+03:00 | P0010]

## Sources

- DOT OIG, "FAA Has Taken Steps To Prevent and Mitigate Runway Incursions…" — oig.dot.gov/library-item/46745 and the 3.12.25 final report PDF.
- FAA, "Readout from the FAA Aviation Safety Summit Breakout Panels" — faa.gov/newsroom.
- aerotime.aero, "FAA leads safety summit after a string of near-miss incidents" (summit Mar 15, 2023).
- NYT, "Airline Close Calls Happen Far More Often Than Previously Known" (Aug 21, 2023).
- Honeywell Aerospace (serious incursions 16→23, 2022→2023).
- FAA Runway Safety Statistics — faa.gov/airports/runway_safety/statistics; FAA "Air Traffic by the Numbers" (May 2024).
