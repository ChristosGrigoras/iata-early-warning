# provenance: primary=OP48 authors=[OP48] id=P0035 ts=2026-06-22T14:55+03:00
"""Normality / distributional diagnostic for the robust-z detector.

Question being answered (an interviewer's): the |z| >= 2 / 3 thresholds and the
1.4826 MAD scaling carry a *normal-theory* interpretation. Is the underlying
monthly-share series actually Gaussian, and do the thresholds correspond to the
tail probabilities that normality would imply?

It does NOT assume the answer is "yes". Median/MAD need no normality to be valid
measures of centre/spread; this script quantifies how far from normal the data
is, so the detector can be framed honestly as a *robust screening rank*, not a
calibrated significance test.

Outputs:
  - production/output/eda/P02_normality_diagnostic.png (3-panel figure)
  - a printed summary block (skew, excess kurtosis, Shapiro/normaltest p,
    empirical vs theoretical z-threshold exceedance rates).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent.parent
STRUCT = ROOT / "production/output/signals/category_share_series.parquet"
OUT_DIR = ROOT / "production/output/eda"
OUT_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "#0E4F9E"
STEEL = "#5B9BD5"
SLATE = "#2E3440"
GRID = "#E5E7EB"
GRAY = "#6B7280"
AMBER = "#D97706"
RED = "#B91C1C"

HEADLINE = ("Anomaly", "Conflict Ground Conflict")

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.edgecolor": SLATE, "axes.labelcolor": SLATE, "text.color": SLATE,
    "xtick.color": SLATE, "ytick.color": SLATE,
})


def main() -> None:
    df = pl.read_parquet(STRUCT)

    # --- (1) headline category: the raw monthly-share distribution ---
    gc = (
        df.filter((pl.col("field") == HEADLINE[0]) & (pl.col("category") == HEADLINE[1]))
        .sort("date")
    )
    share_pct = (gc["share"].to_numpy()) * 100.0
    gc_skew = float(stats.skew(share_pct))
    gc_kurt = float(stats.kurtosis(share_pct))  # excess (normal = 0)
    gc_W, gc_p = stats.shapiro(share_pct)

    # --- (2) pooled robust-z across all 42 floor-passing categories ---
    # Under a stationary normal null, z ~ N(0,1). We test that empirically.
    zrows = df.filter(
        (~pl.col("is_trailing_excluded")) & pl.col("z").is_not_null()
    )
    z = zrows["z"].to_numpy()
    z = z[np.isfinite(z)]
    n_z = z.size
    z_skew = float(stats.skew(z))
    z_kurt = float(stats.kurtosis(z))
    # D'Agostino-Pearson (Shapiro is unreliable / capped for n>5000)
    z_k2, z_p = stats.normaltest(z)

    emp_2 = float(np.mean(np.abs(z) >= 2))
    emp_3 = float(np.mean(np.abs(z) >= 3))
    th_2 = 2 * stats.norm.sf(2)   # 0.0455
    th_3 = 2 * stats.norm.sf(3)   # 0.0027

    # ---------- figure ----------
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))

    # Panel A: GC share histogram + fitted normal
    ax = axes[0]
    ax.hist(share_pct, bins=20, color=STEEL, alpha=0.75, edgecolor="white", density=True)
    xs = np.linspace(share_pct.min(), share_pct.max(), 200)
    ax.plot(xs, stats.norm.pdf(xs, share_pct.mean(), share_pct.std(ddof=1)),
            color=NAVY, lw=2, label="fitted normal")
    ax.set_title("A · Ground-conflict monthly share", color=NAVY, fontweight="bold")
    ax.set_xlabel("share of reports (%)")
    ax.set_ylabel("density")
    ax.legend(frameon=False, fontsize=8)
    ax.text(0.97, 0.97,
            f"skew {gc_skew:+.2f}\nexcess kurt {gc_kurt:+.2f}\nShapiro p {gc_p:.1e}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8, color=SLATE)

    # Panel B: Q-Q plot of GC share
    ax = axes[1]
    (osm, osr), (slope, intercept, r) = stats.probplot(share_pct, dist="norm")
    ax.scatter(osm, osr, s=14, color=STEEL, alpha=0.8, edgecolor="none")
    ax.plot(osm, slope * osm + intercept, color=NAVY, lw=2)
    ax.set_title("B · Q–Q vs normal (ground-conflict share)", color=NAVY, fontweight="bold")
    ax.set_xlabel("theoretical normal quantiles")
    ax.set_ylabel("observed share (%)")
    ax.text(0.03, 0.97, f"R$^2$ = {r**2:.3f}", transform=ax.transAxes,
            ha="left", va="top", fontsize=8, color=SLATE)

    # Panel C: pooled z vs standard normal + thresholds
    ax = axes[2]
    ax.hist(z, bins=60, range=(-6, 6), color=GRAY, alpha=0.55,
            edgecolor="white", density=True, label="pooled robust-z")
    xs = np.linspace(-6, 6, 300)
    ax.plot(xs, stats.norm.pdf(xs), color=NAVY, lw=2, label="N(0,1)")
    for t, c in ((2, AMBER), (3, RED)):
        for s in (-1, 1):
            ax.axvline(s * t, color=c, ls="--", lw=1.2)
    ax.set_title("C · Robust-z vs standard normal (42 categories)",
                 color=NAVY, fontweight="bold")
    ax.set_xlabel("robust z")
    ax.set_ylabel("density")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(0.97, 0.97,
            f"|z|≥2: {emp_2*100:.1f}% obs  vs {th_2*100:.1f}% normal\n"
            f"|z|≥3: {emp_3*100:.1f}% obs  vs {th_3*100:.2f}% normal\n"
            f"excess kurt {z_kurt:+.2f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8, color=SLATE)

    fig.suptitle(
        "Distributional diagnostic — the share series is non-normal; "
        "robust z is a screening rank, not a calibrated p-value",
        color=SLATE, fontsize=11, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    out = OUT_DIR / "P02_normality_diagnostic.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"saved {out}")

    # ---------- summary ----------
    print("\n=== Ground-conflict monthly share (n={}) ===".format(share_pct.size))
    print(f"  skew            {gc_skew:+.3f}   (0 = symmetric)")
    print(f"  excess kurtosis {gc_kurt:+.3f}   (0 = normal tails)")
    print(f"  Shapiro-Wilk    W={gc_W:.3f}  p={gc_p:.2e}  "
          f"({'reject' if gc_p < 0.05 else 'cannot reject'} normality)")
    print(f"\n=== Pooled robust-z, 42 categories (n={n_z}) ===")
    print(f"  skew            {z_skew:+.3f}")
    print(f"  excess kurtosis {z_kurt:+.3f}   (>0 = fatter tails than normal)")
    print(f"  D'Agostino      K2={z_k2:.1f}  p={z_p:.2e}  "
          f"({'reject' if z_p < 0.05 else 'cannot reject'} normality)")
    print(f"  P(|z|>=2)  empirical {emp_2*100:.2f}%   normal-theory {th_2*100:.2f}%")
    print(f"  P(|z|>=3)  empirical {emp_3*100:.2f}%   normal-theory {th_3*100:.2f}%")
    print(f"  tail inflation: |z|>=2 x{emp_2/th_2:.1f}, |z|>=3 x{emp_3/th_3:.1f}")


if __name__ == "__main__":
    main()
