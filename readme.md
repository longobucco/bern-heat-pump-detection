# Bern Solar Panel Analysis

A comprehensive project for analyzing buildings and solar panel installations in the canton of Bern, Switzerland. The project includes data filtering capabilities, interactive mapping, and geospatial visualization features for understanding the distribution and characteristics of solar energy infrastructure.

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

### Core Datasets

The project works with three main datasets:

1. **All Buildings in Bern**: Complete dataset of all buildings in the canton of Bern
2. **Buildings with Solar Panels**: Specific subset of buildings that have solar panel installations
3. **Geo-Coordinate Matching Dataset**: Provides coordinate matching and spatial relationships between the building and solar panel datasets

### Directory `electricity/`

Contains the original electricity production plant datasets:

- `ElectricityProductionPlant.csv`: Main dataset with all plants
- `MainCategoryCatalogue.csv`: Main categories catalog
- `PlantCategoryCatalogue.csv`: Plant categories catalog
- `SubCategoryCatalogue.csv`: Subcategories catalog
- `OrientationCatalogue.csv`: Orientation catalog
- `PlantDetail.csv`: Additional plant details

### Directory `dataset/`

Filtered and processed datasets ready for analysis:

- `BernSolarPanelBuildings.csv`: Buildings with solar panels in the canton of Bern
- `BernBuildings.csv`: All buildings in the canton of Bern
- Geo-coordinate matching files for spatial analysis

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

# Map of all buildings
python folium_map.py --csv dataset/BernBuildings.csv --out maps/all_buildings.html --limit 5000

# Map of solar panel buildings
python folium_map.py --csv dataset/BernSolarPanelBuildings.csv --out maps/solar_buildings.html --limit 1000
```

### Static Visualizations

```bash
# Hexbin plot of solar panel buildings
python plotmap.py --csv dataset/BernSolarPanelBuildings.csv --x _x --y _y --out solar_hexbin.png --kind hexbin --gridsize 120

# Scatter plot of all buildings
python plotmap.py --csv dataset/BernBuildings.csv --x east_lv95 --y north_lv95 --out buildings_scatter.png --kind scatter --s 0.5
```

## Data Analysis Capabilities

The project enables comprehensive analysis of:

- **Building Distribution**: Spatial patterns of all buildings across Bern canton
- **Solar Panel Adoption**: Geographic distribution and density of solar installations
- **Spatial Relationships**: Correlation between building characteristics and solar panel presence
- **Coordinate Matching**: Precise geographic alignment between building and energy datasets

## Coordinate Systems

The project primarily uses the Swiss coordinate system:

- **LV95 (EPSG:2056)**: Official Swiss coordinate system for input data
- **WGS84 (EPSG:4326)**: Automatic conversion for web visualization
- **Web Mercator (EPSG:3857)**: For satellite basemaps

## Output

- **Interactive HTML maps**: Web-ready visualization with layer controls for building and solar data
- **PNG images**: High-resolution static visualizations comparing building vs. solar distributions
- **CSV datasets**: Filtered data with coordinate matching for spatial analysis
- **Comparative visualizations**: Side-by-side analysis of building density vs. solar adoption

## Technical Notes

- Automatic handling of coordinate columns with different naming formats
- Support for data sampling for large datasets
- Integration with swisstopo WFS services for administrative boundaries
- Dynamic informative popups with all available dataset fields
- Coordinate matching capabilities for spatial relationship analysis
- Optimized visualization for datasets of varying sizes (all buildings vs. solar-specific)# Bern Solar Panel Analysis

A comprehensive project for analyzing buildings and solar panel installations in the canton of Bern, Switzerland. The project includes data filtering capabilities, interactive mapping, and geospatial visualization features for understanding the distribution and characteristics of solar energy infrastructure.

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

### Core Datasets

The project works with three main datasets:

1. **All Buildings in Bern**: Complete dataset of all buildings in the canton of Bern
2. **Buildings with Solar Panels**: Specific subset of buildings that have solar panel installations
3. **Geo-Coordinate Matching Dataset**: Provides coordinate matching and spatial relationships between the building and solar panel datasets

### Directory `electricity/`

Contains the original electricity production plant datasets:

- `ElectricityProductionPlant.csv`: Main dataset with all plants
- `MainCategoryCatalogue.csv`: Main categories catalog
- `PlantCategoryCatalogue.csv`: Plant categories catalog
- `SubCategoryCatalogue.csv`: Subcategories catalog
- `OrientationCatalogue.csv`: Orientation catalog
- `PlantDetail.csv`: Additional plant details

### Directory `dataset/`

Filtered and processed datasets ready for analysis:

- `BernSolarPanelBuildings.csv`: Buildings with solar panels in the canton of Bern
- `BernBuildings.csv`: All buildings in the canton of Bern
- Geo-coordinate matching files for spatial analysis

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

# Map of all buildings
python folium_map.py --csv dataset/BernBuildings.csv --out maps/all_buildings.html --limit 5000

# Map of solar panel buildings
python folium_map.py --csv dataset/BernSolarPanelBuildings.csv --out maps/solar_buildings.html --limit 1000
```

### Static Visualizations

```bash
# Hexbin plot of solar panel buildings
python plotmap.py --csv dataset/BernSolarPanelBuildings.csv --x _x --y _y --out solar_hexbin.png --kind hexbin --gridsize 120

# Scatter plot of all buildings
python plotmap.py --csv dataset/BernBuildings.csv --x east_lv95 --y north_lv95 --out buildings_scatter.png --kind scatter --s 0.5
```

## Data Analysis Capabilities

The project enables comprehensive analysis of:

- **Building Distribution**: Spatial patterns of all buildings across Bern canton
- **Solar Panel Adoption**: Geographic distribution and density of solar installations
- **Spatial Relationships**: Correlation between building characteristics and solar panel presence
- **Coordinate Matching**: Precise geographic alignment between building and energy datasets

## Coordinate Systems

The project primarily uses the Swiss coordinate system:

- **LV95 (EPSG:2056)**: Official Swiss coordinate system for input data
- **WGS84 (EPSG:4326)**: Automatic conversion for web visualization
- **Web Mercator (EPSG:3857)**: For satellite basemaps

## Output

- **Interactive HTML maps**: Web-ready visualization with layer controls for building and solar data
- **PNG images**: High-resolution static visualizations comparing building vs. solar distributions
- **CSV datasets**: Filtered data with coordinate matching for spatial analysis
- **Comparative visualizations**: Side-by-side analysis of building density vs. solar adoption

## Technical Notes

- Automatic handling of coordinate columns with different naming formats
- Support for data sampling for large datasets
- Integration with swisstopo WFS services for administrative boundaries
- Dynamic informative popups with all available dataset fields
- Coordinate matching capabilities for spatial relationship analysis
- Optimized visualization for datasets of varying sizes (all buildings vs. solar-specific)