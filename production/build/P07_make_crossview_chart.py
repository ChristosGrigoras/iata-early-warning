# provenance: primary=OP48 authors=[OP48] id=P0022 ts=2026-06-20T14:43+03:00
"""Cross-view overlay: the two INDEPENDENT detectors on one axis. The structured
`Conflict Ground Conflict` share and the narrative `runway incursion / ground
conflict / surface movement` share both rise into the 2021-24 window, from
completely separate pipelines (taxonomy tags vs. an LLM reading free text).

Honest caveat baked into the subtitle: the narrative label sits at a higher
base rate (it is broader and bleeds in some airborne conflicts -- see
P04_validate_narrative_labels.py), so what AGREES across the two views is the
direction/timing of the rise, not the absolute level. IATA palette."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import polars as pl

ROOT = Path(__file__).resolve().parent.parent.parent
STRUCT = ROOT / "production/output/signals/category_share_series.parquet"
NARR = ROOT / "production/output/narrative_signals/gliner_label_monthly_share.parquet"
OUT_DIR = ROOT / "production/output/deck"
ASSETS_DIR = ROOT / "writing/assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "#0E4F9E"        # structured view
STEEL = "#5B9BD5"       # narrative view
SLATE = "#2E3440"
GRID = "#E5E7EB"
GRAY = "#6B7280"
AMBER = "#D97706"
AMBER_FILL = "#FCEBCF"
RUNWAY = "runway incursion / ground conflict / surface movement"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.edgecolor": SLATE, "axes.labelcolor": SLATE, "text.color": SLATE,
    "xtick.color": SLATE, "ytick.color": SLATE,
})


def smooth(df: pl.DataFrame) -> pl.DataFrame:
    return df.sort("date").with_columns(
        (pl.col("share") * 100).rolling_mean(window_size=6, center=True, min_samples=3).alias("pct")
    )


def main() -> None:
    s = pl.read_parquet(STRUCT).filter(
        (pl.col("field") == "Anomaly") & (pl.col("category") == "Conflict Ground Conflict")
    )
    n = pl.read_parquet(NARR).filter(pl.col("risk_label") == RUNWAY)
    s, n = smooth(s), smooth(n)

    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=200)

    band_start = mdates.datestr2num("2021-01-01")
    summit = mdates.datestr2num("2023-03-15")
    ax.axvspan(band_start, summit, color=AMBER_FILL, zorder=0)

    ax.plot(n["date"].to_list(), n["pct"].to_list(), color=STEEL, lw=2.6,
            label="Narrative view — LLM reads free text (broader, higher base rate)", zorder=3)
    ax.plot(s["date"].to_list(), s["pct"].to_list(), color=NAVY, lw=2.8,
            label="Structured view — taxonomy tag", zorder=4)

    # narrative first-fire marker (June 2021)
    fire = mdates.datestr2num("2021-06-01")
    ax.axvline(fire, color=AMBER, ls="--", lw=1.6, zorder=5)
    ax.annotate("Narrative view fires\nJune 2021", xy=(fire, 0.96), xycoords=("data", "axes fraction"),
                xytext=(7, 0), textcoords="offset points", color=AMBER, fontsize=9.5,
                fontweight="bold", va="top")

    ax.set_title("Two independent detectors, same direction: surface-conflict risk rising",
                 fontsize=14.5, fontweight="bold", color=SLATE, pad=14, loc="left")
    ax.text(0.0, 1.006,
            "Monthly share · 6-month rolling mean · 2011–2025 · what agrees is the TREND, not the level (narrative label is broader)",
            transform=ax.transAxes, fontsize=9.5, color=GRAY, va="bottom")

    ax.set_ylabel("Share of monthly reports (%)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.grid(axis="x", color=GRID, lw=0.4, alpha=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5, bbox_to_anchor=(0.0, 0.88))

    fig.tight_layout()
    for path in (OUT_DIR / "P07_crossview_overlay.png", ASSETS_DIR / "P07_crossview_overlay.png"):
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
