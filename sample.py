#!/usr/bin/env python3
import pandas as pd
import os

INPUT_FILE = "dataset/buildings_BE.csv"
OUTPUT_FILE = "dataset/building_sample_BE.csv"
N_SAMPLES = 24000

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] File not found: {INPUT_FILE}")
        return

    # load dataset
    df = pd.read_csv(INPUT_FILE)

    # random sample
    if len(df) < N_SAMPLES:
        print(f"[WARN] Dataset has only {len(df)} rows, saving all.")
        df_sample = df
    else:
        df_sample = df.sample(n=N_SAMPLES, random_state=42)

    # save sample
    df_sample.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"[OK] Saved {len(df_sample)} samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
