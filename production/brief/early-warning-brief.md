---
authors: [OP48]
primary: OP48
---

# Phase 0 brief — Aviation safety early-warning signals

The framing the analysis and deck hang on. Stable intent; update via `plans/_active.md` if it changes.

## Objective — how we interpret "early-warning system"

A system that detects **leading indicators** of aviation safety risk — shifts in the pattern of voluntarily reported incidents and near-misses — **early enough for stakeholders to investigate and intervene before the risk surfaces as an accident.**

Why ASRS fits: it captures **near-misses and latent hazards** (leading signals) rather than accidents (lagging outcomes). The goal is not prediction of specific accidents but **earlier attention allocation**: moving a human's eyes onto an emerging issue sooner than the status quo would.

## Audience / decision-maker

A **safety-intelligence analyst** (the kind of function IATA runs across 350+ airlines) who triages signals and escalates credible ones to airlines or regulators. The system's output is a **prioritised triage queue**, not an automated decision. This framing matters: it sets the bar at "useful prompt to investigate," not "proven causal claim."

## What counts as a "signal" (definition, to avoid hand-waving)

A detected deviation that is:
1. **Distinguishable from baseline noise** — statistically separable from normal fluctuation.
2. **Persistent or accelerating** — sustained or growing over a defined window, not a one-off blip.
3. **Interpretable** — we can point to the specific narratives / category / theme driving it.

A signal is a **reason to look**, never a conclusion.

## The two signal types we will build

1. **Volume / rate anomalies** *(structured fields)* — statistically significant rises in report counts within a category (event type, flight phase, aircraft, contributing factor) vs. an expected baseline. Answers: *"Is something happening more than usual?"*
2. **Emerging narrative themes** *(free text)* — new or rapidly growing clusters/topics in the narratives that the existing taxonomy doesn't cleanly capture. Answers: *"Is something new happening that we don't yet have a label for?"* This is the **harder, higher-value differentiator.**

Combined view: a rising cluster that also shows a volume anomaly is the strongest early signal.

## Success criteria (for this case study)

We cannot measure real-world accidents prevented, so success = demonstrating credibility and judgment:
- The method surfaces **at least one interpretable emerging theme or anomaly**, ideally one that — in retrospect — rose *before* it became widely recognised.
- We are **honest about reporting bias and false positives**, and show how the design mitigates them.
- We **communicate clearly** how the signal plugs into a decision-making workflow.

## Non-goals

- Not predicting specific accidents or establishing causation.
- Not a production / real-time streaming system.
- Not a complete safety taxonomy — we surface candidates for human review.

## Central risk and how the framing handles it

**Reporting bias:** ASRS counts reflect *reporting behaviour*, not true event rates. A spike can be driven by awareness campaigns or policy changes, not by a real safety shift.

Mitigations baked into the framing:
- Treat signals as **relative shifts**, normalise to total report volume where possible.
- Require **interpretability** (criterion 3) so analysts judge plausibility.
- **Corroborate** strong signals against external public sources (NTSB / FAA / news / weather) in Phase 5 — this is where Firecrawl is used.
- State the caveat explicitly in the deck; position output as triage, not truth.

## Scope decision (Phase 1) — confirmed

**Broad pull: all report categories across a ~10–15 year window** (target Jan 2011 – Dec 2025). [CG]
Rationale: emergence detection needs both breadth (to catch *new* themes anywhere) and a long enough baseline for anomaly detection. Executed as **date-chunked DBOL CSV exports** (each chunk ≤10k records). See `research/notes/asrs-data-source.md` for the export recipe.
