# provenance: primary=OP48 authors=[OP48]
"""Extract the CSV payload from a browser-MCP CDP Runtime.evaluate log file.

The DBOL export is fetched in-browser via fetch().text(); large CDP responses are
spilled to a JSON log file. This pulls the string value out and writes it as a CSV.

Usage: python P01_extract_cdp_csv.py <cdp_log.json> <out.csv>
"""
import json
import os
import sys


def find_csv(o):
    if isinstance(o, dict):
        if o.get("type") == "string" and isinstance(o.get("value"), str):
            return o["value"]
        for v in o.values():
            r = find_csv(v)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_csv(v)
            if r is not None:
                return r
    return None


def main():
    src, out = sys.argv[1], sys.argv[2]
    data = json.load(open(src))
    csv_text = find_csv(data)
    if not csv_text:
        raise SystemExit(f"No CSV string found in {src}")
    reported = None
    if csv_text.startswith("COUNT="):
        nl = csv_text.index("\n")
        reported = csv_text[:nl].strip()
        csv_text = csv_text[nl + 1:]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(csv_text)
    # data rows = total lines minus 2 header rows minus 1 blank separator
    nlines = csv_text.count("\n")
    print(f"wrote {out} ({os.path.getsize(out)} bytes) reported_ACNs={reported} ~lines={nlines}")


if __name__ == "__main__":
    main()
