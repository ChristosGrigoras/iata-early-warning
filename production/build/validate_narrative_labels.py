# provenance: primary=OP48 authors=[OP48] id=P0021 ts=2026-06-20T14:43+03:00
"""Manual precision check of the narrative classifier's headline label,
`runway incursion / ground conflict / surface movement`.

No gold-standard labels exist, so this is a reviewer-adjudicated spot-check on a
seeded, confidence-stratified sample of FLAGGED narratives (positives only ->
estimates precision, not recall). Each sampled synopsis was read and assigned:

  strict = genuine runway incursion / ground or surface-movement conflict
           (the risk the label is meant to catch)
  broad  = genuinely about surface/taxi/ground movement or ops, but not a
           near-miss conflict (matches the label's broad wording)
  fp     = false positive: no surface/ground element (almost always an
           AIRBORNE NMAC / pattern conflict the model mislabels as "conflict")

Run: python production/build/validate_narrative_labels.py
"""

from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parent.parent.parent
ASSIGN = ROOT / "production/output/narrative_signals/gliner_label_assignments.parquet"
ASRS = ROOT / "data/processed/asrs.parquet"
OUT_DIR = ROOT / "production/output/narrative_signals/validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RUNWAY = "runway incursion / ground conflict / surface movement"

# Reviewer adjudication (OP48), keyed by ACN. See module docstring for codes.
VERDICT = {
    "983975": "strict", "988065": "strict", "1088902": "strict",
    "1502537": "strict", "1784233": "strict", "1765686": "fp",
    "2023438": "strict", "2239396": "strict", "1232532": "fp",
    "1235613": "broad", "1382415": "broad", "1715430": "strict",
    "1740245": "fp", "1907945": "broad", "1935822": "strict",
    "2108530": "fp", "2141336": "strict", "2298765": "strict",
    "1706812": "fp", "1881927": "fp", "1078902": "fp",
    "1214106": "broad", "1385907": "broad", "1754909": "broad",
    "1768645": "broad", "2028162": "broad", "2104835": "fp",
    "2282507": "broad", "2231025": "broad", "2059396": "fp",
}


def build_sample() -> pl.DataFrame:
    a = pl.read_parquet(ASSIGN).filter(pl.col("risk_label") == RUNWAY).with_columns(
        pl.col("ACN").cast(pl.Utf8)
    )
    syn = pl.read_parquet(ASRS).select(["ACN", "Synopsis"]).with_columns(pl.col("ACN").cast(pl.Utf8))
    a = a.join(syn, on="ACN", how="left")
    hi = a.filter(pl.col("confidence") >= 0.9).sample(n=18, seed=42)
    lo = a.filter(pl.col("confidence") < 0.9).sample(n=12, seed=42)
    return pl.concat([hi, lo]).sort("confidence", descending=True)


def main() -> None:
    samp = build_sample().with_columns(
        pl.col("ACN").replace_strict(VERDICT, default="UNJUDGED").alias("verdict")
    )

    missing = samp.filter(pl.col("verdict") == "UNJUDGED")
    if missing.height:
        print("WARNING: unjudged ACNs (sample drifted):", missing["ACN"].to_list())

    n = samp.height
    counts = {v: samp.filter(pl.col("verdict") == v).height for v in ("strict", "broad", "fp")}
    prec_broad = (counts["strict"] + counts["broad"]) / n
    prec_strict = counts["strict"] / n

    print(f"Sample N = {n} (flagged positives only -> precision, not recall)")
    print(f"  strict TP : {counts['strict']}")
    print(f"  broad  TP : {counts['broad']}")
    print(f"  false pos : {counts['fp']}")
    print(f"Precision (broad surface/ground relevance) = {prec_broad:.0%}")
    print(f"Precision (strict incursion/conflict)      = {prec_strict:.0%}")
    print()

    # precision by confidence band (shows confidence is informative)
    bands = [(">=0.95", pl.col("confidence") >= 0.95),
             ("0.90", (pl.col("confidence") >= 0.9) & (pl.col("confidence") < 0.95)),
             ("<=0.85", pl.col("confidence") < 0.9)]
    print("Precision (broad) by confidence band:")
    rows = []
    for name, expr in bands:
        b = samp.filter(expr)
        if b.height:
            good = b.filter(pl.col("verdict").is_in(["strict", "broad"])).height
            print(f"  conf {name:>6}: {good}/{b.height} = {good / b.height:.0%}")
            rows.append({"conf_band": name, "n": b.height, "good": good,
                         "precision_broad": round(good / b.height, 3)})

    samp.select(["ACN", "ym", "confidence", "verdict", "Synopsis"]).write_csv(
        OUT_DIR / "narrative_validation_sample.csv"
    )
    pl.DataFrame(rows).write_csv(OUT_DIR / "narrative_validation_by_confidence.csv")
    print(f"\nwrote {OUT_DIR / 'narrative_validation_sample.csv'}")
    print(f"wrote {OUT_DIR / 'narrative_validation_by_confidence.csv'}")


if __name__ == "__main__":
    main()
