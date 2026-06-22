---
authors: [OP48]
primary: OP48
---

# Active

## What I want

Build the IATA case-study deliverable: an analysis/prototype that demonstrates whether public data (primarily NASA ASRS) can produce **early signals** of emerging aviation safety risks or operational issues, plus a 5–6 slide presentation explaining the framing, approach, signals, and decision-support value.

## What done looks like

- [ ] A runnable analysis (notebook/report) showing at least one credible early-signal method on ASRS data.
- [ ] A clear interpretation of "early-warning system" for aviation safety (framing).
- [ ] 5–6 slide deck: (a) framing, (b) approach, (c) key signals/insights, (d) decision-support value.
- [ ] Published as a GitHub repo link, ready to email the day before the interview.

## Constraints

- Local compute; GitHub repo created at the end for the link.
- Judged on framing + reasoning + communication, not production-readiness.
- Mind ASRS reporting bias (voluntary, self-reported) when claiming "signals".

## Status

Phase 0–3 done; spec LOCKED (`production/spec/P03_methodology.md`). **Phase 4 Signal A built + executed** → `production/build/P04_02-structured-signals.ipynb` (+ executed), artifacts in `production/output/signals/`. **Headline LOCKED** (`research/notes/P04_signal-interpretation.md`): surface safety / ground-conflict risk — `Anomaly→Conflict Ground Conflict` + `Flight Phase→Taxi` both ~double off pre-2020 baseline, accelerate 2023–24; leads the public 2023 runway-incursion crisis. Workload = secondary. **Phase 4 Signal B scaled and executed on full data via OpenRouter DeepSeek V4 Flash** → `production/build/P04_03-narrative-signals.ipynb` (+ executed), artifacts in `production/output/narrative_signals/`. Result: 79,572 narratives processed; **5 persisted narrative fires**, including `runway incursion / ground conflict / surface movement` (watch fire at 202106), strengthening cross-view support for the headline. **Phase 5 DONE** → `research/notes/P05_signal-corroboration.md`: external sources (FAA Safety Summit Mar 15 2023, DOT OIG, NYT Aug 2023, serious incursions 16→23 2022→23) confirm the surface-conflict trend; ASRS signal **leads the public crisis ~12–18 months** (share rose 2021–22, narrative fire June 2021). Bias rule-outs hold (share-metric, taxonomy stable, reverse-causality predates summit). **Phase 5 Step-1 robustness done (P0011): traffic-normalized rate rose ~15% vs FY2019, serious Cat A&B incursions 6-yr high FY2023 → "just rebound" objection killed. Deck outline done (P0012) → `writing/deck-outline.md` (6 slides, 10-min, speaker notes). Step 3 done (P0013): HERO chart. Step 4 done (P0014): 8-slide Marp deck `writing/P07_deck.md` → `writing/P07_deck.pdf` + `writing/P07_deck.html` (IATA palette, hero+GPS charts embedded, renders via google-chrome). Next: Step 6 — repo hygiene + README + push to GitHub, then Step 7 submit. (Step 5 prototype skipped.)**

**(superseded) Phase 7 — build the 5–6 slide deck (framing → approach → signal → lead-time corroboration → decision value); Phase 6 prototype optional.** Provenance uses `[CODE | TS | ID]` + `provenance-ledger.md` (at P0010).

## Notes

- Full sequence: see `plans/early-warning-roadmap.md` (Phases 0–8; critical path 0→1→2→3→4).
- Candidate methods to explore: time-series trend/anomaly detection on report volumes by category; NLP embeddings + clustering/topic modelling on narratives to spot emerging themes; combining the two (rising clusters = early signal).
