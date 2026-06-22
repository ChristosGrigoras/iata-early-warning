---
authors: [OP48]
primary: OP48
prov_id: P0005
prov_ts: 2026-06-19T00:30+03:00
---

# Signal interpretation — headline selection (Phase 4 → 5)

Interprets the Signal A candidate table (`production/output/signals/signal_candidates.csv`) through an **early-warning lens** (recent + sustained rise, not historical spikes) and locks the deck headline. Source series: `production/output/signals/category_share_series.parquet`. [OP48 | 2026-06-19T00:30+03:00 | P0005]

## Method of selection

Top-ranked-by-`peak_z` candidates were re-screened on: recent fires (last 24 claimable months), positive recent slope, and late-window vs early-window share. This demotes categories whose big move was years ago (`z_latest` now negative) and promotes genuinely emerging ones. [OP48 | 2026-06-19T00:30+03:00 | P0005]

## LOCKED headline — surface safety / ground-conflict risk

The surface-conflict story rises off its pre-2020 baseline and accelerates through 2023–24, but the **two structured fields rise on different timelines** — important for honest framing:

- `Anomaly → Conflict Ground Conflict` (share %): 2011–19 ≈ 4–5 → 2021 **6.7** → 2022 **7.0** → 2023 **9.0** → 2024 **11.2** → 2025 **10.5**. **← carries the early/pre-crisis claim** (climbs within 2021–22).
- `Aircraft 1 | Flight Phase → Taxi` (share %): 2011–19 ≈ 8–11 → 2023 **12.8** → 2024 **15.2** → 2025 **13.9**. **← rise is 2023–24 (concurrent/lagging), confirms magnitude, NOT the lead.**

**Why it's the headline:** [OP48 | 2026-06-19T00:30+03:00 | P0005]
- Sustained and recent (not a one-off spike).
- **Cross-view validation = structured trend + narrative classifier** (not the two structured fields): the narrative `runway incursion / ground conflict` label independently fires **June 2021** (`narrative_signal_candidates.csv`), agreeing with the Ground-Conflict trend on the *early* timing.
- **External corroboration:** maps onto the documented 2023 runway-incursion surge (FAA Safety Summit, March 2023) — verified in `P05_signal-corroboration.md`.
- **Lead time:** ground-conflict share + narrative fire were already climbing in 2021–22, *before* the high-profile 2023 near-collisions and regulatory response → a falsifiable early-warning claim.

### Detector nuance (state this in Q&A) [OP48 | 2026-06-19T03:58+03:00 | P0016]
The strict Signal-A robust-z detector returns **`fire_level = none`** for *both* `Conflict Ground Conflict` and `Taxi` (`signal_candidates.csv`) — but **not because z stays low**. The monthly share is **volatile**: ground-conflict's robust z spikes above threshold repeatedly (12 watch-months, peak ≈6, incl. z≈5 in April 2021) yet **never for the required 3 consecutive months** (longest watch run = 2), so no persisted fire registers. So the headline's *formal* early-warning fire is the **narrative label (June 2021)**, whose rise was smooth enough to hold the 3-month rule; the structured Ground-Conflict line is **trend evidence**, not a z-score fire. This is a genuine, complementary failure-mode story (the persistence rule suppresses a noisy-but-rising structured signal; the smoother narrative label caught it), not a weakness to hide.

**Deck spine:** *"ASRS ground-conflict reports began rising in 2021–22 (and the narrative classifier fired June 2021) — the approach would have flagged it ahead of the public runway-incursion crisis; taxi-phase share then confirms the surge into 2023–24."* [OP48 | 2026-06-19T03:58+03:00 | P0016]

## Secondary (supporting slide) — workload / staffing strain

`Person 1 | Human Factors → Workload` (share %): 2011–19 ≈ 10–16 → 2021 **17.6** → 2022 **26.5** → 2023 **24.6** → 2024 **23.4** → 2025 **15.7**. Sharp post-COVID surge (ATC/crew staffing), but **reverting in 2025** → frame as "a past episode the method also catches," not a current emergent. [OP48 | 2026-06-19T00:30+03:00 | P0005]

## Dropped (and why)

- `Troubleshooting`, `Smoke/Fire/Fumes/Odor`, `Situational Awareness` — high `peak_z` but historical; `z_latest` now negative.
- `Initial Approach`, `Airspace Structure`, `Airport` — flat or noisy, no clean emerging trend. [OP48 | 2026-06-19T00:30+03:00 | P0005]

## Implications for Signal B (notebook `03`)

Add **"runway incursion / ground conflict / surface-movement"** as a named GLiNER2 risk label. If its narrative share rises in step with the structured signal, that delivers the structured+narrative cross-view the methodology calls the headline (§7). [OP48 | 2026-06-19T00:30+03:00 | P0005]
