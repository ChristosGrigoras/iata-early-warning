---
authors: [OP48]
primary: OP48
---

# Backlog

Ideas not started. One line each; promote to `_active.md` or a `plans/[name].md` when picked up.

- Evaluate **GLiNER2** zero-shot schema-extraction / classification on narratives to quantify & trend specific candidate risks (complement to unsupervised topic discovery). [OP48]
- Pull and cache ASRS export (define query, date range, fields); document steps in `research/notes/`.
- EDA notebook: report volumes over time, by category/aircraft/phase-of-flight, anomalies, and reporting-bias checks.
- NLP pipeline: embed narratives → cluster/topic-model → track cluster growth over time as "emerging theme" signal.
- Time-series anomaly detection on category counts (e.g. STL/decomposition, rolling z-score, changepoint detection).
- Cross-reference an external public source (e.g. NTSB, FAA, weather) to corroborate a detected signal.
- Streamlit/Taipy prototype: interactive "signal dashboard" (trend + emerging clusters + drilldown to narratives).
- **[ENRICHMENT — high ROI]** Fetch **FAA normalized runway-incursion rate** (incursions per million operations, from "Air Traffic by the Numbers" + Runway Safety Statistics) and overlay on our Signal-A share series — confirms the 2021–24 rise survives traffic-normalization (kills the "just post-COVID rebound" objection). Cheap (~1h, cite FAA's own rate; no join pipeline). Join key: month/FY national. [OP48]
- **[ENRICHMENT — deprioritized]** FAA traffic volume (OPSNET/ASPM) for a self-computed rate; BTS On-Time taxi-out full series 2011–25 (congestion proxy); ATC controller staffing timeline (DOT OIG / FAA Workforce Plan) for the secondary "staffing strain" signal. Name as future work in deck; don't build before shipping. [OP48]
- Build the 5–6 slide deck from validated findings; write speaker notes in `writing/`.
- Create GitHub repo, scrub secrets/large data, write README, produce submission link.
