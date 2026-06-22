---
authors: [OP48]
primary: OP48
prov_id: P0008
prov_ts: 2026-06-19T01:55+03:00
---

# Signal B — scale-up cost & decision (cost-aware appendix)

> **UPDATE — decision superseded (2026-06-19, later same day, P0009).** The "stay on the free 239-narrative pilot" call below was **reversed once full coverage proved necessary** for the persistence/lead-time claims to be defensible (pilot N was too small for persisted fires). The zero-shot labeller was run via **OpenRouter → DeepSeek V4 Flash** (`deepseek/deepseek-v4-flash`), concurrent batched calls, over **all 79,572 narratives** — a hosted path that lands at the cheap end of the table below (well under the mini-LLM batch estimate). The original GLiNER2 pilot reasoning is kept verbatim as the record of *why* the pilot was capped and what the alternatives cost; the §5 detector logic is identical under either labeller. The local-CPU `~66 h` runtime — not cost — was the actual blocker.

**Original decision (CG, 2026-06-19, pre-pivot):** stay on the **free local GLiNER2 pilot** (239 narratives); do **not** spend now. This note documents the measured cost-to-scale so the deck can state, honestly and precisely, what full-coverage would take. [OP48 | 2026-06-19T01:55+03:00 | P0008]

## Why the pilot is capped

Local GLiNER2 (`fastino/gliner2-base-v1`, CPU, DeBERTa-v3-base encoder) measured at **~3.0 s/narrative** on this machine → **~66 hours** for the full 80,047. Fine for a method demo; impractical for full coverage without paid/accelerated inference. [OP48 | 2026-06-19T01:55+03:00 | P0008]

## Corpus size (measured)

`Report 1 | Narrative`, 80,047 rows: mean **269 words / ~1,521 chars / ~380 tokens**; median 214 words. **~30.4M narrative tokens**; with per-call label-list + instruction overhead, **~60M input / ~4M output** tokens for a full labeling pass. [OP48 | 2026-06-19T01:55+03:00 | P0008]

## Live pricing (pulled 2026-06-19 — verify before any spend)

- **Pioneer / GLiNER hosted (Fastino):** subscription, not per-token. **Hobby $5/mo incl. $30/mo inference allowance**; Pro $20/user/mo ($50/day, $1,500/mo cap, downloadable weights); Enterprise custom. Source: pioneer.ai/pricing.
- **OpenAI:** gpt-5.5 flagship **$5 in / $30 out** per 1M (cached input $0.50); GPT-4.1 Mini **$0.40/$1.60**, **batch $0.20/$0.80**. Source: developers.openai.com/api/docs/pricing.

## Cost to scale to full 80k (estimates)

| Path | Est. cost | Notes |
|------|-----------|-------|
| Local pilot (**chosen**) | **$0** | 239 rows; ~66 h for full run |
| **GLiNER Pioneer Hobby** | **~$5/mo** | $30 allowance likely covers full 80k; in-tool, fast |
| Mini LLM (batch) | ~$15 | full coverage |
| Mini LLM (non-batch) | ~$30 | full coverage |
| Flagship full pass | ~$210–420 | diminishing returns for this deliverable |
| Hybrid (mini bulk + flagship on ~15% ambiguous) | ~$45–78 | best precision per $ |

**Key point for the deck:** the strongest in-tool option (GLiNER Pioneer) is also the **cheapest paid path (~$5)** — full narrative coverage would cost less than a mini-LLM pass. Cost is *not* the blocker; we cap at pilot by choice for this exercise. [OP48 | 2026-06-19T01:55+03:00 | P0008]

## If we later flip to "scale"

1. Pioneer Hobby ($5) → run all 80k via `GLiNER2.from_api()` (needs `PIONEER_API_KEY`).
2. Re-run `03-narrative-signals.ipynb` with `MAX_NARRATIVES` raised to full; the §5 detector logic is unchanged.
3. Then the persistence/lead-time claims for the narrative signal become defensible at full coverage (pilot N is too small for persisted fires). [OP48 | 2026-06-19T01:55+03:00 | P0008]
