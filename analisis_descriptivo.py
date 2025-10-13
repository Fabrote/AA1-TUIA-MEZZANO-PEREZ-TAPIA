# ============================================================================
# ANÁLISIS DESCRIPTIVO DE VARIABLES - CLASIFICACIÓN POR TIPO
# ============================================================================

print("=" * 80)
print("CLASIFICACIÓN DE VARIABLES DEL DATASET WEATHER AUSTRALIA")
print("=" * 80)
print()

# Diccionario con descripción de cada variable
variable_info = {
    'Date': {
        'Tipo': 'Temporal',
        'Descripción': 'Fecha de la observación meteorológica',
        'Formato': 'YYYY-MM-DD',
        'Rango': 'Últimos 10 años de datos',
        'Uso': 'Identificador temporal, permite análisis de tendencias y estacionalidad'
    },
    'Location': {
        'Tipo': 'Categórica',
        'Descripción': 'Ciudad donde se realizó la observación',
        'Valores': '49 ciudades australianas',
        'Uso': 'Identificador geográfico, permite análisis regional'
    },
    'MinTemp': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Temperatura mínima del día (°C)',
        'Unidad': 'Grados Celsius',
        'Rango típico': '-8°C a 34°C',
        'Uso': 'Predictor importante para lluvia, indica condiciones térmicas nocturnas'
    },
    'MaxTemp': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Temperatura máxima del día (°C)',
        'Unidad': 'Grados Celsius',
        'Rango típico': '0°C a 48°C',
        'Uso': 'Predictor importante, indica condiciones térmicas diurnas'
    },
    'Rainfall': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Cantidad de precipitación registrada en el día (mm)',
        'Unidad': 'Milímetros',
        'Rango típico': '0 mm a 371 mm',
        'Uso': 'Indicador de lluvia del día actual, relacionado con RainTomorrow'
    },
    'Evaporation': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Evaporación de agua en 24 horas (mm)',
        'Unidad': 'Milímetros',
        'Rango típico': '0 mm a 145 mm',
        'Uso': 'Indica humedad atmosférica y balance hídrico',
        'Nota': '~43% de valores faltantes'
    },
    'Sunshine': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Horas de sol brillante en el día',
        'Unidad': 'Horas',
        'Rango típico': '0 a 14.5 horas',
        'Uso': 'Relacionado con nubosidad y probabilidad de lluvia',
        'Nota': '~48% de valores faltantes'
    },
    'WindGustDir': {
        'Tipo': 'Categórica Ordinal',
        'Descripción': 'Dirección de la ráfaga de viento más fuerte',
        'Valores': '16 direcciones cardinales (N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW)',
        'Uso': 'Patrón de viento, relacionado con sistemas meteorológicos'
    },
    'WindGustSpeed': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Velocidad de la ráfaga de viento más fuerte (km/h)',
        'Unidad': 'Kilómetros por hora',
        'Rango típico': '6 km/h a 135 km/h',
        'Uso': 'Intensidad del viento, relacionado con tormentas'
    },
    'WindDir9am': {
        'Tipo': 'Categórica Ordinal',
        'Descripción': 'Dirección del viento a las 9:00 AM',
        'Valores': '16 direcciones cardinales',
        'Uso': 'Patrón de viento matutino'
    },
    'WindDir3pm': {
        'Tipo': 'Categórica Ordinal',
        'Descripción': 'Dirección del viento a las 3:00 PM',
        'Valores': '16 direcciones cardinales',
        'Uso': 'Patrón de viento vespertino, importante para predicción'
    },
    'WindSpeed9am': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Velocidad del viento a las 9:00 AM (km/h)',
        'Unidad': 'Kilómetros por hora',
        'Rango típico': '0 km/h a 130 km/h',
        'Uso': 'Intensidad del viento matutino'
    },
    'WindSpeed3pm': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Velocidad del viento a las 3:00 PM (km/h)',
        'Unidad': 'Kilómetros por hora',
        'Rango típico': '0 km/h a 87 km/h',
        'Uso': 'Intensidad del viento vespertino, crítico para predicción a 23:59:59'
    },
    'Humidity9am': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Humedad relativa a las 9:00 AM (%)',
        'Unidad': 'Porcentaje',
        'Rango': '0% a 100%',
        'Uso': 'Indicador de humedad atmosférica matutina, relacionado con lluvia'
    },
    'Humidity3pm': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Humedad relativa a las 3:00 PM (%)',
        'Unidad': 'Porcentaje',
        'Rango': '0% a 100%',
        'Uso': 'Indicador de humedad vespertina, predictor fuerte de lluvia'
    },
    'Pressure9am': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Presión atmosférica a las 9:00 AM (hPa)',
        'Unidad': 'Hectopascales',
        'Rango típico': '980 hPa a 1041 hPa',
        'Uso': 'Indicador de sistemas de alta/baja presión, relacionado con clima'
    },
    'Pressure3pm': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Presión atmosférica a las 3:00 PM (hPa)',
        'Unidad': 'Hectopascales',
        'Rango típico': '977 hPa a 1040 hPa',
        'Uso': 'Cambios de presión indican frentes meteorológicos'
    },
    'Cloud9am': {
        'Tipo': 'Numérica Discreta',
        'Descripción': 'Fracción del cielo cubierto por nubes a las 9:00 AM',
        'Escala': '0 (despejado) a 8 (completamente nublado) oktas',
        'Uso': 'Indicador de nubosidad matutina',
        'Nota': '~38% de valores faltantes'
    },
    'Cloud3pm': {
        'Tipo': 'Numérica Discreta',
        'Descripción': 'Fracción del cielo cubierto por nubes a las 3:00 PM',
        'Escala': '0 (despejado) a 8 (completamente nublado) oktas',
        'Uso': 'Indicador de nubosidad vespertina, predictor de lluvia',
        'Nota': '~41% de valores faltantes'
    },
    'Temp9am': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Temperatura a las 9:00 AM (°C)',
        'Unidad': 'Grados Celsius',
        'Rango típico': '-7°C a 40°C',
        'Uso': 'Temperatura matutina, relacionada con evolución térmica del día'
    },
    'Temp3pm': {
        'Tipo': 'Numérica Continua',
        'Descripción': 'Temperatura a las 3:00 PM (°C)',
        'Unidad': 'Grados Celsius',
        'Rango típico': '-5°C a 46°C',
        'Uso': 'Temperatura vespertina, cercana al momento de predicción'
    },
    'RainToday': {
        'Tipo': 'Categórica Binaria',
        'Descripción': '¿Llovió hoy? (más de 1mm de precipitación)',
        'Valores': 'Yes / No',
        'Uso': 'Predictor importante, indica si hubo lluvia en el día actual'
    },
    'RainTomorrow': {
        'Tipo': 'Categórica Binaria (VARIABLE OBJETIVO)',
        'Descripción': '¿Lloverá mañana? (más de 1mm de precipitación)',
        'Valores': 'Yes / No',
        'Uso': 'VARIABLE OBJETIVO - Lo que queremos predecir a las 23:59:59',
        'Importancia': 'Esta es la variable dependiente del modelo'
    }
}

# ============================================================================
# CLASIFICACIÓN POR TIPO DE VARIABLE
# ============================================================================
print()

# Variables numéricas continuas
numericas_continuas = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                       'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm',
                       'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm',
                       'Temp9am', 'Temp3pm']

print(f"[+] Variables Numericas Continuas ({len(numericas_continuas)}):")
for var in numericas_continuas:
    print(f"  - {var}")
print()

# Variables numéricas discretas
numericas_discretas = ['Cloud9am', 'Cloud3pm']
print(f"[+] Variables Numericas Discretas ({len(numericas_discretas)}):")
for var in numericas_discretas:
    print(f"  - {var}")
print()

# Variables categóricas ordinales
categoricas_ordinales = ['WindGustDir', 'WindDir9am', 'WindDir3pm']
print(f"[+] Variables Categoricas Ordinales ({len(categoricas_ordinales)}):")
for var in categoricas_ordinales:
    print(f"  - {var}")
print()

# Variables categóricas nominales
categoricas_nominales = ['Location', 'RainToday', 'RainTomorrow']
print(f"[+] Variables Categoricas Nominales ({len(categoricas_nominales)}):")
for var in categoricas_nominales:
    print(f"  - {var}")
print()

# Variables temporales
temporales = ['Date']
print(f"[+] Variables Temporales ({len(temporales)}):")
for var in temporales:
    print(f"  - {var}")
print()

print()
print("=" * 80)
print(f"TOTAL: {len(numericas_continuas) + len(numericas_discretas) + len(categoricas_ordinales) + len(categoricas_nominales) + len(temporales)} variables originales")
print("=" * 80)
print()

# ============================================================================
# TABLA RESUMEN DE VARIABLES
# ============================================================================

print("\nTABLA RESUMEN DE VARIABLES:")
print("-" * 80)
print(f"{'Variable':<20} {'Tipo':<30} {'Descripcion':<50}")
print("-" * 80)

for var, info in variable_info.items():
    tipo = info['Tipo']
    desc = info['Descripción'][:47] + "..." if len(info['Descripción']) > 50 else info['Descripción']
    print(f"{var:<20} {tipo:<30} {desc:<50}")

print("-" * 80)
print("\nFin de la clasificacion de variables")
