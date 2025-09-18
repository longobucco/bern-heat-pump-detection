#!/usr/bin/env python3
import pandas as pd
import os

# Dataset with building coordinates in GK
BUILDINGS_PATH = "dataset/buildings_BE.csv"
# Dataset with buildings that have solar panels
BERN_PATH = "dataset/BernSolarPanelBuildings.csv"
# Output dataset with matching x,y columns only
OUTPUT_PATH = "dataset/buildings_BE_matches_xy.csv"


def left_of_dot_to_int(series: pd.Series) -> pd.Series:
    # Keep only the part before the decimal point, then cast to int
    s = series.astype(str).str.split(".", n=1, expand=True)[0]
    return pd.to_numeric(s, errors="coerce").astype("Int64")


def main():
    if not os.path.exists(BUILDINGS_PATH):
        print(f"File not found: {BUILDINGS_PATH}")
        return
    if not os.path.exists(BERN_PATH):
        print(f"File not found: {BERN_PATH}")
        return

    # buildings_BE.csv: expected GKODE, GKODN (with decimals)
    bld = pd.read_csv(BUILDINGS_PATH, dtype=str)
    if not {"GKODE", "GKODN"}.issubset(bld.columns):
        print("Missing GKODE/GKODN columns in buildings_BE.csv")
        return
    bld["x_int"] = left_of_dot_to_int(bld["GKODE"])
    bld["y_int"] = left_of_dot_to_int(bld["GKODN"])
    bld = bld.dropna(subset=["x_int", "y_int"])

    # BernSolarPanelBuildings.csv: expected _x, _y (integers)
    bern = pd.read_csv(BERN_PATH)
    if not {"_x", "_y"}.issubset(bern.columns):
        print("Missing _x/_y columns in BernSolarPanelBuildings.csv")
        return
    bern["_x"] = pd.to_numeric(bern["_x"], errors="coerce").astype("Int64")
    bern["_y"] = pd.to_numeric(bern["_y"], errors="coerce").astype("Int64")
    bern = bern.dropna(subset=["_x", "_y"])

    # Match on x,y
    merged = bld.merge(bern, left_on=["x_int", "y_int"], right_on=[
                       "_x", "_y"], how="inner")

    # New dataset with only x,y columns (from matched values)
    result = merged.rename(columns={"_x": "x", "_y": "y"})[
        ["x", "y"]].drop_duplicates()

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"Matches found: {len(result)}")
    print(f"File saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
