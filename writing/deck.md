---
marp: true
paginate: true
size: 16:9
math: katex
title: Early warning from near-misses — IATA case study
author: OP48 / CDX53 / CMP25 (provenance-tracked)
style: |
  :root {
    --navy: #0E4F9E;
    --steel: #5B9BD5;
    --slate: #2E3440;
    --gray: #6B7280;
    --amber: #D97706;
    --amber-fill: #FCEBCF;
    --line: #E5E7EB;
  }
  section {
    font-family: "Helvetica Neue", "Segoe UI", Arial, sans-serif;
    color: var(--slate);
    background: #ffffff;
    padding: 48px 60px;
    font-size: 22px;
  }
  h1 { color: var(--navy); font-size: 40px; margin-bottom: 8px; }
  h2 { color: var(--navy); font-size: 30px; border-bottom: 3px solid var(--line); padding-bottom: 6px; }
  strong { color: var(--navy); }
  em.amber, .amber { color: var(--amber); font-style: normal; font-weight: 700; }
  a { color: var(--steel); }
  section.lead { justify-content: center; text-align: left; }
  section.lead h1 { font-size: 50px; }
  .sub { color: var(--gray); font-size: 24px; }
  .tag { color: var(--gray); font-size: 16px; }
  table { font-size: 19px; }
  th { background: var(--navy); color: #fff; }
  tr:nth-child(even) { background: #F3F6FB; }
  footer { color: var(--gray); font-size: 13px; }
  ul { line-height: 1.5; }
  .small { font-size: 18px; }
  .center { text-align: center; }
  img[alt~="hero"] { box-shadow: 0 2px 14px rgba(14,79,158,0.18); border-radius: 6px; }
footer: "IATA Senior Data Scientist · case study · data: NASA ASRS 2011–2025"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Early warning from near-misses
## Surfacing emerging safety risk early — from public data

<span class="sub">One worked example, and an operating model to sustain it.</span>

<br>

<span class="tag">NASA Aviation Safety Reporting System (ASRS) · 80,047 reports · 2011–2025</span>

---

## The idea — and how the signal is read

- **Accidents are rare and *lagging*. Precursors — near-misses — are common, and they come *first*.** ASRS is a national, public repository of these voluntary reports — filed by pilots, controllers, and mechanics, and rich in free-text narrative.

> An *early-warning system* is simply this: **detect precursors trending upward before the accident — from data already held.**

**One detection engine (shared):** each label becomes a monthly *share* (not raw counts, so COVID/awareness swings don't drive it); a series fires on **robust z ≥ 2** vs its 24-mo baseline, **persisting 3+ months**, with taxonomy-change & seasonality guards.

**The two views differ only in how a report is labeled:**

<div class="columns" style="display:grid; grid-template-columns: 1fr 1fr; gap: 36px;">
<div>

**1 · Structured tags**
- From **ASRS taxonomy codes** — precise, but only risks that already carry a code.

</div>
<div>

**2 · Narrative view (LLM)**
- A **zero-shot model** reads the free text — catches the emerging & unlabeled (e.g. **GPS jamming**).

</div>
</div>

<span class="small amber">Output = a ranked shortlist for human review, not an alarm. Leading indicators, not lagging ones. · 79,572 narratives · 2011–2025 · US</span>

---

## Finding: runway & taxiway near-misses rose early

![hero w:600](assets/hero_surface_conflict.png)

<span style="font-size:18px; line-height:1.4;">The structured "ground-conflict" tag roughly <span class="amber">doubled — ~5% of reports to ~11% by 2024</span> (the raw count tripled too — not a denominator artifact). Independently, the narrative view (♦) began flagging runway-incursion reports in <span class="amber">June 2021</span> — both ahead of the 2023 crisis.</span>

<span class="small amber">The telling part: the *structured* share spiked above threshold again and again (its *z* hit ~6) — but too erratically to ever hold the **3-month persistence rule**, so it never registered a fire. The *narrative* signal rose smoothly enough to persist — and fired **June 2021**. Same risk, two different failure modes — which is why both are run.</span>

---

## It led the crisis — by 12–18 months

**The signal rose in 2021–22. Public recognition came in 2023:**
- <span class="amber">FAA emergency safety summit — March 2023</span>, after the JFK and Austin near-collisions.
- <span class="amber">NYT: airline close calls far more frequent than known — August 2023.</span>

**→ Lead time: ~12–18 months.**

<span class="small amber">The decisive check: the rise *predates* the summit — so awareness-driven over-reporting cannot explain the leading edge.</span>

<span class="small">Notable: the FAA's own response was to *mine its safety database (ASIAS) for emerging trends* — **reactively, after** the events. Here the same idea is applied **beforehand**.</span>

---

## Not just more traffic — the *rate* rose too

<div class="columns" style="display:grid; grid-template-columns: 1fr 0.9fr; gap: 32px; align-items:center;">
<div>

**The obvious objection: more flying ⇒ more conflicts. The data rules it out:**
- Incursions **per movement** ran <span class="amber">~15% above pre-pandemic</span> — rising while traffic was still **below** the 2019 peak.
- **Severity** spiked, not just frequency — and more traffic raises *frequency*, not *severity*.

</div>
<div>

| Serious incursions (Cat A&B) | |
|----|----|
| **2023** | **22 — a 6-year high** |
| 2024 | 9 (−59%) |

</div>
</div>

<span class="small">Sources: FAA *Air Traffic by the Numbers*; DOT OIG (Mar 2025). External counts are fiscal-year, raw; the figures here are calendar-month share — directional, not like-for-like.</span>

---

## What this is — and what it isn't

<div class="columns" style="display:grid; grid-template-columns: 1fr 1fr; gap: 36px;">
<div>

**What it is**
- A *leading indicator* that risk is rising.
- Low-cost, public, explainable, reproducible.
- Corroborated two ways: the narrative detector that *fired*, the structured trend that *agrees*, and external sources.

</div>
<div>

**What it isn't**
- Not accident prediction — these are precursors, not accidents.
- Not causal. Leading hypothesis: post-COVID understaffing + the traffic rebound — but only the **symptom is observed, not the cause**.
- Voluntary data. The bias is *mitigated* (share, not counts) — not eliminated.
- Monthly, US-only, de-identified (no airport). These figures and the FAA's agree in **direction, not magnitude**.

</div>
</div>

<span class="small amber">Throughout: a signal is a reason for an analyst to *look* — never an automated verdict.</span>

---

## From one signal to a monthly watchlist

- This case is the **proof of concept** — the same pipeline already produces a **ranked monthly watchlist** from both detectors.
- **Value to a safety team:** a short, explainable list of *what is emerging and where to look first — months earlier.*

![w:870](assets/watchlist_table.png)

<span class="small">**Next:** join FAA traffic & controller-staffing data (to test causation) and NTSB outcomes (do these precursors lead to accidents?).</span>

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Thank you

<span class="sub">Precursors come first — and they already sit in free, public data.<br>A simple, transparent method would have put runway conflict on an analyst's shortlist <span class="amber">~12–18 months early.</span></span>

<br>

<span class="tag">Full methodology & appendix available · ASRS 2011–2025 · narrative + structured views</span>

---

## Appendix — the share rise isn't a denominator artifact

![w:680](assets/rawcount_ground_conflict.png)

<span style="font-size:18px; line-height:1.4;">A rising *share* could be an artifact if the denominator shrank or other categories collapsed. It isn't: the <span class="amber">raw ground-conflict count roughly tripled</span> (≈230 → 640 reports/yr) while <span class="amber">total monthly reporting stayed flat</span> — the numerator rose on its own. ASRS anomaly tags are *multi-label*, so category shares don't sum to 100% (one rising doesn't force another down), and the FAA's *absolute* incursion counts rose independently. Share, raw count, and external data all point the same way.</span>

---

## Appendix — two independent detectors, same trend

![w:740](assets/crossview_overlay.png)

<span style="font-size:18px; line-height:1.4;">The headline's cross-view check, on one axis. The <span class="amber">structured</span> taxonomy tag and the <span class="amber">narrative</span> LLM — entirely separate pipelines — both rise into 2021–24. What agrees is the *direction and timing*, not the level: the narrative label sits at a higher base rate because it's broader. The narrative view fires **June 2021**; the structured trend confirms. <span class="amber">(The 2022 share dip is a reporting-volume rebound — the underlying counts kept rising.)</span></span>

---

## Appendix — was the language model validated? Yes

<div class="columns" style="display:grid; grid-template-columns: 1fr 1fr; gap: 34px;">
<div>

**Reviewer spot-check — 30 flagged narratives** (runway label):
- <span class="amber">70%</span> genuinely about surface / ground movement (broad match).
- <span class="amber">37%</span> a true runway-incursion / ground-conflict near-miss (strict).
- Precision rises with confidence: **88%** (7/8) at ≥0.95 · 70% (7/10) at 0.90 · 58% (7/12) at ≤0.85 — small bands, directional.
- **Main failure mode:** 8 of 9 false positives are *airborne* NMACs the model tags as "conflict."

</div>
<div>

**What it means — and the honest scope:**
- The narrative *absolute level* is inflated, so **trend is used, not level**, cross-checked against the cleaner structured tag.
- A confidence threshold (≥0.95) or an airborne-vs-surface guard would sharpen it.
- Precision only (flagged positives); recall not measured — this is a spot-check, not a gold-standard eval.

<span class="small amber">Exactly why the output is a candidate for review, not a count.</span>

</div>
</div>
