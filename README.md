# AA1-TUIA-MEZZANO-PEREZ-TAPIA
# TP2 - Clasificación de Lluvia en Australia

## Descripción
Proyecto de Machine Learning para predecir si lloverá al día siguiente en ciudades de Australia usando datos meteorológicos históricos.

## Dataset
- **Archivo**: `weatherAUS.csv`
- **Registros**: 145.460 observaciones
- **Período**: 2007-2017
- **Ciudades**: 49 ubicaciones en Australia
- **Variable objetivo**: `RainTomorrow` (Sí/No)

## Contenido del Proyecto

### Notebook Principal
- `TP-clasificacion-AA1.ipynb`: Análisis completo incluyendo:
  - Clustering geográfico (KMeans, Estados, Regiones NRM)
  - Análisis exploratorio de datos (EDA)
  - Preprocesamiento e imputación de valores faltantes y outliers
  - Codificación de variables categóricas
  - Entrenamiento de modelos de clasificación

### Archivos Adicionales
- `weatherAUS.csv`: Dataset principal
- `NRM_clusters.shp`: Shapefile de regiones NRM de Australia
- `clusters_kmeans.html`: Mapa Interactivo de ciudades, clustering por KMeans 
- `clusters_NRM_regions.html`: Mapa Interactivo de ciudades, clustering por NRM_regions 
- `clusters_states.html`: Mapa Interactivo de ciudades, clustering por estados 


## Características Principales
- **18 variables numéricas**: temperaturas, precipitación, viento, humedad, presión, nubes
- **7 variables categóricas**: ubicación, direcciones del viento, lluvia
- **Preprocesamiento completo**: imputación de valores faltantes, codificación cíclica para direcciones de viento

## Integrantes
- Florencia Mezzano
- Fabrizio Tapia
- Sebastián Perez