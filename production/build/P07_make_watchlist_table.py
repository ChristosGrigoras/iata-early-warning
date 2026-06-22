# provenance: primary=OP48 authors=[OP48] id=P0023 ts=2026-06-20T14:43+03:00
"""Render the 'monthly watchlist' artifact the deck promises: a ranked,
explainable shortlist of currently/recently elevated risk signals drawn from
BOTH detectors (structured taxonomy + narrative LLM). Turns the slide's claim
into a concrete table. Stats are pulled live from the candidate CSVs so the
numbers cannot drift from the pipeline. IATA palette."""

from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl

ROOT = Path(__file__).resolve().parent.parent.parent
NARR_CSV = ROOT / "production/output/narrative_signals/narrative_signal_candidates.csv"
STRUCT_CSV = ROOT / "production/output/signals/signal_candidates.csv"
OUT_DIR = ROOT / "production/output/deck"
ASSETS_DIR = ROOT / "writing/assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "#0E4F9E"
STEEL = "#5B9BD5"
SLATE = "#2E3440"
AMBER = "#D97706"
ROW_ALT = "#F3F6FB"


def fmt_fire(ym) -> str:
    if ym is None:
        return "—"
    ym = int(ym)
    return f"{ym // 100}-{ym % 100:02d}"


def main() -> None:
    narr = pl.read_csv(NARR_CSV)
    struct = pl.read_csv(STRUCT_CSV)

    def nrow(label):
        r = narr.filter(pl.col("risk_label") == label)
        return r.row(0, named=True) if r.height else None

    def srow(cat):
        r = struct.filter(pl.col("category") == cat)
        return r.row(0, named=True) if r.height else None

    # Curated, honest watchlist: signal, view, source row, note.
    spec = [
        ("GPS interference / jamming", "Narrative", nrow("GPS interference or jamming"), "peak_z", "first_fire_ym", ""),
        ("Runway / ground conflict", "Both views", nrow("runway incursion / ground conflict / surface movement"), "peak_z", "first_fire_ym", "headline · structured trend agrees"),
        ("Smoke / fire / fumes / odor", "Both views", nrow("smoke fire fumes odor"), "peak_z", "first_fire_ym", ""),
        ("UAS / drone encounter", "Narrative", nrow("UAS or drone encounter"), "peak_z", "first_fire_ym", ""),
        ("Unstabilized approach", "Narrative", nrow("unstabilized approach"), "peak_z", "first_fire_ym", ""),
        ("Crew / ATC workload strain", "Structured", srow("Workload"), "peak_z", "first_fire_ym", "post-COVID; reverting 2025"),
    ]

    headers = ["Risk signal", "View", "First fire", "Peak z", "Status / note"]
    rows = []
    for name, view, src, zk, fk, note in spec:
        if src is None:
            continue
        z = src.get(zk)
        fire = fmt_fire(src.get(fk))
        status = str(src.get("fire_level", "")).strip()
        status_note = status if not note else f"{status} · {note}"
        rows.append([name, view, fire, f"{z:.1f}" if z is not None else "—", status_note])

    fig, ax = plt.subplots(figsize=(12, 4.2), dpi=200)
    ax.axis("off")
    ax.set_position([0.02, 0.02, 0.96, 0.72])  # leave headroom for titles
    tbl = ax.table(cellText=rows, colLabels=headers, cellLoc="left", loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.7)

    ncol = len(headers)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#FFFFFF")
        cell.set_linewidth(1.2)
        if r == 0:
            cell.set_facecolor(NAVY)
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor(ROW_ALT if r % 2 == 0 else "white")
            cell.set_text_props(color=SLATE)
    # widen the signal + status columns
    widths = [0.27, 0.13, 0.12, 0.10, 0.38]
    for (r, c), cell in tbl.get_celld().items():
        cell.set_width(widths[c])

    fig.text(0.02, 0.93, "Monthly watchlist — ranked, explainable shortlist from both detectors",
             fontsize=14, fontweight="bold", color=SLATE, ha="left", va="top")
    fig.text(0.02, 0.85,
             "Candidates for human review, not alarms · 'peak z' = strength of the share anomaly · status from the persistence rule",
             fontsize=9, color="#6B7280", ha="left", va="top")

    for path in (OUT_DIR / "P07_watchlist_table.png", ASSETS_DIR / "P07_watchlist_table.png"):
        fig.savefig(path, bbox_inches="tight", facecolor="white", dpi=200)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
