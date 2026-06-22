---
authors: [OP48]
primary: OP48
prov_id: P0021
prov_ts: 2026-06-20T14:43+03:00
---

# Narrative classifier — precision spot-check (Signal B validation)

Closes the validation gap flagged in `OBSERVATIONS.md` §4: the narrative LLM (OpenRouter DeepSeek) is the novel half of the method and carries the headline's formal June-2021 fire, yet had no precision evidence. This is a reviewer-adjudicated spot-check of the headline label `runway incursion / ground conflict / surface movement`. Reproducible via `production/build/P04_validate_narrative_labels.py`. [OP48 | 2026-06-20T14:43+03:00 | P0021]

## Method & scope (state the limits up front)

- **Positives only → precision, not recall.** Sampled 30 narratives the classifier *flagged* with the runway label; read each `Synopsis` and adjudicated. We do not measure missed positives (recall) — that would need labelling un-flagged narratives.
- **Seeded, confidence-stratified sample** (18 at confidence ≥0.9, 12 below; seed=42) so it reproduces.
- **Reviewer = OP48**, not a domain expert and not the model under test — an independent check, but not a gold standard. Verdicts per ACN are hard-coded in the script for reproducibility.
- Verdict codes: **strict** = genuine runway incursion / ground- or surface-movement conflict; **broad** = genuinely about surface/taxi/ground ops but not a near-miss; **fp** = no surface/ground element.

## Result

| Metric | Value |
|--------|-------|
| Precision — broad (surface/ground relevant) | **70%** (21/30) |
| Precision — strict (true incursion/conflict near-miss) | **37%** (11/30) |
| False positives | 30% (9/30) |

**Precision rises with model confidence (small bands — n = 8 / 10 / 12):** 88% (7/8) at ≥0.95 · 70% (7/10) at 0.90 · 58% (7/12) at ≤0.85 → confidence is informative (treat the gradient as directional, given the tiny per-band counts); raising `cls_threshold` to ~0.95 would roughly halve the false-positive rate.

**Dominant failure mode:** **8 of 9 false positives are *airborne* NMAC / traffic-pattern conflicts** that the model tags as "conflict" — i.e. the word "conflict" in the label bleeds airborne events into a surface label. A simple airborne-vs-surface guard (or dropping "conflict" from the label wording) would sharpen it materially.

## Implications (and why the headline still holds)

1. **Use trend, not level.** The label is broad (it flags ~15.7% of all narratives, base rate ~13% even in 2011), so the *absolute* share overstates true runway-incursion prevalence. The early-warning claim rests on the **rise** (13%→21%, and the June-2021 fire), and on **cross-view agreement with the cleaner structured `Conflict Ground Conflict` tag** (4%→11%) — not on the narrative level.
2. **The FP mode is roughly time-stable**, so it inflates the level but does not obviously manufacture the trend; the structured tag (which does not share this FP mode) rises in parallel, which is the real safeguard.
3. **Honest framing preserved:** output is a *candidate for human review, not a count* — a 70% broad / 37% strict precision is acceptable for a triage shortlist, not for an automated metric.

## Artifacts

- `production/build/P04_validate_narrative_labels.py` — reproducible sampler + adjudication + precision.
- `production/output/narrative_signals/validation/narrative_validation_sample.csv` — the 30 adjudicated rows (ACN, ym, confidence, verdict, synopsis).
- `production/output/narrative_signals/validation/narrative_validation_by_confidence.csv` — precision by confidence band.
- Deck appendix slide ("did we validate the language model?") summarizes this. [OP48 | 2026-06-20T14:43+03:00 | P0021]
