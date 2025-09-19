#!/usr/bin/env python3
import os
import pandas as pd
import requests
from urllib.parse import urlencode

# Input dataset: columns "GKODE","GKODN" in LV95 / EPSG:2056
CSV_PATH = "dataset/building_sample_BE.csv"
OUT_DIR = "unlabeled-orthophoto-256px"

WIDTH = HEIGHT = 256
# 20 cm per pixel (double the area compared to 0.10 m/px)
M_PER_PX = 0.075
LAYER = "ch.swisstopo.swissimage-product"  # High-res orthophoto
WMS_URL = "https://wms.geo.admin.ch/"


def download_ortho(x, y, out_file):
    half = (WIDTH * M_PER_PX) / 2.0
    minx, miny, maxx, maxy = x - half, y - half, x + half, y + half

    params = {
        "SERVICE": "WMS",
        "REQUEST": "GetMap",
        "VERSION": "1.3.0",
        "LAYERS": LAYER,
        "STYLES": "",
        "CRS": "EPSG:2056",
        "BBOX": f"{minx},{miny},{maxx},{maxy}",
        "WIDTH": WIDTH,
        "HEIGHT": HEIGHT,
        "FORMAT": "image/png"
    }

    url = f"{WMS_URL}?{urlencode(params)}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(out_file, "wb") as f:
        f.write(r.content)


def main():
    df = pd.read_csv(CSV_PATH)
    os.makedirs(OUT_DIR, exist_ok=True)

    for i, row in df.iterrows():
        x, y = float(row["GKODE"]), float(row["GKODN"])
        out_file = os.path.join(OUT_DIR, f"ortho_{int(x)}_{int(y)}.png")

        try:
            download_ortho(x, y, out_file)
            print(f"[OK] Saved {out_file}")
        except Exception as e:
            print(f"[WARN] Failed {x},{y}: {e}")


if __name__ == "__main__":
    main()