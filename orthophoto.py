#!/usr/bin/env python3
"""
Build dataset: CSV (EGID, east_lv95, north_lv95, has_heat_pump, ...)
 -> download ortho patches via WMS (EPSG:2056)
 -> create joined CSV with img_path

Usage:
  python make_hp_image_dataset.py \
    --csv bern_buildings.csv \
    --out joined_bern.csv \
    --out_dir patches \
    --buffer_m 40 \
    --size_px 256

Notes:
- Works in LV95 (EPSG:2056). Your CSV already has east_lv95/north_lv95.
- Default layer: ch.swisstopo.swissimage-product (ortofoto).
"""

import os
import time
import math
import argparse
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
from tqdm import tqdm

WMS_URL = "https://wms.geo.admin.ch/"          # WMS endpoint
LAYER = "ch.swisstopo.swissimage-product"    # Swiss ortho layer
CRS = "EPSG:2056"                          # LV95


def bbox_from_point(x, y, r):
    # r = half-size (meters). BBOX for WMS 1.3.0 in LV95
    return f"{x - r},{y - r},{x + r},{y + r}"


def fetch_patch(x, y, r, size=256, timeout=30):
    params = {
        "SERVICE": "WMS",
        "REQUEST": "GetMap",
        "VERSION": "1.3.0",
        "LAYERS": LAYER,
        "STYLES": "default",
        "CRS": CRS,
        "BBOX": bbox_from_point(x, y, r),
        "WIDTH": size,
        "HEIGHT": size,
        "FORMAT": "image/jpeg",
        "DPI": 96,  # optional hint
    }
    resp = requests.get(WMS_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True,
                    help="Input CSV with EGID,east_lv95,north_lv95,has_heat_pump,...")
    ap.add_argument("--out", default="joined.csv",
                    help="Output CSV with img_path")
    ap.add_argument("--out_dir", default="patches",
                    help="Directory where images are saved")
    ap.add_argument("--buffer_m", type=float, default=40.0,
                    help="Half-size of patch (meters). 40 => ~80m window")
    ap.add_argument("--size_px", type=int, default=256,
                    help="Patch size (pixels)")
    ap.add_argument("--limit", type=int, default=0,
                    help="Process only first N rows (0 = all)")
    ap.add_argument("--delay", type=float, default=0.05,
                    help="Seconds between requests (politeness)")
    ap.add_argument("--retries", type=int, default=2,
                    help="Retries per image on error")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    df = pd.read_csv(args.csv)
    if args.limit > 0:
        df = df.head(args.limit).copy()

    img_paths = []
    ok = 0
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Downloading patches"):
        egid = str(row["EGID"])
        x = float(row["east_lv95"])
        y = float(row["north_lv95"])
        out_path = os.path.join(args.out_dir, f"{egid}.jpg")

        if not os.path.exists(out_path):
            attempt = 0
            while True:
                try:
                    img = fetch_patch(x, y, r=args.buffer_m, size=args.size_px)
                    img.save(out_path, "JPEG", quality=95)
                    ok += 1
                    break
                except Exception as e:
                    attempt += 1
                    if attempt > args.retries:
                        out_path = ""  # mark as missing
                        break
                    time.sleep(0.5 * attempt)  # backoff
            time.sleep(args.delay)

        img_paths.append(out_path)

    df["img_path"] = img_paths

    # (Optional) filter rows without image
    # df = df[df["img_path"] != ""].reset_index(drop=True)

    df.to_csv(args.out, index=False)
    print(f"[OK] Saved {ok} images into {args.out_dir}/")
    print(f"[OK] Joined CSV: {args.out} (rows: {len(df)})")


if __name__ == "__main__":
    main()
