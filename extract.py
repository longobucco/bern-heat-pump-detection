#!/usr/bin/env python3
"""
Extract GWR buildings for a canton (default: BE) from data.sqlite (MADD/GWR)
and save a CSV with: EGID, east_lv95, north_lv95, has_heat_pump, heat_source_1, heat_source_2,
+ (if pyproj is installed) lon/lat in WGS84.

Usage:
    python export_gwr_canton.py --sqlite /path/to/data.sqlite --canton BE --out bern_buildings.csv
"""

import argparse
import sqlite3
import sys
import pandas as pd


def maybe_add_lonlat(df):
    try:
        from pyproj import Transformer
        tr = Transformer.from_crs(2056, 4326, always_xy=True)  # LV95 -> WGS84
        lon, lat = tr.transform(
            df["east_lv95"].values, df["north_lv95"].values)
        df["lon"] = lon
        df["lat"] = lat
    except Exception as e:
        print(
            f"[WARNING] lon/lat not added (pyproj missing or error: {e})", file=sys.stderr)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sqlite", required=True,
                    help="Path to data/data.sqlite (from CH.zip or canton)")
    ap.add_argument("--canton", default="BE",
                    help="Canton code to filter (e.g. BE, ZH, VD...)")
    ap.add_argument("--out", default="buildings_canton.csv",
                    help="Output CSV file")
    ap.add_argument("--sep", default=",",
                    help="CSV separator (default ,). For TSV use '\t'")
    args = ap.parse_args()

    # If the user does not specify the path, use data/data.sqlite as default
    db_path = args.sqlite if args.sqlite != "data.sqlite" else "data/data.sqlite"
    conn = sqlite3.connect(db_path)
    query = """
        SELECT
          EGID,
          GKODE AS east_lv95,
          GKODN AS north_lv95,
          CASE WHEN GWAERZH1 = 7410 OR GWAERZH2 = 7410 THEN 1 ELSE 0 END AS has_heat_pump,
          GENH1 AS heat_source_1,
          GENH2 AS heat_source_2,
          GDEKT AS canton
        FROM building
        WHERE GDEKT = ?
    """
    df = pd.read_sql_query(query, conn, params=(args.canton,))
    conn.close()

    if df.empty:
        print(
            f"[INFO] No records found for canton {args.canton}.", file=sys.stderr)
    else:
        df = maybe_add_lonlat(df)
        df.to_csv(args.out, index=False, sep=args.sep)
        print(f"[OK] Saved {len(df):,} records to {args.out}")


if __name__ == "__main__":
    main()
