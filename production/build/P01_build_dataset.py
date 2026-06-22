# provenance: primary=OP48 authors=[OP48]
"""Build the combined ASRS dataset from yearly DBOL CSV exports.

Each raw CSV has a two-row header (row 0 = category group, row 1 = field name),
a blank separator line, then data. Field names repeat across groups (Aircraft 1/2,
Person 1/2, Report 1/2), so we disambiguate by prefixing the group where a field
name is not globally unique. pandas parses the messy quoting/embedded newlines in
narratives more robustly than a strict CSV reader; we then dedupe by ACN (yearly
chunks overlap by one month) and write Parquet for Polars-based analysis.

Usage: python P01_build_dataset.py      # data/raw/*.csv -> data/processed/asrs.parquet
"""
import glob
import os
from collections import Counter

import pandas as pd

RAW_DIR = "data/raw"
OUT = "data/processed/asrs.parquet"


def flatten_columns(cols):
    fields = [str(f).strip() for (_g, f) in cols]
    counts = Counter(fields)
    names, seen = [], Counter()
    for (g, f) in cols:
        g, f = str(g).strip(), str(f).strip()
        base = f if counts[f] == 1 else (f"{g} | {f}" if g else f)
        seen[base] += 1
        names.append(base if seen[base] == 1 else f"{base} ({seen[base]})")
    return names


def load_one(path):
    df = pd.read_csv(
        path, header=[0, 1], dtype=str,
        keep_default_na=False, na_filter=False, skip_blank_lines=True,
    )
    df.columns = flatten_columns(list(df.columns))
    df["src_year"] = os.path.splitext(os.path.basename(path))[0].replace("asrs_", "")
    return df


def main():
    paths = sorted(glob.glob(os.path.join(RAW_DIR, "asrs_*.csv")))
    if not paths:
        raise SystemExit(f"No CSVs in {RAW_DIR}")
    frames = []
    for p in paths:
        df = load_one(p)
        print(f"{os.path.basename(p)}: {df.shape[0]} rows, {df.shape[1]} cols")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    before = len(combined)
    combined = combined.drop_duplicates(subset=["ACN"], keep="first").reset_index(drop=True)
    after = len(combined)
    print(f"\ncombined: {before} rows -> {after} unique ACNs (removed {before - after} overlap dupes)")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    combined.to_parquet(OUT, index=False)
    print(f"wrote {OUT} ({os.path.getsize(OUT)/1e6:.1f} MB), {combined.shape[1]} columns")


if __name__ == "__main__":
    main()
