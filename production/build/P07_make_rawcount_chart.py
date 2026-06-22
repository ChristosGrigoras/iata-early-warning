# provenance: primary=OP48 authors=[OP48] id=P0020 ts=2026-06-20T14:21+03:00
"""Build the appendix / Q&A-backup chart that defuses the compositional-data
objection ("a share can rise just because the denominator or other categories
moved"). Plots the ground-conflict RAW monthly count (numerator) against the
total monthly reports (denominator) on twin axes: the numerator roughly tripled
while the denominator stayed flat, so the rising share reflects a real rise in
ground-conflict reports, not a composition artifact. IATA-aligned palette,
consistent with P07_make_hero_chart.py."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import polars as pl
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent.parent
SERIES = ROOT / "production/output/signals/category_share_series.parquet"
OUT_DIR = ROOT / "production/output/deck"
ASSETS_DIR = ROOT / "writing/assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# --- IATA-aligned palette (matches P07_make_hero_chart.py) --------------------
NAVY = "#0E4F9E"       # numerator — ground-conflict count
STEEL = "#5B9BD5"
SLATE = "#2E3440"      # text
GRID = "#E5E7EB"
GRAY = "#6B7280"       # denominator — total reports
AMBER = "#D97706"      # semantic: crisis markers
AMBER_FILL = "#FCEBCF" # lead-time band fill (matches P07_make_hero_chart.py)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": SLATE,
    "axes.labelcolor": SLATE,
    "text.color": SLATE,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
})


def main() -> None:
    df = pl.read_parquet(SERIES)
    gc = (
        df.filter((pl.col("field") == "Anomaly") & (pl.col("category") == "Conflict Ground Conflict"))
        .sort("date")
        .with_columns([
            pl.col("count").rolling_mean(window_size=6, center=True, min_samples=3).alias("gc_smooth"),
            pl.col("total_reports").rolling_mean(window_size=6, center=True, min_samples=3).alias("tot_smooth"),
        ])
    )
    x = gc["date"].to_list()

    fig, ax = plt.subplots(figsize=(12, 6.4), dpi=200)
    ax2 = ax.twinx()

    # Lead-time band + crisis markers (same dates as the hero chart) so the
    # "when" is explicit here too: the numerator climbs through the pre-crisis
    # window, BEFORE the public inflection.
    band_start = mdates.datestr2num("2021-01-01")
    summit = mdates.datestr2num("2023-03-15")
    nyt = mdates.datestr2num("2023-08-21")
    ax2.axvspan(band_start, summit, color=AMBER_FILL, zorder=0)
    for xpos in (summit, nyt):
        ax.axvline(xpos, color=AMBER, ls="--", lw=1.4, zorder=5)
    ax.annotate("Ground-conflict count\nclimbs here · pre-crisis",
                xy=(mdates.datestr2num("2021-10-01"), 0.95), xycoords=("data", "axes fraction"),
                color=AMBER, fontsize=9.5, fontweight="bold", ha="center", va="top")
    ax.annotate("FAA Safety\nSummit · Mar 2023", xy=(summit, 0.40), xycoords=("data", "axes fraction"),
                xytext=(7, 0), textcoords="offset points", color=AMBER, fontsize=9, fontweight="bold", va="center")
    ax.annotate("NYT close-calls\nexposé · Aug 2023", xy=(nyt, 0.18), xycoords=("data", "axes fraction"),
                xytext=(7, 0), textcoords="offset points", color=AMBER, fontsize=9, va="center")

    # Denominator (right axis): total monthly reports — flat band, gray.
    ax2.plot(x, gc["total_reports"].to_list(), color=GRAY, alpha=0.16, lw=1.0, zorder=1)
    ax2.plot(x, gc["tot_smooth"].to_list(), color=GRAY, lw=2.4, ls="--",
             label="Total reports / month (denominator)", zorder=2)

    # Numerator (left axis): ground-conflict monthly count — rising, navy.
    ax.plot(x, gc["count"].to_list(), color=NAVY, alpha=0.18, lw=1.0, zorder=3)
    ax.plot(x, gc["gc_smooth"].to_list(), color=NAVY, lw=2.8,
            label="Ground-conflict reports / month (numerator)", zorder=4)

    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)

    ax.set_title("The share rise is real: ground-conflict counts climbed while total reporting stayed flat",
                 fontsize=14.5, fontweight="bold", color=SLATE, pad=14, loc="left")
    ax.text(0.0, 1.006, "Monthly ASRS reports · 6-month rolling mean · 2011–2025 · numerator ≈ tripled, denominator flat → not a compositional artifact",
            transform=ax.transAxes, fontsize=9.5, color=GRAY, va="bottom")

    ax.set_ylabel("Ground-conflict reports / month", color=NAVY)
    ax2.set_ylabel("Total reports / month", color=GRAY)
    ax.tick_params(axis="y", colors=NAVY)
    ax2.tick_params(axis="y", colors=GRAY)
    ax.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.grid(axis="x", color=GRID, lw=0.4, alpha=0.5)
    for sp in ("top",):
        ax.spines[sp].set_visible(False)
        ax2.spines[sp].set_visible(False)

    # combined legend (both axes)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    band_patch = Patch(facecolor=AMBER_FILL, label="Lead-time window (pre-crisis)")
    ax.legend(h1 + h2 + [band_patch], l1 + l2 + ["Lead-time window (pre-crisis)"],
              loc="upper left", frameon=False, fontsize=10, bbox_to_anchor=(0.0, 0.98))

    fig.tight_layout()
    out = OUT_DIR / "P07_rawcount_ground_conflict.png"
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    # mirror into the deck asset folder so the slide can embed it
    asset = ASSETS_DIR / "P07_rawcount_ground_conflict.png"
    fig.savefig(asset, bbox_inches="tight", facecolor="white")
    print(f"wrote {out}")
    print(f"wrote {asset}")


if __name__ == "__main__":
    main()
