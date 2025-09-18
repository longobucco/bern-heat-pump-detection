# Heat Pumps Detection

This project builds a geospatial dataset for **heat pump detection from aerial imagery**.  
It combines official Swiss building register data (GWR/REA via MADD) with orthophotos from **swisstopo (SWISSIMAGE)**.

---

## 1. Extract buildings for a specific canton

Use the `extract.py` script to filter buildings for a given canton from the national GWR SQLite database (`data.sqlite`).

```bash
python extract.py --sqlite data/data.sqlite --canton BE --out bern_buildings.csv
