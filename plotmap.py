#!/usr/bin/env python3
"""
Plot Swiss CH1903+ / LV95 (EPSG:2056) points on a satellite basemap.

Examples:
  # Hexbin on satellite (dataset with columns _x/_y)
  python plotmap.py --csv dataset/BernSolarPanelBuildings.csv --x _x --y _y --out bern_hexbin.png --kind hexbin --gridsize 120

  # Scatter on satellite (dataset with east_lv95/north_lv95)
  python plotmap.py --csv bern_buildings.csv --x east_lv95 --y north_lv95 --out bern_scatter.png --kind scatter --s 0.5
"""

import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
from owslib.wfs import WebFeatureService


CANDIDATES = [
    ("east_lv95", "north_lv95"),
    ("x_lv95", "y_lv95"),
    ("_x", "_y"),
    ("x", "y"),
    ("east", "north"),
    ("e", "n"),
]


def load_canton_boundary(canton_code="BE"):
    """Download canton boundary from swisstopo WFS and return GeoDataFrame in EPSG:3857"""
    url = "https://wfs.geo.admin.ch/?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities"
    wfs = WebFeatureService(url=url, version="2.0.0")
    layer = "ch.swisstopo.swissboundaries3d-kanton-flaeche.fill"

    response = wfs.getfeature(typename=layer, outputFormat="application/json")
    gdf = gpd.read_file(response)
    gdf = gdf[gdf["KANTONSABK"] == canton_code]
    gdf = gdf.to_crs(epsg=3857)
    return gdf


def pick_xy(cols):
    s = {c.lower(): c for c in cols}
    for ex, ny in CANDIDATES:
        if ex in s and ny in s:
            return s[ex], s[ny]
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True,
                    help="Input CSV with LV95 coordinates")
    ap.add_argument("--x", default="", help="X column (LV95 eastings)")
    ap.add_argument("--y", default="", help="Y column (LV95 northings)")
    ap.add_argument("--out", default="plot.png",
                    help="Output PNG path (saved under images/)")
    ap.add_argument(
        "--kind", choices=["scatter", "hexbin"], default="hexbin", help="Plot type")
    ap.add_argument("--sample", type=int, default=0,
                    help="Plot only first N rows (0 = all)")
    ap.add_argument("--s", type=float, default=1.0,
                    help="Marker size for scatter")
    ap.add_argument("--alpha", type=float, default=0.5,
                    help="Alpha for points/hexes")
    ap.add_argument("--gridsize", type=int, default=100,
                    help="Hexbin gridsize (higher = finer)")
    args = ap.parse_args()

    # dataset header
    head = pd.read_csv(args.csv, nrows=0)
    cols = list(head.columns)

    x_col = args.x or ""
    y_col = args.y or ""
    if not x_col or not y_col:
        x_col, y_col = pick_xy(cols)
    if not x_col or not y_col:
        print("[ERROR] Could not determine coordinate columns.", file=sys.stderr)
        print(f"Available columns: {cols}", file=sys.stderr)
        print("Pass them explicitly, e.g.: --x _x --y _y", file=sys.stderr)
        sys.exit(1)

    # only coordinates
    df = pd.read_csv(args.csv, usecols=[x_col, y_col])
    if args.sample and args.sample > 0:
        df = df.head(args.sample)

    # GeoDataFrame in LV95 -> 3857 for web basemap
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df[x_col], df[y_col]), crs="EPSG:2056")
    gdf3857 = gdf.to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(8, 8))
    if args.kind == "scatter":
        ax.scatter(gdf3857.geometry.x, gdf3857.geometry.y,
                   s=args.s, alpha=args.alpha)
    else:
        hb = ax.hexbin(gdf3857.geometry.x, gdf3857.geometry.y,
                       gridsize=args.gridsize)
        hb.set_alpha(args.alpha)  # default colors

    # limits + padding
    x_min, x_max = gdf3857.geometry.x.min(), gdf3857.geometry.x.max()
    y_min, y_max = gdf3857.geometry.y.min(), gdf3857.geometry.y.max()
    pad_x = (x_max - x_min) * 0.02
    pad_y = (y_max - y_min) * 0.02
    ax.set_xlim(x_min - pad_x, x_max + pad_x)
    ax.set_ylim(y_min - pad_y, y_max + pad_y)

    # satellite basemap
    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery,
                    crs=gdf3857.crs.to_string())

    # attempt to plot Bern canton boundary
    try:
        canton_gdf = load_canton_boundary("BE")
        canton_gdf.plot(ax=ax, facecolor="none",
                        edgecolor="red", linewidth=2, zorder=10)
    except Exception as e:
        print(f"[WARN] Could not load canton boundary: {e}", file=sys.stderr)

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(f"{x_col} (LV95, m)")
    ax.set_ylabel(f"{y_col} (LV95, m)")
    ax.set_title(
        "Buildings in Canton Bern on Satellite (LV95 -> Web Mercator)")

    plt.tight_layout()
    os.makedirs("images", exist_ok=True)
    out_filename = os.path.basename(args.out)
    out_path = os.path.join("images", out_filename)
    fig.savefig(out_path, dpi=200)
    print(f"[OK] Saved {out_path}")


if __name__ == "__main__":
    main()
