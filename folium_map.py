#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shows ALL points from the BernSolarPanelBuildings CSV as Folium markers with detailed popups.
Uses an iterative approach similar to GeoPandas for creating informative popups.
- Input: CSV with LV95 coordinates (default columns: _x, _y)
- Output: Interactive HTML with OSM/Esri layers and LayerControl
Dep: pip install pandas pyproj folium
"""

import argparse
import os
import sys
import pandas as pd
from pyproj import Transformer
import folium

# Candidate pairs (case-insensitive) for convenience
CANDIDATES = [
    ("_x", "_y"),
    ("east_lv95", "north_lv95"),
    ("x_lv95", "y_lv95"),
    ("x", "y"),
    ("east", "north"),
    ("e", "n"),
]


def pick_xy(cols):
    s = {c.lower(): c for c in cols}
    for ex, ny in CANDIDATES:
        if ex in s and ny in s:
            return s[ex], s[ny]
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="dataset/BernSolarPanelBuildings.csv",
                    help="Path to CSV (default: dataset/BernSolarPanelBuildings.csv)")
    ap.add_argument("--x", default="", help="Name of X column (LV95 easting)")
    ap.add_argument("--y", default="", help="Name of Y column (LV95 northing)")
    ap.add_argument("--out", default="maps/bern_map.html",
                    help="Output HTML file")
    ap.add_argument("--limit", type=int, default=0,
                    help="Use only the first N rows (0=all)")
    ap.add_argument("--radius", type=float, default=4.0,
                    help="Marker radius (px, small=2)")
    ap.add_argument("--alpha", type=float, default=0.8,
                    help="Marker opacity [0..1]")
    ap.add_argument("--color", default="#e41a1c",
                    help="Border color (hex or name)")
    ap.add_argument("--fill", default="#e41a1c", help="Fill color")
    args = ap.parse_args()

    # Read header to find columns
    try:
        head = pd.read_csv(args.csv, nrows=0)
    except Exception as e:
        print(f"[ERROR] Unable to read {args.csv}: {e}", file=sys.stderr)
        sys.exit(1)

    cols = list(head.columns)
    x_col = args.x or ""
    y_col = args.y or ""
    if not x_col or not y_col:
        x_col, y_col = pick_xy(cols)

    if not x_col or not y_col:
        print("[ERROR] Coordinate columns not found.", file=sys.stderr)
        print(f"Available columns: {cols}", file=sys.stderr)
        print("Pass explicitly: --x _x --y _y", file=sys.stderr)
        sys.exit(1)

    # Read all columns to have more data for popups
    df = pd.read_csv(args.csv)
    if args.limit > 0:
        df = df.head(args.limit).copy()

    if df.empty:
        print("[INFO] No rows to draw.", file=sys.stderr)
        sys.exit(0)

    # Remove rows with missing or invalid coordinates
    df = df.dropna(subset=[x_col, y_col])
    print(f"[INFO] Valid rows after removing NaN: {len(df)}")

    # Transform LV95 (EPSG:2056) -> WGS84 (EPSG:4326)
    tr = Transformer.from_crs(2056, 4326, always_xy=True)
    lon, lat = tr.transform(df[x_col].values, df[y_col].values)
    df["lon"] = lon
    df["lat"] = lat

    # Check for valid coordinates
    df = df[df["lon"].notna() & df["lat"].notna()]
    print(f"[INFO] Valid rows after transformation: {len(df)}")

    if df.empty:
        print(
            "[ERROR] No valid coordinates found after transformation.", file=sys.stderr)
        sys.exit(1)

    # Center map on average of points
    center_lat = float(df["lat"].mean())
    center_lon = float(df["lon"].mean())

    # Base map
    m = folium.Map(location=[center_lat, center_lon],
                   zoom_start=11, control_scale=True)

    # Base layers (OSM + Esri)
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap",
                     show=True).add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri — Sources: Esri, USGS, IGN, etc.",
        name="Esri Satellite",
        show=False,
    ).add_to(m)

    # FeatureGroup for markers
    fg = folium.FeatureGroup(name="Bern Solar Panel Buildings", show=True)
    m.add_child(fg)

    # Iterazione su righe DataFrame per aggiungere marker con popup
    # Following the requested pattern similar to GeoPandas approach
    for _, row in df.iterrows():
        # Create informative popup with building data
        popup_html = f"""
        <div style='background-color:white; color:black; padding:12px; border-radius:8px; font-family:sans-serif; font-size:13px; max-width:300px;'>
            <b>🏠 Solar Panel Building</b><br><br>
            <b>Address:</b> {row.get('Address', 'N/A')}<br>
            <b>Municipality:</b> {row.get('Municipality', 'N/A')}<br>
            <b>PostCode:</b> {row.get('PostCode', 'N/A')}<br>
            <b>Canton:</b> {row.get('Canton', 'N/A')}<br><br>
            <b>⚡ Power Info:</b><br>
            <b>Total Power:</b> {row.get('TotalPower', 'N/A')} kW<br>
            <b>Installation:</b> {row.get('BeginningOfOperation', 'N/A')}<br><br>
            <b>📍 Coordinates:</b><br>
            Lat: {row['lat']:.6f}<br>
            Lon: {row['lon']:.6f}
        </div>
        """

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, parse_html=True, max_width=350),
            radius=args.radius,
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=args.alpha,
            weight=2
        ).add_to(fg)

    folium.LayerControl(collapsed=False).add_to(m)

    # Save
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    m.save(args.out)
    print(f"[OK] Map saved in {args.out}")


if __name__ == "__main__":
    main()
