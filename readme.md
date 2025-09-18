# Bern Solar Panel Analysis

A comprehensive project for analyzing buildings and electricity production plants in the canton of Bern, Switzerland. The project includes data filtering capabilities, interactive mapping, and geospatial visualization features.

## Main Features

### 🔍 Data Filtering

- **`filter-bern-solar.py`**: Filters electricity production plants for the canton of Bern (BE) specifically for solar panels (SubCategory 'subcat_2')
- **`filter_bern_buildings.py`**: Filters all buildings in the canton of Bern from the main dataset

### 🗺️ Interactive Mapping

- **`folium_map.py`**: Creates interactive HTML maps using Folium with:
- Support for Swiss LV95 coordinates (EPSG:2056)
- Automatic conversion to WGS84 coordinates for web visualization
- Detailed informative popups for each point
- Multiple layers (OpenStreetMap, Esri Satellite)
- Interactive layer control

### 📊 Geospatial Visualization

- **`plotmap.py`**: Generates static visualizations on satellite basemaps with:
- Support for scatter and hexbin plots
- Integration with swisstopo data for cantonal boundaries
- High-resolution satellite basemap
- PNG format export

## Data Structure

### Directory `electricity/`

Contains the main electricity production plant datasets:

- `ElectricityProductionPlant.csv`: Main dataset with all plants
- `MainCategoryCatalogue.csv`: Main categories catalog
- `PlantCategoryCatalogue.csv`: Plant categories catalog
- `SubCategoryCatalogue.csv`: Subcategories catalog
- `OrientationCatalogue.csv`: Orientation catalog
- `PlantDetail.csv`: Additional plant details

### Directory `dataset/`

Filtered datasets ready for analysis:

- `BernSolarPanelBuildings.csv`: Buildings with solar panels in the canton of Bern
- `BernBuildings.csv`: All buildings in the canton of Bern

### Directory `data/`

Supplementary data on Bern buildings:

- GeoJSON files for buildings and entrances
- SQLite database with integrated data
- Specifications and documentation in PDF format

### Directory `maps/` and `images/`

- `maps/`: Generated interactive HTML maps
- `images/`: Static PNG visualizations

## Requirements

```bash
pip install pandas pyproj folium geopandas matplotlib contextily owslib
```

## Usage

### Data Filtering

```bash
# Filter solar panels in the canton of Bern
python filter-bern-solar.py

# Filter all buildings in the canton of Bern
python filter_bern_buildings.py
```

### Creating Interactive Maps

```bash
# Base map with default dataset
python folium_map.py

# Custom map
python folium_map.py --csv dataset/BernSolarPanelBuildings.csv --out maps/custom_map.html --limit 1000
```

### Static Visualizations

```bash
# Hexbin plot of solar panels
python plotmap.py --csv dataset/BernSolarPanelBuildings.csv --x _x --y _y --out bern_hexbin.png --kind hexbin --gridsize 120

# Scatter plot of buildings
python plotmap.py --csv dataset/BernBuildings.csv --x east_lv95 --y north_lv95 --out bern_scatter.png --kind scatter --s 0.5
```

## Coordinate Systems

The project primarily uses the Swiss coordinate system:

- **LV95 (EPSG:2056)**: Official Swiss coordinate system for input data
- **WGS84 (EPSG:4326)**: Automatic conversion for web visualization
- **Web Mercator (EPSG:3857)**: For satellite basemaps

## Output

- **Interactive HTML maps**: Web-ready visualization with layer controls
- **PNG images**: High-resolution static visualizations
- **CSV datasets**: Filtered data ready for further analysis

## Technical Notes

- Automatic handling of coordinate columns with different naming formats
- Support for data sampling for large datasets
- Integration with swisstopo WFS services for administrative boundaries
- Dynamic informative popups with all available dataset fields