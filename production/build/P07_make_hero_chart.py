# provenance: primary=CDX53 authors=[CDX53, OP48] id=P0013 ts=2026-06-19T03:40+03:00
"""Build the deck HERO chart: surface/ground-conflict near-misses rose ~2 years
before the 2023 runway-incursion crisis. Structured view (Conflict Ground
Conflict + Taxi phase share), annotated with the public-crisis markers and the
lead-time band. IATA-aligned palette."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import polars as pl
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Pre-rise baseline window (clean decade, excludes the 2020 COVID distortion).
BASE_LO, BASE_HI = 201101, 201912

ROOT = Path(__file__).resolve().parent.parent.parent
SERIES = ROOT / "production/output/signals/category_share_series.parquet"
NARR = ROOT / "production/output/narrative_signals/gliner_label_monthly_share.parquet"
NARR_LABEL = "runway incursion / ground conflict / surface movement"
OUT_DIR = ROOT / "production/output/deck"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- IATA-aligned palette -------------------------------------------------
NAVY = "#0E4F9E"       # primary — ground-conflict line
STEEL = "#5B9BD5"      # secondary — taxi line
TEAL = "#0F8C7A"       # tertiary — narrative (LLM) line
SLATE = "#2E3440"      # text
GRID = "#E5E7EB"       # gridlines
AMBER = "#D97706"      # semantic: "risk rising" / crisis markers
AMBER_FILL = "#FCEBCF" # lead-time band fill

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": SLATE,
    "axes.labelcolor": SLATE,
    "text.color": SLATE,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
})


def series(df: pl.DataFrame, field: str, category: str) -> pl.DataFrame:
    s = (
        df.filter((pl.col("field") == field) & (pl.col("category") == category))
        .sort("date")
        .with_columns(
            (pl.col("share") * 100).alias("share_pct"),
        )
    )
    # 6-month centered rolling mean for readability (raw is noisy)
    s = s.with_columns(
        pl.col("share_pct").rolling_mean(window_size=6, center=True, min_samples=3).alias("share_smooth")
    )
    return s


def pooled_baseline(s: pl.DataFrame) -> float:
    """Weighted (pooled) baseline share % over 2011–2019: total category count
    / total reports — the honest aggregate rate, robust to monthly volume."""
    d = s.filter((pl.col("ym") >= BASE_LO) & (pl.col("ym") <= BASE_HI))
    return 100.0 * d["count"].sum() / d["total_reports"].sum()


def narrative_series(label: str) -> pl.DataFrame:
    s = (
        pl.read_parquet(NARR)
        .filter(pl.col("risk_label") == label)
        .sort("date")
        .with_columns((pl.col("share") * 100).alias("share_pct"))
    )
    s = s.with_columns(
        pl.col("share_pct").rolling_mean(window_size=6, center=True, min_samples=3).alias("share_smooth")
    )
    return s


def main() -> None:
    df = pl.read_parquet(SERIES)
    gc = series(df, "Anomaly", "Conflict Ground Conflict")
    taxi = series(df, "Aircraft 1 | Flight Phase", "Taxi")
    narr = narrative_series(NARR_LABEL)

    fig, ax = plt.subplots(figsize=(12, 6.4), dpi=200)

    # Lead-time band: signal rises here, BEFORE the public crisis.
    band_start = mdates.datestr2num("2021-01-01")
    summit = mdates.datestr2num("2023-03-15")
    nyt = mdates.datestr2num("2023-08-21")
    ax.axvspan(band_start, summit, color=AMBER_FILL, zorder=0)

    # raw (faint) + smoothed (bold) for each series, plus each line's own
    # 2011–2019 pooled baseline (dotted, same colour) so the eye sees every
    # series DEPART from its historical norm — not just sit at a level.
    label_x = mdates.datestr2num("2011-02-01")
    for s, color, label in [
        (gc, NAVY, "Structured: ground-conflict tag"),
        (taxi, STEEL, "Structured: taxi phase (concurrent)"),
        (narr, TEAL, "Narrative: runway incursion (LLM)"),
    ]:
        x = s["date"].to_list()
        ax.plot(x, s["share_pct"].to_list(), color=color, alpha=0.16, lw=1.0, zorder=2)
        ax.plot(x, s["share_smooth"].to_list(), color=color, lw=2.6, label=label, zorder=3)
        base = pooled_baseline(s)
        ax.axhline(base, color=color, ls=":", lw=1.2, alpha=0.7, zorder=1.5)
        ax.text(label_x, base, f"{base:.1f}%", color=color, fontsize=8.5, fontweight="bold",
                va="center", ha="left",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=1.0), zorder=7)

    # ♦ mark where the narrative (LLM) view independently fires (June 2021)
    fire = mdates.datestr2num("2021-06-01")
    narr_fire = (
        narr.filter(pl.col("ym") == 202106)["share_smooth"].to_list()
    )
    fire_y = narr_fire[0] if narr_fire and narr_fire[0] is not None else 18.0
    ax.scatter([fire], [fire_y], marker="D", s=110, color=TEAL,
               edgecolor="white", linewidth=1.2, zorder=6)
    ax.annotate("Narrative view fires\n(independent) · Jun 2021",
                xy=(fire, fire_y), xytext=(8, 14), textcoords="offset points",
                color=TEAL, fontsize=9.5, fontweight="bold", va="bottom",
                arrowprops=dict(arrowstyle="-", color=TEAL, lw=1.0))

    # crisis markers
    for xpos in (summit, nyt):
        ax.axvline(xpos, color=AMBER, ls="--", lw=1.6, zorder=4)
    ax.annotate("FAA emergency\nSafety Summit\nMar 2023", xy=(summit, 0.74), xycoords=("data", "axes fraction"),
                xytext=(7, 0), textcoords="offset points", color=AMBER, fontsize=9.5, fontweight="bold", va="center")
    ax.annotate("NYT close-calls\nexposé · Aug 2023", xy=(nyt, 0.30), xycoords=("data", "axes fraction"),
                xytext=(7, 0), textcoords="offset points", color=AMBER, fontsize=9.5, va="center")

    # lead-time label inside the band (refers to the navy Ground-Conflict line)
    ax.annotate("Ground-conflict share\nrises here · ~12–18 mo lead",
                xy=(mdates.datestr2num("2021-10-01"), 0.94), xycoords=("data", "axes fraction"),
                color=AMBER, fontsize=10, fontweight="bold", ha="center", va="top")

    ax.set_title("Ground-conflict reports rose above their decade baseline before 2023",
                 fontsize=15, fontweight="bold", color=SLATE, pad=14, loc="left")
    ax.text(0.0, 1.005, "Share of monthly ASRS reports · 6-mo rolling mean · 2011–2025 · dotted = each line's 2011–19 baseline · ♦ = narrative (LLM) view fires independently",
            transform=ax.transAxes, fontsize=9.5, color="#6B7280", va="bottom")

    ax.set_ylabel("Share of monthly reports (%)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.grid(axis="x", color=GRID, lw=0.4, alpha=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    handles, labels = ax.get_legend_handles_labels()
    handles.append(Patch(facecolor=AMBER_FILL, label="Lead-time window (pre-crisis)"))
    handles.append(Line2D([0], [0], color=SLATE, ls=":", lw=1.2, label="2011–19 baseline (per line)"))
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=10,
              bbox_to_anchor=(0.0, 0.86))

    fig.tight_layout()
    out = OUT_DIR / "P07_hero_surface_conflict.png"
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
