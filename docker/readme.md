# Proyecto de Inferencia de Lluvia en Australia con Docker

Este directorio contiene los archivos necesarios para construir y ejecutar un contenedor de Docker que realiza predicciones sobre la probabilidad de lluvia en Australia al día siguiente.

## Contenido de este directorio (`docker/`)

- `inferencia.py` — Script principal de predicción.
- `city_to_nrm.pkl` — Mapeo de ciudades a regiones NRM.
- `grouped_medians.pkl` — Medianas por región para imputación numérica.
- `grouped_modes.pkl` — Modas por región para imputación categórica.
- `scaler.pkl` — Scaler entrenado.
- `final_columns.pkl` — Orden y estructura final de columnas.
- `Dockerfile` — Instrucciones para construir la imagen.
- `requirements.txt` — Librerías necesarias para inferencia.

## Requisitos

- Docker instalado en su sistema.
- El archivo `mejor_modelo_keras.h5` debe estar presente en el directorio raíz del proyecto (un nivel por encima de esta carpeta `docker`). Esto se hace ejecutando el archivo save_preprocessing_objects.py. 

## Construcción de la Imagen de Docker

1.  **Abra una terminal** en el directorio raíz de este proyecto (es decir, en `TP 2 - Clasificacion`).

2.  **Ejecutar el siguiente comando** para construir la imagen de Docker. La opción `-t` le asigna un nombre (tag) a la imagen para que sea fácil de referenciar.

    ```bash
    docker build -t lluvia-predictor -f docker/Dockerfile .
    ```

    **Explicación del comando:**
    - `docker build`: El comando para construir una imagen.
    - `-t lluvia-predictor`: Asigna el nombre `lluvia-predictor` a la imagen.
    - `-f docker/Dockerfile`: Especifica la ruta al `Dockerfile`.
    - `.`: Indica que el contexto de construcción es el directorio actual (el raíz del proyecto), lo cual es crucial para que Docker pueda acceder tanto a la carpeta `docker` como al archivo `mejor_modelo_keras.h5`.

## Ejecución del Contenedor

Para ejecutar el contenedor y realizar una predicción, debe pasar un string JSON como argumento al comando `docker run`.

1.  **Prepar JSON de entrada.** Debe ser un objeto JSON válido en una sola línea. Aquí hay un ejemplo:

    ```json
    { "Date": "2023-01-15", "Location": "Albury", "MinTemp": 13.4, "MaxTemp": 22.9, "Rainfall": 0.6, "Evaporation": null, "Sunshine": null, "WindGustDir": "W", "WindGustSpeed": 44.0, "WindDir9am": "W", "WindDir3pm": "WNW", "WindSpeed9am": 20.0, "WindSpeed3pm": 24.0, "Humidity9am": 71.0, "Humidity3pm": 22.0, "Pressure9am": 1007.7, "Pressure3pm": 1007.1, "Cloud9am": 8.0, "Cloud3pm": null, "Temp9am": 16.9, "Temp3pm": 21.8, "RainToday": "No" }
    ```

2.  **Ejecutar el contenedor** con el JSON como argumento. Asegúrese de escapar las comillas dobles correctamente según su sistema operativo.

    **En PowerShell (Windows):**

    ```powershell
    docker run --rm lluvia-predictor '{ "Date": "2023-01-15", "Location": "Albury", "MinTemp": 13.4, "MaxTemp": 22.9, "Rainfall": 0.6, "Evaporation": null, "Sunshine": null, "WindGustDir": "W", "WindGustSpeed": 44.0, "WindDir9am": "W", "WindDir3pm": "WNW", "WindSpeed9am": 20.0, "WindSpeed3pm": 24.0, "Humidity9am": 71.0, "Humidity3pm": 22.0, "Pressure9am": 1007.7, "Pressure3pm": 1007.1, "Cloud9am": 8.0, "Cloud3pm": null, "Temp9am": 16.9, "Temp3pm": 21.8, "RainToday": "No" }'
    ```

    **En Bash (Linux/macOS/Git Bash en Windows):**

    ```bash
    docker run --rm lluvia-predictor '{ "Date": "2023-01-15", "Location": "Albury", "MinTemp": 13.4, "MaxTemp": 22.9, "Rainfall": 0.6, "Evaporation": null, "Sunshine": null, "WindGustDir": "W", "WindGustSpeed": 44.0, "WindDir9am": "W", "WindDir3pm": "WNW", "WindSpeed9am": 20.0, "WindSpeed3pm": 24.0, "Humidity9am": 71.0, "Humidity3pm": 22.0, "Pressure9am": 1007.7, "Pressure3pm": 1007.1, "Cloud9am": 8.0, "Cloud3pm": null, "Temp9am": 16.9, "Temp3pm": 21.8, "RainToday": "No" }'
    ```

3.  **El resultado** será un JSON con la probabilidad y la predicción final, por ejemplo:

    ```json
    {
        "probability_rain_tomorrow": 0.123456789,
        "prediction_rain_tomorrow": "No"
    }
    ```

### Ejecución con el JSON de ejemplo por defecto

Si ejecuta el contenedor sin argumentos, el script `inferencia.py` usará un JSON de ejemplo interno:

```bash
docker run --rm lluvia-predictor
```