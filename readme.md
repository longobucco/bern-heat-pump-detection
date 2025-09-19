# Bern Solar Panel Detection

Un progetto di computer vision per il rilevamento automatico di pannelli solari attraverso l'analisi di ortofoto aeree nel cantone di Berna, Svizzera. Il sistema utilizza dati open data di swisstopo e opendata.swiss per creare un dataset bilanciato di immagini aeree ad alta risoluzione per l'addestramento di modelli di machine learning.

## Problema

Identificare automaticamente gli edifici dotati di pannelli solari attraverso l'analisi di fotografie aeree ad alta risoluzione (ortofoto).

## Processo di Sviluppo

1. **Estrazione Dati**: Ottenimento dei dati da opendata.swiss sui pannelli solari e edifici nel cantone di Berna
2. **Estrazione Coordinate**: Matching spaziale tra edifici con pannelli solari e coordinate geografiche
3. **Acquisizione Ortofoto**: Download automatico di ortofoto ad alta risoluzione da swisstopo WMS
4. **Creazione Dataset**: Costruzione di un dataset bilanciato con rapporto ~1:3 tra esempi positivi e negativi

## Pipeline del Progetto

### 🏗️ Preprocessing dei Dati

- **`sample.py`**: Campionamento casuale di 24.000 edifici dal dataset completo del cantone di Berna
- **`match.py`**: Matching spaziale tra edifici con pannelli solari e coordinate geografiche per identificare esempi positivi
- **`orthophoto.py`**: Download di ortofoto per edifici con pannelli solari (esempi positivi)
- **`original-orthophoto.py`**: Download di ortofoto per edifici casuali (esempi negativi/non etichettati)

### 🖼️ Acquisizione Immagini

- **Risoluzione**: Immagini disponibili in due formati (125x125px e 256x256px)
- **Risoluzione spaziale**: 20 cm per pixel
- **Fonte**: Servizio WMS swisstopo (ch.swisstopo.swissimage-product)
- **Sistema di coordinate**: LV95 (EPSG:2056)

### 🗺️ Visualizzazione e Analisi

- **`folium_map.py`**: Creazione di mappe interattive HTML con:
  - Supporto per coordinate Swiss LV95 (EPSG:2056)
  - Conversione automatica a WGS84 per visualizzazione web
  - Popup informativi dettagliati
  - Layer multipli (OpenStreetMap, Esri Satellite)

- **`plotmap.py`**: Visualizzazioni statiche su basemap satellitari:
  - Plot scatter e hexbin
  - Integrazione con dati swisstopo per confini cantonali
  - Esportazione in formato PNG ad alta risoluzione

## Struttura del Dataset

### Dataset Immagini

Il progetto genera quattro directory di immagini per il training di modelli di computer vision:

#### Esempi Positivi (Edifici con Pannelli Solari)
- **`true-orthophoto-125px/`**: 8.346 immagini 125x125px di edifici con pannelli solari
- **`true-orthophoto-256px/`**: 8.346 immagini 256x256px di edifici con pannelli solari

#### Esempi Negativi/Non Etichettati
- **`unlabeled-orthophoto-125px/`**: 23.995 immagini 125x125px di edifici casuali
- **`unlabeled-orthophoto-256px/`**: 19.583 immagini 256x256px di edifici casuali

**Rapporto del Dataset**: ~1:3 (positivi:negativi), bilanciamento ottimale per training di modelli di classificazione

### Dataset CSV

#### Directory `dataset/`

- **`BernSolarPanelBuildings.csv`**: 37.099 edifici con pannelli solari nel cantone di Berna
  - Include coordinate LV95, indirizzo, potenza installata, data di messa in funzione
- **`buildings_BE.csv`**: 477.847 edifici totali nel cantone di Berna
- **`building_sample_BE.csv`**: 24.000 edifici campionati casualmente per esempi negativi
- **`buildings_BE_matches_xy.csv`**: 8.347 coordinate di edifici con pannelli solari estratte per il download delle ortofoto

## Caratteristiche Tecniche

### Coordinate e Proiezioni
- **Input**: Swiss LV95 (EPSG:2056) - sistema di coordinate ufficiale svizzero
- **Output web**: WGS84 (EPSG:4326) - conversione automatica per visualizzazione
- **Basemap**: Web Mercator (EPSG:3857) - per integrazione con mappe satellitari

### Parametri Ortofoto
- **Risoluzione spaziale**: 20 cm/pixel
- **Dimensioni immagine**: 125x125px (25m x 25m) o 256x256px (51.2m x 51.2m)
- **Formato**: PNG ad alta qualità
- **Copertura**: Area di 12.5m di raggio dal centroide dell'edificio

### API e Servizi
- **Fonte dati**: opendata.swiss per dati energia e edifici
- **Ortofoto**: swisstopo WMS (ch.swisstopo.swissimage-product)
- **Confini amministrativi**: swisstopo WFS per confini cantonali

## Utilizzo

### Preparazione del Dataset

```bash
# 1. Campionamento di edifici casuali
python sample.py

# 2. Estrazione coordinate edifici con pannelli solari
python match.py

# 3. Download ortofoto edifici con pannelli (esempi positivi)
python orthophoto.py

# 4. Download ortofoto edifici casuali (esempi negativi)
python original-orthophoto.py
```

### Generazione delle Visualizzazioni

```bash
# Mappa interattiva di tutti gli edifici con pannelli solari
python folium_map.py --csv dataset/BernSolarPanelBuildings.csv --out maps/solar_buildings.html

# Visualizzazione hexbin della densità di pannelli solari
python plotmap.py --csv dataset/BernSolarPanelBuildings.csv --x _x --y _y --out images/solar_hexbin.png --kind hexbin --gridsize 120

# Scatter plot di tutti gli edifici
python plotmap.py --csv dataset/buildings_BE.csv --x GKODE --y GKODN --out images/buildings_scatter.png --kind scatter --s 0.5
```

## Requisiti

```bash
pip install pandas pyproj folium geopandas matplotlib contextily owslib requests
```

## Applicazioni Potenziali

### Machine Learning
- **Classificazione binaria**: Rilevamento presenza/assenza pannelli solari
- **Object detection**: Localizzazione precisa dei pannelli nelle immagini
- **Semantic segmentation**: Segmentazione pixel-level dei pannelli solari
- **Transfer learning**: Fine-tuning di modelli pre-addestrati (ResNet, EfficientNet, etc.)

### Analisi Geospaziale
- **Mapping**: Identificazione automatica di nuove installazioni solari
- **Trend analysis**: Monitoraggio dell'espansione del fotovoltaico nel tempo
- **Urban planning**: Supporto alla pianificazione energetica territoriale
- **Policy making**: Analisi dell'efficacia delle politiche di incentivazione

### Computer Vision Research
- **Benchmark dataset**: Dataset standardizzato per confronto di algoritmi
- **Domain adaptation**: Trasferimento a altre regioni geografiche
- **Multi-temporal analysis**: Rilevamento di cambiamenti nel tempo
- **Multi-scale analysis**: Confronto prestazioni a diverse risoluzioni

## Note Tecniche

- **Gestione memoria**: Download progressivo per dataset di grandi dimensioni
- **Error handling**: Gestione automatica di fallimenti di download WMS
- **Coordinate handling**: Supporto automatico per diversi formati di colonne coordinate
- **Scalabilità**: Pipeline ottimizzata per dataset di centinaia di migliaia di edifici
- **Qualità**: Controllo qualità automatico delle immagini scaricate
- **Reproducibilità**: Seed fisso per campionamento deterministico

## Struttura Directory

```
bern-solar-panel-detection/
├── dataset/                          # Dataset CSV processati
│   ├── BernSolarPanelBuildings.csv   # 37.099 edifici con pannelli
│   ├── buildings_BE.csv              # 477.847 edifici totali BE
│   ├── building_sample_BE.csv        # 24.000 edifici campionati
│   └── buildings_BE_matches_xy.csv   # 8.347 coordinate estratte
├── true-orthophoto-125px/            # 8.346 immagini positive 125px
├── true-orthophoto-256px/            # 8.346 immagini positive 256px
├── unlabeled-orthophoto-125px/       # 23.995 immagini negative 125px
├── unlabeled-orthophoto-256px/       # 19.583 immagini negative 256px
├── maps/                             # Mappe HTML interattive
├── images/                           # Visualizzazioni statiche PNG
└── *.py                             # Script di preprocessing e visualizzazione
```

## Licenza e Attribuzioni

- **Dati**: opendata.swiss (Open Government Data)
- **Ortofoto**: © swisstopo
- **Confini amministrativi**: © swisstopo
- **Codice**: Sviluppato per ricerca accademica in computer vision e energy analytics