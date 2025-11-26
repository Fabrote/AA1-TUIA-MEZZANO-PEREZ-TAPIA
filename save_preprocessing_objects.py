import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

print("Iniciando el guardado de artefactos de preprocesamiento (versión corregida)...")

# --- 1. Directorio de salida ---
output_dir = 'docker'
os.makedirs(output_dir, exist_ok=True)
print(f"Directorio '{output_dir}' asegurado.")

# --- 2. Carga y preparación inicial de datos (replicando el notebook) ---
df = pd.read_csv(r'C:\\Users\\Usuario\\OneDrive\\Documentos\\TUIA\\4to Cuatri\\AA1\\TP2-Clasificación\\weatherAUS.csv')

# Mapeo pre-calculado de Ciudad a NRM_label
city_to_nrm = {
    'Albury': 'Murray Basin', 'BadgerysCreek': 'East Coast', 'Cobar': 'Rangelands', 
    'CoffsHarbour': 'East Coast', 'Moree': 'Murray Basin', 'Newcastle': 'East Coast', 
    'NorahHead': 'East Coast', 'NorfolkIsland': 'External Territory', 'Penrith': 'East Coast', 
    'Richmond': 'East Coast', 'Sydney': 'East Coast', 'SydneyAirport': 'East Coast', 
    'WaggaWagga': 'Murray Basin', 'Williamtown': 'East Coast', 'Wollongong': 'East Coast', 
    'Canberra': 'Murray Basin', 'Tuggeranong': 'Murray Basin', 'MountGinini': 'Murray Basin', 
    'Ballarat': 'Southern Slopes', 'Bendigo': 'Murray Basin', 'Sale': 'East Coast', 
    'MelbourneAirport': 'Southern Slopes', 'Melbourne': 'Southern Slopes', 'Mildura': 'Murray Basin', 
    'Nhil': 'Murray Basin', 'Portland': 'Southern Slopes', 'Watsonia': 'Southern Slopes', 
    'Dartmoor': 'Southern Slopes', 'Brisbane': 'East Coast', 'Cairns': 'Wet Tropics', 
    'GoldCoast': 'East Coast', 'Townsville': 'Monsoonal North', 'Adelaide': 'Southern and South-Western Flatlands', 
    'MountGambier': 'Southern and South-Western Flatlands', 'Nuriootpa': 'Southern and South-Western Flatlands', 
    'Woomera': 'Rangelands', 'Albany': 'Southern and South-Western Flatlands', 
    'Witchcliffe': 'Southern and South-Western Flatlands', 'PearceRAAF': 'Southern and South-Western Flatlands', 
    'PerthAirport': 'Southern and South-Western Flatlands', 'Perth': 'Southern and South-Western Flatlands', 
    'SalmonGums': 'Southern and South-Western Flatlands', 'Walpole': 'Southern and South-Western Flatlands',
    'Hobart': 'Southern Slopes', 'Launceston': 'Southern Slopes', 'AliceSprings': 'Rangelands', 
    'Darwin': 'Monsoonal North', 'Katherine': 'Monsoonal North', 'Uluru': 'Rangelands'
}
df['NRM_label'] = df['Location'].map(city_to_nrm)
joblib.dump(city_to_nrm, os.path.join(output_dir, 'city_to_nrm.pkl'))
print("Artefacto 'city_to_nrm.pkl' guardado.")

# Limpieza y filtrado
df = df.dropna(subset=['RainTomorrow']).copy()
df['missing_count'] = df.isnull().sum(axis=1)
faltantes_permitidos = (len(df.columns.tolist()) - 7) // 2
df = df[df['missing_count'] <= faltantes_permitidos].copy()

# Mapeo de variables objetivo y predictoras
df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0})
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes': 1, 'No': 0})
df['RainToday'] = df['RainToday'].astype('Int64')

# --- 3. División de datos EXACTA a la del notebook ---
X = df.drop(columns='RainTomorrow')
y = df['RainTomorrow']
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# SEGUNDO SPLIT: Esta fue la parte que faltó replicar correctamente
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.125, random_state=42)
print("Datos divididos replicando la lógica del notebook.")

# --- 4. Cálculo y guardado de artefactos de imputación sobre el X_train correcto ---
# Mediana para variables numéricas
numeric_cols = ['MinTemp','MaxTemp','Temp9am','Temp3pm', 'Humidity9am','Humidity3pm', 'Pressure9am','Pressure3pm', 'Rainfall', 'WindGustSpeed','WindSpeed9am','WindSpeed3pm', 'Sunshine','Evaporation', 'Cloud9am','Cloud3pm']
medianas_por_grupo = X_train.groupby('NRM_label')[numeric_cols].median()
joblib.dump(medianas_por_grupo, os.path.join(output_dir, 'grouped_medians.pkl'))
print("Artefacto 'grouped_medians.pkl' guardado.")

# Moda para variables de viento
cols_viento = ['WindGustDir','WindDir9am','WindDir3pm']
modas_por_grupo = X_train.groupby('NRM_label')[cols_viento].agg(lambda x: x.mode().iat[0])
joblib.dump(modas_por_grupo, os.path.join(output_dir, 'grouped_modes.pkl'))
print("Artefacto 'grouped_modes.pkl' guardado.")

# --- 5. Preparar datos de entrenamiento para ajustar el Scaler ---
X_train_processed = X_train.copy()
X_train_processed.loc[X_train_processed['Evaporation'] > 60, 'Evaporation'] = np.nan

# A. Imputación
for col in numeric_cols:
    X_train_processed[col] = X_train_processed[col].fillna(X_train_processed['NRM_label'].map(medianas_por_grupo[col]))
for col in cols_viento:
    X_train_processed[col] = X_train_processed[col].fillna(X_train_processed['NRM_label'].map(modas_por_grupo[col]))
X_train_processed.loc[X_train_processed["RainToday"].isna() & (X_train_processed["Rainfall"] >= 1), "RainToday"] = 1
X_train_processed.loc[X_train_processed["RainToday"].isna(), "RainToday"] = 0

# B. Codificación Cíclica
wind_dir_to_deg = {'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5}
for col in cols_viento:
    X_train_processed[f'{col}_sin'] = np.sin(np.deg2rad(X_train_processed[col].map(wind_dir_to_deg)))
    X_train_processed[f'{col}_cos'] = np.cos(np.deg2rad(X_train_processed[col].map(wind_dir_to_deg)))

X_train_processed['Date'] = pd.to_datetime(X_train_processed['Date'])
X_train_processed['Month'] = X_train_processed['Date'].dt.month
X_train_processed['Month_sin'] = np.sin(2 * np.pi * X_train_processed['Month'] / 12)
X_train_processed['Month_cos'] = np.cos(2 * np.pi * X_train_processed['Month'] / 12)

# C. One-Hot Encoding
X_train_processed = pd.get_dummies(X_train_processed, columns=['NRM_label'], drop_first=True, dtype=int)

# D. Eliminar columnas que no van al modelo
cols_to_drop = ['Date', 'Month', 'Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'missing_count']
X_train_processed.drop(columns=cols_to_drop, inplace=True)

# E. Asegurar que las columnas están en el orden correcto
final_columns = [
    'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustSpeed',
    'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
    'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm', 'RainToday',
    'WindGustDir_sin', 'WindGustDir_cos', 'WindDir9am_sin', 'WindDir9am_cos',
    'WindDir3pm_sin', 'WindDir3pm_cos', 'Month_sin', 'Month_cos',
    'NRM_label_Central Slopes', 'NRM_label_East Coast', 'NRM_label_Monsoonal North',
    'NRM_label_Murray Basin', 'NRM_label_Rangelands', 'NRM_label_Southern Slopes',
    'NRM_label_Southern and South-Western Flatlands', 'NRM_label_Wet Tropics'
]

# El get_dummies puede no haber creado todas las columnas si no había ejemplos en el split
for col in final_columns:
    if col not in X_train_processed.columns:
        X_train_processed[col] = 0

X_train_final = X_train_processed[final_columns].astype('float64')


# --- 6. Ajustar y guardar Scaler y lista de columnas ---
scaler = StandardScaler()
scaler.fit(X_train_final)
joblib.dump(scaler, os.path.join(output_dir, 'scaler.pkl'))
print("Artefacto 'scaler.pkl' guardado.")

joblib.dump(final_columns, os.path.join(output_dir, 'final_columns.pkl'))
print("Artefacto 'final_columns.pkl' guardado.")


# --- 7. Entrenamiento y guardado del modelo de Red Neuronal ---
print("\nIniciando el entrenamiento del modelo de red neuronal...")


# Escalar los datos de entrenamiento que ya fueron procesados
X_train_scaled = scaler.transform(X_train_final)

# Configuración y compilación del modelo
tf.random.set_seed(42)
np.random.seed(42)

n_features = X_train_scaled.shape[1]

model = Sequential([
    Dense(64, activation='relu', input_shape=(n_features,)),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')  
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
)

# Callbacks y class weights
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

y_train_int = y_train.astype(int)
clases = np.unique(y_train_int)
pesos = compute_class_weight(class_weight='balanced', classes=clases, y=y_train_int)
class_weight = {int(clases[i]): pesos[i] for i in range(len(clases))}

# Entrenamiento
history = model.fit(
    X_train_scaled, y_train_int,
    validation_split=0.2,  
    epochs=100,
    batch_size=32,
    callbacks=[early_stop],
    class_weight=class_weight,
    verbose=1               
)

# Guardar el modelo en el directorio raíz
model.save('mejor_modelo_keras.h5')
print("\nModelo de red neuronal entrenado y guardado como 'mejor_modelo_keras.h5' en el directorio raíz.")