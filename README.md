# AA1-TUIA-MEZZANO-PEREZ-TAPIA
# TP2 - Clasificación de Lluvia en Australia

# Proyecto de Predicción de Lluvia en Australia

## Descripción
Este proyecto contiene un modelo de aprendizaje automático para predecir si lloverá al día siguiente en varias ciudades de Australia. El proceso completo, desde el análisis de datos hasta la puesta en producción a través de Docker, se documenta a continuación.


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


## Tabla de Contenidos
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Paso a Paso para la Ejecución](#paso-a-paso-para-la-ejecución)
3. [Detalles del Notebook de Análisis (`TP-clasificacion-AA1.ipynb`)](#detalles-del-notebook-de-análisis)
4. [Detalles del Script de Inferencia (`inferencia.py`)](#detalles-del-script-de-inferencia)

---

## Estructura del Proyecto

```
.
├── docker/                     # Contiene todo lo necesario para la inferencia en Docker
│   ├── inferencia.py           # Script que carga el modelo y realiza predicciones
│   ├── requirements.txt        # Librerías para el entorno de Docker
│   ├── Dockerfile              # Define la imagen de Docker
│   ├── city_to_nrm.pkl         # Mapeo de ciudad a región climática
│   ├── final_columns.pkl       # Lista de columnas finales para el modelo
│   ├── grouped_medians.pkl     # Medianas para imputación numérica
│   ├── grouped_modes.pkl       # Modas para imputación categórica
│   └── scaler.pkl              # Objeto StandardScaler ajustado
│
├── TP-clasificacion-AA1.ipynb  # Notebook con el análisis exploratorio y entrenamiento de modelos
├── save_preprocessing_objects.py # Script para generar los artefactos de preprocesamiento y el modelo
├── mejor_modelo_keras.h5       # El modelo de red neuronal entrenado
├── weatherAUS.csv              # El dataset original
└── README.md                   # Este archivo
```

---

### Ejecución con Docker

Ejecutar el archivo python "save_preprossecing_objects.py" para guardar los artefactos y el modelo.
Luego continuar con el paso a paso descrito en el archivo readme.md localizado dentro de la carpeta docker para la correcta ejecución. 

## Detalles del Notebook de Análisis

El archivo `TP-clasificacion-AA1.ipynb` contiene todo el proceso de investigación y desarrollo:
- **Carga y Exploración de Datos (EDA):** Análisis inicial, estadísticas descriptivas y visualizaciones.
- **Clustering Geoespacial:** Se exploran 3 formas de agrupar las ciudades: KMeans, por Estado y por Regiones NRM (Natural Resource Management), concluyendo que NRM es la más adecuada para imputar datos faltantes por similitud climática.
- **Preprocesamiento:** Limpieza de datos, imputación de valores nulos usando las medianas/modas por región NRM, y creación de nuevas características (codificación cíclica para variables de viento y mes).
- **Entrenamiento de Modelos:** Se entrenan y evalúan varios modelos, siendo la Red Neuronal con TensorFlow/Keras la seleccionada como final.

## Detalles del Script de Inferencia

El script `docker/inferencia.py` está diseñado para ser ejecutado en un entorno donde el modelo y los artefactos de preprocesamiento están disponibles.
- Recibe los datos de entrada como una cadena JSON desde la línea de comandos.
- Carga todos los artefactos (`.pkl`).
- Aplica exactamente los mismos pasos de preprocesamiento que se aplicaron a los datos de entrenamiento (imputación, codificación cíclica, one-hot encoding, etc.).
- Escala los datos con el `scaler.pkl` guardado.
- Carga el modelo `mejor_modelo_keras.h5` y realiza la predicción.
- Devuelve el resultado como una salida JSON.

## Integrantes

- Florencia Mezzano
- Fabrizio Tapia
- Sebastián Perez


