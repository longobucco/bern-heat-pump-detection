# Bern Solar Panel Detection

A computer vision project for automatic solar panel detection through analysis of aerial orthophotos in the Canton of Bern, Switzerland. The system uses open data from swisstopo and opendata.swiss to create a balanced dataset of high-resolution aerial images for machine learning model training.

## Problem

Automatically identify buildings equipped with solar panels through analysis of high-resolution aerial photographs (orthophotos).

## Development Process

1. **Data Extraction**: Obtaining data from opendata.swiss on solar panels and buildings in the Canton of Bern
2. **Coordinate Extraction**: Spatial matching between buildings with solar panels and geographic coordinates
3. **Orthophoto Acquisition**: Automatic download of high-resolution orthophotos from swisstopo WMS
4. **Dataset Creation**: Construction of a balanced dataset with ~1:3 ratio between positive and negative examples

## Project Pipeline

### 🏗️ Data Preprocessing

- **`sample.py`**: Random sampling of 24,000 buildings from the complete Canton of Bern dataset
- **`match.py`**: Spatial matching between buildings with solar panels and geographic coordinates to identify positive examples
- **`orthophoto.py`**: Download orthophotos for buildings with solar panels (positive examples)
- **`original-orthophoto.py`**: Download orthophotos for random buildings (negative/unlabeled examples)

### 🖼️ Image Acquisition

- **Resolution**: Images available in two formats (125x125px and 256x256px)
- **Spatial resolution**: 20 cm per pixel
- **Source**: swisstopo WMS service (ch.swisstopo.swissimage-product)
- **Coordinate system**: LV95 (EPSG:2056)

### 🗺️ Visualization and Analysis

- **`folium_map.py`**: Creation of interactive HTML maps with:

  - Support for Swiss LV95 coordinates (EPSG:2056)
  - Automatic conversion to WGS84 for web visualization
  - Detailed informative popups
  - Multiple layers (OpenStreetMap, Esri Satellite)

- **`plotmap.py`**: Static visualizations on satellite basemaps:
  - Scatter and hexbin plots
  - Integration with swisstopo data for cantonal boundaries
  - Export in high-resolution PNG format

## Dataset Structure

### Image Dataset

The project generates four image directories for computer vision model training:

#### Positive Examples (Buildings with Solar Panels)

- **`true-orthophoto-125px/`**: 8,346 images 125x125px of buildings with solar panels
- **`true-orthophoto-256px/`**: 8,346 images 256x256px of buildings with solar panels

#### Negative/Unlabeled Examples

- **`unlabeled-orthophoto-125px/`**: 23,995 images 125x125px of random buildings
- **`unlabeled-orthophoto-256px/`**: 19,583 images 256x256px of random buildings

**Dataset Ratio**: ~1:3 (positive:negative), optimal balancing for classification model training

### CSV Dataset

#### `dataset/` Directory

- **`BernSolarPanelBuildings.csv`**: 37,099 buildings with solar panels in the Canton of Bern
  - Includes LV95 coordinates, address, installed power, commissioning date
- **`buildings_BE.csv`**: 477,847 total buildings in the Canton of Bern
- **`building_sample_BE.csv`**: 24,000 randomly sampled buildings for negative examples
- **`buildings_BE_matches_xy.csv`**: 8,347 coordinates of buildings with solar panels extracted for orthophoto download

## Technical Characteristics

### Coordinates and Projections

- **Input**: Swiss LV95 (EPSG:2056) - official Swiss coordinate system
- **Web output**: WGS84 (EPSG:4326) - automatic conversion for visualization
- **Basemap**: Web Mercator (EPSG:3857) - for integration with satellite maps

### Orthophoto Parameters

- **Spatial resolution**: 20 cm/pixel
- **Image dimensions**: 125x125px (25m x 25m) or 256x256px (51.2m x 51.2m)
- **Format**: High-quality PNG
- **Coverage**: 12.5m radius area from building centroid

### APIs and Services

- **Data source**: opendata.swiss for energy and building data
- **Orthophotos**: swisstopo WMS (ch.swisstopo.swissimage-product)
- **Administrative boundaries**: swisstopo WFS for cantonal boundaries

## Usage

### YOLO Model Training

The project uses YOLO (You Only Look Once) for automatic solar panel detection. The dataset is already prepared and organized in the appropriate directories.

```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Start YOLO model training
python yolo.py
```

The `yolo.py` file performs training over 5 epochs using:

- **Base model**: Pre-trained YOLOv8n (nano)
- **Training dataset**: 256x256px images of buildings with solar panels
- **Validation dataset**: 256x256px images of random buildings
- **Configuration**: Defined in `data.yaml`

### Training Configuration

The `data.yaml` file contains the dataset configuration:

```yaml
train: /path/to/true-orthophoto-256px # Positive examples
val: /path/to/unlabeled-orthophoto-256px # Negative examples
nc: 2 # Number of classes
names: ["solar-panel", "no-solar-panel"] # Class names
```

### Training Results

Training results are automatically saved in:

- **`runs/detect/train/`**: Metrics, charts and model weights
- **`runs/detect/train/weights/best.pt`**: Best trained model
- **`runs/detect/train/weights/last.pt`**: Last checkpoint

### Visualization Generation

```bash
# Interactive map of all buildings with solar panels
python folium_map.py --csv dataset/BernSolarPanelBuildings.csv --out maps/solar_buildings.html

# Hexbin visualization of solar panel density
python plotmap.py --csv dataset/BernSolarPanelBuildings.csv --x _x --y _y --out images/solar_hexbin.png --kind hexbin --gridsize 120

# Scatter plot of all buildings
python plotmap.py --csv dataset/buildings_BE.csv --x GKODE --y GKODN --out images/buildings_scatter.png --kind scatter --s 0.5
```

## Requirements

The project requires few essential dependencies for YOLO training:

```bash
pip install -r requirements.txt
```

**Main dependencies:**

- `ultralytics>=8.0.0` - YOLO framework for object detection
- `pandas>=2.0.0` - CSV data manipulation
- `numpy>=1.24.0` - Basic numerical operations
- `jupyter>=1.0.0` - Optional, for interactive experimentation

**Notes:**

- Ultralytics automatically installs PyTorch, torchvision and other necessary dependencies
- Geospatial libraries are no longer needed for training only
- For GPU support, make sure you have CUDA installed and compatible

## Potential Applications

### Object Detection with YOLO

- **Automatic detection**: Identification and precise localization of solar panels in orthophotos
- **Real-time inference**: Ability to process new images in real-time for continuous mapping
- **Bounding box detection**: Precise panel coordinates for quantitative analysis
- **Confidence scoring**: Model certainty assessment for each detection
- **Multi-scale detection**: Ability to detect panels of different sizes in the same image

### Deployment and Inference

- **Batch processing**: Automatic processing of large orthophoto datasets
- **Web API**: Integration into web systems for image upload and analysis
- **Mobile deployment**: Optimization for mobile devices with YOLO nano
- **Edge computing**: Deployment on IoT devices for distributed analysis
- **Cloud integration**: Scalability on cloud infrastructures for massive processing

### Geospatial Analysis

- **Mapping**: Automatic identification of new solar installations
- **Trend analysis**: Monitoring photovoltaic expansion over time
- **Urban planning**: Support for territorial energy planning
- **Policy making**: Analysis of incentive policy effectiveness

### Computer Vision Research

- **Benchmark dataset**: Standardized dataset for algorithm comparison
- **Domain adaptation**: Transfer to other geographical regions
- **Multi-temporal analysis**: Detection of changes over time
- **Multi-scale analysis**: Performance comparison at different resolutions

## Technical Notes

- **Memory management**: Progressive download for large datasets
- **Error handling**: Automatic handling of WMS download failures
- **Coordinate handling**: Automatic support for different coordinate column formats
- **Scalability**: Pipeline optimized for datasets of hundreds of thousands of buildings
- **Quality**: Automatic quality control of downloaded images
- **Reproducibility**: Fixed seed for deterministic sampling

## Directory Structure

```
bern-solar-panel-detection/
├── dataset/                          # Processed CSV datasets
│   ├── BernSolarPanelBuildings.csv   # 37,099 buildings with panels
│   ├── buildings_BE.csv              # 477,847 total BE buildings
│   ├── building_sample_BE.csv        # 24,000 sampled buildings
│   └── buildings_BE_matches_xy.csv   # 8,347 extracted coordinates
├── true-orthophoto-125px/            # 8,346 positive images 125px
├── true-orthophoto-256px/            # 8,346 positive images 256px
├── unlabeled-orthophoto-125px/       # 23,995 negative images 125px
├── unlabeled-orthophoto-256px/       # 19,583 negative images 256px
├── maps/                             # Interactive HTML maps
├── images/                           # Static PNG visualizations
└── *.py                             # Preprocessing and visualization scripts
```

## License and Attributions

- **Data**: opendata.swiss (Open Government Data)
- **Orthophotos**: © swisstopo
- **Administrative boundaries**: © swisstopo
- **Code**: Developed for academic research in computer vision and energy analytics
