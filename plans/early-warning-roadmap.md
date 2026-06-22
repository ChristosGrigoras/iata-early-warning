---
authors: [OP48]
primary: OP48
---

# Early-warning roadmap — IATA case study

End-to-end sequence from framing to submission. Critical path is 0→1→2→3→4 (sequential); Phase 6 is optional; Phase 7 can start once Phase 4 has results.

## Phase 0 — Framing & scope → `production/brief/`
Define what "early-warning system" means here, the user/decision-maker, success criteria, and the 1–2 signal types we'll build.
- [x] Write the brief (objective, audience, signal definition, success criteria, non-goals). → `production/brief/P00_early-warning-brief.md`
- [x] **Decision:** both — volume/rate anomalies (structured) + emerging narrative themes (free text).
- [x] Confirm data-pull scope: broad multi-year (2011–2025).

## Phase 1 — Data acquisition → DONE
- [x] Data-access method: DBOL wizard + in-session `fetch` of CSV export; Firecrawl reserved for Phase 5. → `research/notes/P01_asrs-data-source.md`
- [x] Query/range/fields: all categories, 2011–2025, yearly chunks (1-month overlap).
- [x] Exports run (15 CSVs, ~224 MB) → `data/raw/`.
- [x] Loader (`production/build/P01_build_dataset.py`) → `data/processed/asrs.parquet`: **80,047 unique reports, 127 cols**.

## Phase 2 — EDA → `production/build/P02_01-eda.ipynb`
- [x] Volumes over time; by category / aircraft / flight phase.
- [x] Coverage gaps + explicit reporting-bias check.
- [x] Conclude viable signals: structured-category **share** anomalies + NLP narrative-theme emergence. Multi-label caveat recorded (`research/notes/P02_eda-qa-summary.md`).

## Phase 3 — Methodology spec → `production/spec/P03_methodology.md` (LOCKED)
- [x] Lock approach: share-based robust-z anomaly (structured, Signal A) + GLiNER2 zero-shot risk labels with unsupervised discovery guard (narrative, Signal B); cross-validate.
- [x] Define "signal" metrics: share, 24-mo MAD baseline, z≥2/3, ≥3-month persistence, min 20/mo volume.
- [x] Bias guards: taxonomy-change gate, YoY seasonality check, ranked-candidates framing.
- [x] Framing: retrospective lead-time headline + caveated current watchlist.
- [x] Data dictionary documented (§2). User signed off on framing, guards, Signal B approach.

## Phase 4 — Build the signals → `production/build/02-…`, `03-…`
- [x] Signal A built + executed (`P04_02-structured-signals.ipynb`); artifacts in `production/output/signals/`.
- [x] Headline locked: surface/ground-conflict (`Conflict Ground Conflict` + `Taxi`), workload secondary (`research/notes/P04_signal-interpretation.md`).
- [x] Signal B notebook built + executed (`P04_03-narrative-signals.ipynb`): OpenRouter DeepSeek V4 Flash full-data classification (79,572 narratives) + unsupervised discovery pass. Produced 5 persisted narrative fires, including `runway incursion / ground conflict / surface movement` (`first_fire_ym=202106`).

## Phase 5 — Validate & interpret → notebooks + `research/notes/`
- [x] Stress-test signals (real vs. reporting-driven): share-metric, taxonomy, seasonality, reverse-causality rule-outs → `research/notes/P05_signal-corroboration.md`.
- [x] Corroborate against external public sources: FAA Safety Summit (Mar 15 2023), DOT OIG, NYT (Aug 2023), serious incursions 16→23 (2022→23). Signal leads crisis ~12–18 mo.
- [x] Write down caveats (units mismatch, reverse-causality, reporting bias).

## Phase 6 — Prototype (optional) → `production/build/` (Streamlit/Taipy)
- [ ] Interactive "signal dashboard" demo.
- **Decision:** build prototype or not (only if Phases 4–5 land cleanly).

## Phase 7 — Narrative & deck → `writing/` + `production/output/`
- [ ] 5–6 slides: framing → approach → signals → decision-support value.
- [ ] Polished README + speaker notes; fold in responsible-AI/provenance angle.

## Phase 8 — Publish & submit → GitHub repo + link
- [ ] Scrub secrets/large data; finalize README.
- [ ] Create repo (local → GitHub); produce submission link for the day before the interview.

## Risks
- Phase 1 data-access friction — front-load.
- Phase 5 over-claiming a signal that is just reporting bias.
