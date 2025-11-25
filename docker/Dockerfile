# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema si fueran necesarias
# Por ahora no se necesitan, pero se deja como ejemplo
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copiar el archivo de requerimientos e instalar las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los artefactos de preprocesamiento y el script de inferencia
# Esto copia todo lo que está en la carpeta 'docker' del host a /app en el contenedor
COPY . .

# Copiar el modelo de Keras desde el directorio raíz del proyecto al directorio de trabajo del contenedor
COPY ../mejor_modelo_keras.h5 .

# Establecer el comando por defecto para ejecutar el script de inferencia
# Esto permite pasar el JSON como un argumento de línea de comandos a `docker run`
ENTRYPOINT ["python", "inferencia.py"]
CMD [""]