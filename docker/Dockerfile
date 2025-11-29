# Imagen base minimalista con Python 3.11.
# Usamos "slim" porque reduce el tamaño final del contenedor
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema si fueran necesarias
# Por ahora no se necesitan, pero queda el bloque documentado como ejemplo
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copiar el archivo de requerimientos e instalar las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los artefactos de preprocesamiento y el script de inferencia
# Esto copia todo lo que está en la carpeta 'docker' del host a /app en el contenedor
# Copiamos la carpeta completa (artefactos + inferencia.py)
# Esto incluye:
# - inferencia.py
# - city_to_nrm.pkl
# - grouped_medians.pkl
# - grouped_modes.pkl
# - scaler.pkl
# - final_columns.pkl
COPY . .

# Copiar el modelo de Keras desde el directorio raíz del proyecto al directorio de trabajo del contenedor
COPY ../mejor_modelo_keras.h5 .

# Establecer el comando por defecto para ejecutar el script de inferencia
# Esto permite pasar el JSON como un argumento de línea de comandos a `docker run`
ENTRYPOINT ["python", "inferencia.py"]
CMD [""]