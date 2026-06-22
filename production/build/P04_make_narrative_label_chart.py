# provenance: primary=OP48 authors=[OP48] id=P0039 ts=2026-06-22T16:55+03:00
"""Regenerate the per-label narrative-signal diagnostic plots
(`production/output/narrative_signals/plots/P04_label_*.png`) with the trend
ONSET made explicit: a vertical line at the first persisted fire month plus a
shaded persistence run, on top of the existing share / 24-month baseline /
±1-MAD / watch-strong layers.

Reads the persisted scored series + candidates (no LLM re-run needed); mirrors
the firing logic baked into `P04_03-narrative-signals.ipynb`. Run:
    python production/build/P04_make_narrative_label_chart.py
"""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import polars as pl

ROOT = Path(__file__).resolve().parent.parent.parent
NARR_DIR = ROOT / "production/output/narrative_signals"
SCORED = NARR_DIR / "gliner_label_monthly_share.parquet"
CAND = NARR_DIR / "narrative_signal_candidates.csv"
PLOT_DIR = NARR_DIR / "plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# Clear, consistent palette (diagnostic, not a deck figure).
BLUE = "#0E4F9E"    # share line
ORANGE = "#D97706"  # 24m baseline + fire marker
BANDC = "#9DC3E6"   # ±1 MAD fill
WATCH = "#E8A33D"   # watch months
STRONG = "#0F8C7A"  # strong months
FIREC = "#C0392B"   # first-fire line + persistence shading


def safe_name(label: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in label)[:90]


def persistence_run(g: pd.DataFrame, first_fire: int, level: str) -> tuple:
    """Return (start_date, end_date) of the consecutive fire run that begins at
    first_fire, using the firing column for the achieved level."""
    col = "strong_fire" if level == "strong" else "watch_fire"
    idx = g.index[g["ym"] == first_fire]
    if len(idx) == 0:
        return None, None
    i0 = g.index.get_loc(idx[0])
    run = 0
    for i in range(i0, len(g)):
        if bool(g[col].iloc[i]):
            run += 1
        else:
            break
    if run == 0:
        return None, None
    start = g["date"].iloc[i0]
    end = g["date"].iloc[i0 + run - 1] + pd.offsets.MonthEnd(1)
    return start, end


def main() -> None:
    scored = pl.read_parquet(SCORED).to_pandas()
    cand = pl.read_csv(CAND).to_pandas()
    fired = cand[cand["first_fire_ym"].notna()]

    for _, row in fired.iterrows():
        lbl = row["risk_label"]
        level = str(row["fire_level"])
        first_fire = int(row["first_fire_ym"])
        g = scored[scored["risk_label"] == lbl].sort_values("ym").reset_index(drop=True)

        fig, ax = plt.subplots(figsize=(11.5, 4.2), dpi=140)
        ax.plot(g["date"], g["share"], color=BLUE, lw=1.6, label="Share", zorder=4)
        ax.plot(g["date"], g["median_24"], color=ORANGE, lw=1.1, label="24m baseline", zorder=3)
        band = 1.4826 * g["mad_24"]
        ax.fill_between(g["date"], g["median_24"] - band, g["median_24"] + band,
                        color=BANDC, alpha=0.30, lw=0, label="\u00b11 MAD", zorder=1)

        # persistence run + first-fire line (the trend ONSET)
        start, end = persistence_run(g, first_fire, level)
        fire_date = pd.to_datetime(str(first_fire), format="%Y%m")
        if start is not None:
            ax.axvspan(start, end, color=FIREC, alpha=0.12, zorder=0,
                       label="persistence run (\u22653 mo)")
        ax.axvline(fire_date, color=FIREC, ls="--", lw=1.6, zorder=5)
        ax.annotate(f"first persisted fire\n{fire_date:%b %Y} ({level})",
                    xy=(fire_date, 0.97), xycoords=("data", "axes fraction"),
                    xytext=(6, 0), textcoords="offset points",
                    color=FIREC, fontsize=8.5, fontweight="bold", va="top")

        wf = g[g["watch_fire"]]
        sf = g[g["strong_fire"]]
        if not wf.empty:
            ax.scatter(wf["date"], wf["share"], s=18, color=WATCH, label="watch", zorder=6)
        if not sf.empty:
            ax.scatter(sf["date"], sf["share"], s=22, color=STRONG, label="strong", zorder=7)
        tr = g[g["is_trailing_excluded"]]
        if not tr.empty:
            ax.axvspan(tr["date"].min(), tr["date"].max() + pd.offsets.MonthEnd(1),
                       color="gray", alpha=0.12, zorder=0)

        ax.set_title(lbl)
        ax.set_xlabel("Year")
        ax.set_ylabel("Narrative label share")
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.tick_params(axis="x", rotation=0)
        ax.legend(fontsize=8, ncol=2)
        fig.tight_layout()
        out = PLOT_DIR / f"P04_label_{safe_name(lbl)}.png"
        fig.savefig(out, bbox_inches="tight")
        plt.close(fig)
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
