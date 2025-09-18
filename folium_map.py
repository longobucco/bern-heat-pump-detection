#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shows ALL points from the BernSolarPanelBuildings CSV as Folium markers
    # NOTE: For very large datasets, the HTML can become heavy; here we follow the request "all records".
    valid_coords = df[df["lon"].notna() & df["lat"].notna()]
    print(f"[INFO] Disegnando {len(valid_coords)} punti validi su {len(df)} totali")
    
    for lo, la in zip(valid_coords["lon"].values, valid_coords["lat"].values):
        folium.CircleMarker(
            location=(la, lo),
            radius=args.radius,
            color=args.color,
            weight=0,  # thin border (0=no border)
            fill=True,
            fill_color=args.fill,
            fill_opacity=args.alpha,
        ).add_to(fg)r Folium.
- Input: CSV con coordinate LV95 (default colonne: _x, _y)
- Output: HTML interattivo con layer OSM/Esri e LayerControl
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
                    help="Percorso al CSV (default: dataset/BernSolarPanelBuildings.csv)")
    ap.add_argument("--x", default="", help="Nome colonna X (LV95 easting)")
    ap.add_argument("--y", default="", help="Nome colonna Y (LV95 northing)")
    ap.add_argument("--out", default="bern_map.html",
                    help="File HTML in output")
    ap.add_argument("--limit", type=int, default=0,
                    help="Usa solo le prime N righe (0=tutte)")
    ap.add_argument("--radius", type=float, default=2.0,
                    help="Raggio marker (px, piccolo=2)")
    ap.add_argument("--alpha", type=float, default=0.8,
                    help="Opacità marker [0..1]")
    ap.add_argument("--color", default="#e41a1c",
                    help="Colore bordo (hex o nome)")
    ap.add_argument("--fill", default="#e41a1c", help="Fill color")
    args = ap.parse_args()

    # Read header to find columns
    try:
        head = pd.read_csv(args.csv, nrows=0)
    except Exception as e:
        print(f"[ERRORE] Impossibile leggere {args.csv}: {e}", file=sys.stderr)
        sys.exit(1)

    cols = list(head.columns)
    x_col = args.x or ""
    y_col = args.y or ""
    if not x_col or not y_col:
        x_col, y_col = pick_xy(cols)

    if not x_col or not y_col:
        print("[ERRORE] Colonne coordinate non trovate.", file=sys.stderr)
        print(f"Colonne disponibili: {cols}", file=sys.stderr)
        print("Passa esplicitamente: --x _x --y _y", file=sys.stderr)
        sys.exit(1)

    usecols = [x_col, y_col]
    df = pd.read_csv(args.csv, usecols=usecols)
    if args.limit > 0:
        df = df.head(args.limit).copy()

    if df.empty:
        print("[INFO] Nessuna riga da disegnare.", file=sys.stderr)
        sys.exit(0)

    # Remove rows with missing or invalid coordinates
    df = df.dropna(subset=[x_col, y_col])
    print(f"[INFO] Righe valide dopo rimozione NaN: {len(df)}")

    # Transform LV95 (EPSG:2056) -> WGS84 (EPSG:4326)
    tr = Transformer.from_crs(2056, 4326, always_xy=True)
    lon, lat = tr.transform(df[x_col].values, df[y_col].values)
    df["lon"] = lon
    df["lat"] = lat

    # Check for valid coordinates
    df = df[df["lon"].notna() & df["lat"].notna()]
    print(f"[INFO] Righe valide dopo trasformazione: {len(df)}")

    if df.empty:
        print(
            "[ERRORE] Nessuna coordinata valida trovata dopo la trasformazione.", file=sys.stderr)
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

    # Adds ALL markers as small CircleMarkers
    # NOTE: For very large datasets, the HTML can become heavy; here we follow the request "all records".
    for lo, la in zip(df["lon"].values, df["lat"].values):
        folium.CircleMarker(
            location=(la, lo),
            radius=args.radius,
            color=args.color,
            weight=0,  # bordo sottile (0=nessun bordo)
            fill=True,
            fill_color=args.fill,
            fill_opacity=args.alpha,
        ).add_to(fg)

    folium.LayerControl(collapsed=False).add_to(m)

    # Save
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    m.save(args.out)
    print(f"[OK] Mappa salvata in {args.out}")


if __name__ == "__main__":
    main()
