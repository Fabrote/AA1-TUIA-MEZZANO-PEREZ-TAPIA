import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import json
import os

# Obtener la ruta del directorio actual para buscar los artefactos necesarios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar artefactos previamente generados para preprocesamiento y predicción
city_to_nrm = joblib.load(os.path.join(BASE_DIR, 'city_to_nrm.pkl'))
grouped_medians = joblib.load(os.path.join(BASE_DIR, 'grouped_medians.pkl'))
grouped_modes = joblib.load(os.path.join(BASE_DIR, 'grouped_modes.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))
final_columns = joblib.load(os.path.join(BASE_DIR, 'final_columns.pkl'))

# Definir y cargar el modelo Keras
def build_model(n_features):
    """
    Construye el modelo de Keras con la arquitectura especificada.
    - Dos capas ocultas con activación ReLU.
    - Capa de Dropout para mitigar sobreajuste.
    - Salida sigmoide para clasificación binaria.
    """
    model = Sequential([
        Dense(64, activation='relu', input_shape=(n_features,)),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])
    # En inferencia no es necesario compilar el modelo
    return model

# Construir el modelo y cargar los pesos
n_features = len(final_columns)
model = build_model(n_features)
model_path = os.path.join(BASE_DIR, 'mejor_modelo_keras.h5')
if os.path.exists(model_path):
    model.load_weights(model_path)
else:
    raise FileNotFoundError(f"El archivo del modelo no se encontró en la ruta: {model_path}")


# Función de preprocesamiento
def preprocess_input(data: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica el mismo preprocesamiento que se utilizó durante el entrenamiento.
    Incluye imputación, codificación, transformación cíclica, escalado y alineación de columnas.
    """
    df = data.copy()

    # Mapeo de la región NRM_label según la ciudad
    df['NRM_label'] = df['Location'].map(city_to_nrm)
    if df['NRM_label'].isnull().any():
        raise ValueError("Se encontró una 'Location' no válida o no mapeada.")

    # Imputación de valores atípicos extremos en Evaporation
    df.loc[df['Evaporation'] > 60, 'Evaporation'] = np.nan
    
    # Imputación de columnas numéricas con la mediana de cada región
    numeric_cols = grouped_medians.columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df['NRM_label'].map(grouped_medians[col]))

    # Imputación de columnas categóricas con la moda de cada región
    wind_cols = grouped_modes.columns
    for col in wind_cols:
        df[col] = df[col].fillna(df['NRM_label'].map(grouped_modes[col]))
    
    # Imputar RainToday basado en Rainfall
    df.loc[df["RainToday"].isna() & (df["Rainfall"] >= 1), "RainToday"] = 1
    df.loc[df["RainToday"].isna(), "RainToday"] = 0
    df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0}).astype('Int64')

    # Codificación Cíclica
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

    wind_dir_to_deg = {'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5}
    for col in wind_cols:
        df[f'{col}_sin'] = np.sin(np.deg2rad(df[col].map(wind_dir_to_deg)))
        df[f'{col}_cos'] = np.cos(np.deg2rad(df[col].map(wind_dir_to_deg)))
        
    # One-Hot Encoding para NRM_label
    df = pd.get_dummies(df, columns=['NRM_label'], drop_first=True, dtype=int)

    # Alinear columnas con las del entrenamiento
    for col in final_columns:
        if col not in df.columns:
            df[col] = 0
    
    df_final = df[final_columns].astype('float64')
    
    # Escalar los datos
    scaled_data = scaler.transform(df_final)
    
    return scaled_data

# Función de predicción
def predict(input_json: str) -> dict:
    """
    Realiza una predicción binaria de 'RainTomorrow' a partir de un JSON de entrada.
    Devuelve la probabilidad de lluvia y la clase predicha (Sí/No).
    """
    # Cargar datos de entrada
    input_data = json.loads(input_json)
    input_df = pd.DataFrame([input_data])

    # Preprocesar los datos
    processed_data = preprocess_input(input_df)

    # Realizar la predicción
    probability = model.predict(processed_data)[0][0]
    prediction = 1 if probability >= 0.5 else 0

    # Devolver resultado
    return {
        "probability_rain_tomorrow": float(probability),
        "prediction_rain_tomorrow": "Yes" if prediction == 1 else "No"
    }

# Bloque principal para ejecución desde CLI
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1]:
        # Si se pasa un argumento, se interpreta como el string JSON
        json_input = sys.argv[1]
    else:
        # JSON de ejemplo si no se proporcionan datos
        json_input = '''
        {
            "Date": "2023-01-15",
            "Location": "Albury",
            "MinTemp": 13.4,
            "MaxTemp": 22.9,
            "Rainfall": 0.6,
            "Evaporation": null,
            "Sunshine": null,
            "WindGustDir": "W",
            "WindGustSpeed": 44.0,
            "WindDir9am": "W",
            "WindDir3pm": "WNW",
            "WindSpeed9am": 20.0,
            "WindSpeed3pm": 24.0,
            "Humidity9am": 71.0,
            "Humidity3pm": 22.0,
            "Pressure9am": 1007.7,
            "Pressure3pm": 1007.1,
            "Cloud9am": 8.0,
            "Cloud3pm": null,
            "Temp9am": 16.9,
            "Temp3pm": 21.8,
            "RainToday": "No"
        }
        '''
    
    # Realizar la predicción e imprimir el resultado
    try:
        result = predict(json_input)
        print(json.dumps(result, indent=4))
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)