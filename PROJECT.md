---
authors: [OP48]
primary: OP48
---

# IATA Case Study — project map

Structured Cursor workspace for the IATA Senior Data Scientist case study: explore whether public data (primarily NASA ASRS incident reports) can surface **early signals** of emerging aviation safety risks or operational issues.

## The brief (fixed inputs)

- **`case-study.md`** — the assignment: framing questions, deliverables (analysis/prototype + 5–6 slides), submission rules (repo link, day before interview).
- **`job.md`** — the role context (what IATA values: framing, reasoning, communication; NLP/GenAI, time series, forecasting, clustering).

## Directories

| Path | Role |
|------|------|
| `plans/` | Current and future intentions (`_active.md`, `_backlog.md`, one file per idea). |
| `research/` | ASRS data dictionary, sources, EDA findings, signal/safety literature (`notes/`). |
| `production/` | Delivery: `brief/`, `spec/` (methodology), `build/` (notebooks, modules, prototype), `output/` (figures, deck). |
| `writing/` | Narrative: `drafts/` → `published/` (report, speaker notes). |
| `data/` | **gitignored.** `raw/` (yearly ASRS CSV exports), `processed/asrs.parquet` (combined, 80k reports). Rebuild via `production/build/build_dataset.py`. |
| `.cursor/rules/` | Layered agent rules (`00-` … `99-`). |

## Key files

- **`MEMORY.md`** — curated facts: stack, verify commands, constraints, data caveats.
- **`PROJECT.md`** — this file; human-readable orientation.

## Stack (starting point — flex as needed)

- **Python + Jupyter** for EDA and modelling.
- **Polars** preferred for data wrangling (fall back to pandas where ecosystem requires it).
- **NLP** on free-text ASRS narratives: embeddings + clustering/topic modelling for emerging-theme detection; time-series trend/anomaly detection on report volumes by category.
- **Prototype UI:** Streamlit or Taipy for an interactive "signal dashboard" demo.

## Skills (available globally)

- **Superpowers** — `~/.cursor/skills/superpowers/skills/` (brainstorming → plan → TDD → verify → review).
- **frontend-design** — for the prototype UI direction.

## Rules index

| File | When |
|------|------|
| `00-workspace.mdc` | Always — map, naming, routing, session loop, git hygiene. |
| `01-plans.mdc` | Always — align work with `plans/_active.md`. |
| `02-writing.mdc` | Files under `writing/**`. |
| `03-production.mdc` | Files under `production/**`. |
| `04-research.mdc` | Files under `research/**`. |
| `05-provenance.mdc` | Always — inline AI authorship tags `[CODE \| TIMESTAMP \| ID]`; ids tracked in `provenance-ledger.md`. |
| `06-model-routing.mdc` | Always — recommend a model to switch to after each suggestion. |
| `99-claude-mem.mdc` | Always — optional claude-mem + `MEMORY.md`. |
