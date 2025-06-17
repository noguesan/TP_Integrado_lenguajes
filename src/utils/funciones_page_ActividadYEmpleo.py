import streamlit as st
import csv
import pandas as pd
import sys
import os
import folium
import json

# Mapas de significado
# columna ESTADO
estado_map = {
    0: 'No respondió',
    1: 'Ocupado',
    2: 'Desocupado',
    3: 'Inactivo',
    4: 'Menor de 10 años'
}

# columna NIVEL_ED
nivel_ed_map = {
    1: 'Primario incompleto',
    2: 'Primario completo',
    3: 'Secundario incompleto',
    4: 'Secundario completo',
    5: 'Superior univ. incompleto',
    6: 'Superior univ. completo',
    7: 'Sin instrucción',
    9: 'Ns/Nr'
}

# columna PP04A * ¿El negocio / empresa / institución /actividad en la que trabaja es...
mapa_tipo_empleo = {
    1: 'Estatal',
    2: 'Privado',
    3: 'Otro'
}

def filtrar_dataframe(df, anio, trimestre, aglomerado):
    """
    Filtra el DataFrame según año, trimestre y opcionalmente aglomerado.

    Parámetros:
        df (pd.DataFrame): El DataFrame original.
        anio (int): Año seleccionado.
        trimestre (int): Trimestre seleccionado.
        aglomerado (int o str): Aglomerado seleccionado, o "Todos".

    Retorna:
        pd.DataFrame: El DataFrame filtrado.
    """

    df_filtrado = df[
        (df["ANO4"] == anio) &
        (df["TRIMESTRE"] == trimestre)
    ]

    if aglomerado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["AGLOMERADO"] == aglomerado]

    return df_filtrado


# FUNCIONES AXULIARES

def resaltar_columnas(tabla, columnas, color = '#ffeeba'):
    """
    Devuelve un DataFrame estilizado, resaltando una o varias columnas con un color de fondo suave
    y texto negro.

    Parámetros:
    - tabla: pd.DataFrame, la tabla original.
    - columnas: str o lista/tupla de str, nombre(s) de columna(s) a resaltar.
    - color: str, color de fondo en formato CSS (por defecto: amarillo suave).

    Retorna:
    - pd.io.formats.style.Styler: la tabla con estilo aplicado.

    Ejemplo de uso:
    resaltar_columnas(df, 'Desocupados')
    resaltar_columnas(df, ['Desocupados', 'Ocupados'])
    """

    return tabla.style.set_properties(
        subset=columnas,
        **{
            'background-color': color,
            'color': 'black',
            'font-weight': 'bold'
        }
    )


# def calcular_estado_por_aglomerado(df):
#     """
#     Calcula por aglomerado la cantidad de Ocupados, Desocupados, Inactivos
#     y el total de personas (sin incluir 'No respondió' ni 'Menor de 10 años').
#     """
#     # Filtrar registros válidos (excluye 0 = No respondió y 4 = Menor de 10 años)
#     df_filtrado = df[df['ESTADO'].isin([1, 2, 3])].copy()

#     # Agrupar por AGLOMERADO y ESTADO, sumando ponderadores
#     resumen = df_filtrado.groupby(['AGLOMERADO', 'ESTADO'])['PONDERA'].sum().unstack(fill_value=0)

#     # Renombrar columnas según estado
#     resumen = resumen.rename(columns={
#         1: 'Ocupado',
#         2: 'Desocupado',
#         3: 'Inactivo'
#     })

#     # Asegurar que todas las columnas estén presentes
#     for col in ['Ocupado', 'Desocupado', 'Inactivo']:
#         if col not in resumen.columns:
#             resumen[col] = 0

#     # Calcular el total
#     resumen['Total'] = resumen[['Ocupado', 'Desocupado', 'Inactivo']].sum(axis=1)

#     # Reemplazar los códigos de aglomerado por su nombre
#     # Construir diccionario de nombres
#     aglomerado_nombres = {int(k): v["nombre"] for k, v in aglomerados_dict.items()}
#     resumen.index = resumen.index.map(aglomerado_nombres)

#     # Resetear el índice sin cambiar el nombre de la columna
#     resumen = resumen.reset_index()

#     # Ordenar por nombre de aglomerado
#     resumen = resumen.sort_values('AGLOMERADO')

#     return resumen


# FUNCIONES

## 1.5.1.Para las personas desocupadas, informar la cantidad de ellas según sus estudios alcanzados.
## Se debe informar para un año y trimestre elegido por el usuario.

def resumen_nivel_educativo(df):
    """
    Genera una tabla que cruza el nivel educativo alcanzado con la condición de actividad 
    (ocupado, desocupado, inactivo), ponderando los casos por la variable 'PONDERA'.
    Excluye a quienes no respondieron o son menores de 10 años.
    """
    # Mapear descripciones
    df['ESTADO_DESC'] = df['ESTADO'].map(estado_map)
    df['NIVEL_ED_DESC'] = df['NIVEL_ED'].map(nivel_ed_map)

    # Filtrar personas válidas (ocupado, desocupado, inactivo)
    df_validos = df[df['ESTADO'].isin([1, 2, 3])].copy()

    # Tabla cruzada ponderada: Nivel educativo vs Condición de actividad
    tabla = df_validos.pivot_table(
        index='NIVEL_ED_DESC',
        columns='ESTADO_DESC',
        values='PONDERA',
        aggfunc='sum',
        fill_value=0
    )

    # Ordenar por total descendente
    tabla['Total'] = tabla.sum(axis=1)
    tabla = tabla.sort_values(by='Total', ascending=False)

    # (Opcional) Eliminar la columna de total si no se quiere mostrar
    tabla = tabla.drop(columns='Total')

    return tabla



## 1.5.2 Informar la evolución del desempleo(tasa de desempleo) a lo largo del tiempo. Se debe poder fi ltrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.  
## La tasa de desempleo es el cociente de personas desocupadas y la suma de personas desocupadas más ocupadas multiplicado por 100.  

## 1.5.3 Informar la evolución del empleo (tasa de empleo) a lo largo del tiempo. Se debe poder fi ltrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.  
## La tasa de empleo es el cociente entre personas ocupadas y la suma de personas desocupadas más ocupadas multiplicado por 100.  

## El codigo responde a ambas preguntas

def evolucion_tasas(df):
    """
    Calcula la evolución de la tasa de desempleo y empleo a lo largo del tiempo,
    mostrando también la cantidad de Ocupados y Desocupados (ponderados).

    Parámetros:
    - df: DataFrame con columnas 'ANO4', 'TRIMESTRE', 'ESTADO', 'PONDERA'

    Retorna:
    - DataFrame con columnas: Año, Trimestre, Ocupados, Desocupados,
      Tasa de Desempleo (%), Tasa de Empleo (%)
    """
    # Filtrar solo Ocupados (1) y Desocupados (2)
    df_actividad = df[df['ESTADO'].isin([1, 2])].copy()

    # Agrupar por año, trimestre y estado, sumar PONDERA
    agrupado = df_actividad.groupby(['ANO4', 'TRIMESTRE', 'ESTADO'])['PONDERA'].sum().unstack(fill_value=0)

    # Renombrar columnas según código
    agrupado = agrupado.rename(columns={1: 'Ocupados', 2: 'Desocupados'})

    # Calcular tasas
    total = agrupado['Ocupados'] + agrupado['Desocupados']
    agrupado['Tasa de Desempleo (%)'] = (agrupado['Desocupados'] / total) * 100
    agrupado['Tasa de Empleo (%)'] = (agrupado['Ocupados'] / total) * 100

    # Reset index para mejor presentación
    resultado = agrupado.reset_index()

    
    return resultado[['ANO4', 'TRIMESTRE', 'Ocupados','Desocupados', 'Tasa de Desempleo (%)', 'Tasa de Empleo (%)']]


# 1.5.4 Informar para cada aglomerado el total de personas ocupadas, el porcentaje con empleo estatal, el porcentaje con empleo privado y el porcentaje de otro tipo. Considerar la ocupación principal.  

def calcular_empleo_por_aglomerado(df):
    """
    Devuelve un DataFrame con el total de ocupados por aglomerado,
    y los porcentajes según el tipo de empleo principal.
    """
    
    # Agrupar por aglomerado y tipo de empleo
    tabla = df.groupby(['AGLOMERADO', 'PP04A'])['PONDERA'].sum().unstack(fill_value=0).reset_index()
    
    # Renombrar columnas con el mapa
    tabla = tabla.rename(columns=mapa_tipo_empleo)
    
    # Calcular total y porcentajes
    tabla['Total Ocupados'] = tabla[['Estatal', 'Privado', 'Otro']].sum(axis=1)
    tabla['% Estatal'] = 100 * tabla['Estatal'] / tabla['Total Ocupados']
    tabla['% Privado'] = 100 * tabla['Privado'] / tabla['Total Ocupados']
    tabla['% Otro'] = 100 * tabla['Otro'] / tabla['Total Ocupados']
    
    return tabla[['AGLOMERADO', 'Total Ocupados', '% Estatal', '% Privado', '% Otro']]

# 1.5.5 Se debe obtener por aglomerado el porcentaje de la tasa de empleo y desempleo. Esta información se requiere conocer para el año y trimestre más antiguo del cual se contenga 
# información y para el año y trimestre más actual del cual se cuenta información.
# A partir de dicha información se debe visualizar un mapa que por aglomerado muestre con el color de un punto/marca si el porcentaje aumentó o disminuyó. 
# El usuario elegirá si desea ver tasa de empleo o desempleo:
# - Al elegir la tasa de empleo se deben ver puntos verdes en los aglomerados cuya tasa de empleo aumentó con el correr del tiempo. Rojo en el caso contrario.
# - Al elegir la tasa de desempleo se deben ver puntos rojos en los aglomerados cuya tasa de empleo aumentó con el correr del tiempo. Verde en el caso contrario.

## 1- Crear 2 dataframe uno con tasas de empleo y otro con tasas de desempleo
def obtener_primer_y_ultimo_periodo(df):
    """
    Obtiene el primer y el último período disponibles en el DataFrame
    basado en las columnas 'ANO4' y 'TRIMESTRE'.

    Retorna:
    - Tuple (periodo_mas_antiguo, periodo_mas_reciente), cada uno como (año, trimestre)
    """
    # Ordenar por año y trimestre
    ordenado = df.sort_values(by=['ANO4', 'TRIMESTRE'])

    # Primer registro
    primero = ordenado[['ANO4', 'TRIMESTRE']].iloc[0]
    periodo_primero = (primero['ANO4'], primero['TRIMESTRE'])

    # Último registro
    ultimo = ordenado[['ANO4', 'TRIMESTRE']].iloc[-1]
    periodo_ultimo = (ultimo['ANO4'], ultimo['TRIMESTRE'])

    return periodo_primero, periodo_ultimo

def filtrar_dos_periodos(df, periodo_ini, periodo_fin):
    """
    Filtra el DataFrame para que contenga solo los registros de los dos períodos dados.

    Parámetros:
    - df: DataFrame original
    - periodo_ini: (año, trimestre)
    - periodo_fin: (año, trimestre)

    Retorna:
    - DataFrame filtrado
    """
    año1, trim1 = periodo_ini
    año2, trim2 = periodo_fin
    return df[((df['ANO4'] == año1) & (df['TRIMESTRE'] == trim1)) |
              ((df['ANO4'] == año2) & (df['TRIMESTRE'] == trim2))].copy()


def calcular_tasas_por_aglomerado(df):
    """
    Calcula Ocupados, Desocupados, Tasa de Empleo y Desempleo
    por Aglomerado, Año y Trimestre.

    Requiere columnas: 'ANO4', 'TRIMESTRE', 'AGLOMERADO', 'ESTADO', 'PONDERA'

    Retorna:
    - DataFrame con columnas: 'ANO4', 'TRIMESTRE', 'AGLOMERADO', 'Ocupados', 'Desocupados',
                              'Tasa de Empleo (%)', 'Tasa de Desempleo (%)'
    """
    # Solo Ocupados (1) y Desocupados (2)
    df_filtrado = df[df['ESTADO'].isin([1, 2])].copy()

    # Agrupamos
    agrupado = df_filtrado.groupby(['ANO4', 'TRIMESTRE', 'AGLOMERADO', 'ESTADO'])['PONDERA'].sum().unstack(fill_value=0)

    # Renombrar columnas
    agrupado = agrupado.rename(columns={1: 'Ocupados', 2: 'Desocupados'})

    # Calcular tasas
    agrupado['Total'] = agrupado['Ocupados'] + agrupado['Desocupados']
    agrupado['Tasa de Empleo (%)'] = (agrupado['Ocupados'] / agrupado['Total']) * 100
    agrupado['Tasa de Desempleo (%)'] = (agrupado['Desocupados'] / agrupado['Total']) * 100

    agrupado = agrupado.reset_index()
    return agrupado[['ANO4', 'TRIMESTRE', 'AGLOMERADO', 'Tasa de Empleo (%)', 'Tasa de Desempleo (%)']]


def comparar_tasas_aglomerados(df_tasas, periodo_ini, periodo_fin, tipo='Tasa de Empleo (%)'):
    """
    Compara la tasa entre dos períodos por aglomerado y marca si subió o bajó.

    Parámetros:
    - df_tasas: DataFrame generado por calcular_tasas_por_aglomerado
    - periodo_ini: (año, trimestre)
    - periodo_fin: (año, trimestre)
    - tipo: 'Tasa de Empleo (%)' o 'Tasa de Desempleo (%)'

    Retorna:
    - DataFrame con columnas: AGLOMERADO, tasa_inicial, tasa_final, diferencia, cambio ('sube' o 'baja')
    """
    a_ini, t_ini = periodo_ini
    a_fin, t_fin = periodo_fin

    df_ini = df_tasas[(df_tasas['ANO4'] == a_ini) & (df_tasas['TRIMESTRE'] == t_ini)][['AGLOMERADO', tipo]]
    df_fin = df_tasas[(df_tasas['ANO4'] == a_fin) & (df_tasas['TRIMESTRE'] == t_fin)][['AGLOMERADO', tipo]]

    df_merged = df_ini.merge(df_fin, on='AGLOMERADO', suffixes=('_ini', '_fin'))
    df_merged['diferencia'] = df_merged[f'{tipo}_fin'] - df_merged[f'{tipo}_ini']
    df_merged['cambio'] = df_merged['diferencia'].apply(lambda x: 'sube' if x > 0 else 'baja')

    return df_merged

def evolucion_tasas_aglomerados(df):
    """
    Calcula la evolución de las tasas de empleo y desempleo entre el primer
    y el último período disponibles en el DataFrame.

    Parámetros:
    - df: DataFrame original, debe contener las columnas 'ANO4', 'TRIMESTRE', 
          'AGLOMERADO', 'ESTADO', 'PONDERA'.

    Retorna:
    - Tuple (df_comparacion_empleo, df_comparacion_desempleo):
        * df_comparacion_empleo: comparación de tasa de empleo entre dos períodos.
        * df_comparacion_desempleo: comparación de tasa de desempleo entre dos períodos.
    """
    # 1. Obtener el primer y último período
    periodo_ini, periodo_fin = obtener_primer_y_ultimo_periodo(df)

    # 2. Filtrar DataFrame para esos dos períodos
    df_filtrado = filtrar_dos_periodos(df, periodo_ini, periodo_fin)

    # 3. Calcular tasas por aglomerado
    df_tasas = calcular_tasas_por_aglomerado(df_filtrado)

    # 4. Comparar tasas para empleo y desempleo
    df_comparacion_empleo = comparar_tasas_aglomerados(df_tasas, periodo_ini, periodo_fin, tipo='Tasa de Empleo (%)')
    df_comparacion_desempleo = comparar_tasas_aglomerados(df_tasas, periodo_ini, periodo_fin, tipo='Tasa de Desempleo (%)')

    return df_comparacion_empleo, df_comparacion_desempleo

## 2- Cargar datos de coordenadas (archivos json) y poner las coordenadas en los dataframe

def cargar_aglomerados_coordenadas():
    """
    Carga un diccionario con las coordenadas de los aglomerados desde un archivo JSON.

    Retorna:
        dict: Diccionario con los datos de aglomerados y sus coordenadas.
    """
    # Ruta relativa desde src/utils hacia la raíz del proyecto
    json_path = os.path.abspath(os.path.join(os.getcwd(), "aglomerados_coordenadas.json"))

    # Abrir y leer el archivo
    with open(json_path, "r", encoding="utf-8") as f:
        aglomerados_dict = json.load(f)

    return aglomerados_dict

def agregar_coordenadas_a_tasas(df_empleo, df_desempleo):
    """
    Agrega las coordenadas (latitud, longitud) y el nombre del aglomerado
    a los DataFrames de comparación de tasas.

    Parámetros:
    - df_empleo: DataFrame con comparación de tasa de empleo.
    - df_desempleo: DataFrame con comparación de tasa de desempleo.

    Retorna:
    - Tuple (df_empleo, df_desempleo) con columnas extra: 'lat', 'lon', 'nombre_aglomerado'
    """
    # Importar la función si está en otro archivo o módulo
    #from src.utils.funciones_page_ActividadYEmpleo import cargar_aglomerados_coordenadas

    # Cargar diccionario de coordenadas
    aglomerados_dict = cargar_aglomerados_coordenadas()

    # Crear mapas desde el diccionario
    mapa_lat = {int(k): v['coordenadas'][0] for k, v in aglomerados_dict.items()}
    mapa_lon = {int(k): v['coordenadas'][1] for k, v in aglomerados_dict.items()}
    mapa_nombre = {int(k): v['nombre'] for k, v in aglomerados_dict.items()}

    # Asegurar que AGLOMERADO sea int
    df_empleo['AGLOMERADO'] = df_empleo['AGLOMERADO'].astype(int)
    df_desempleo['AGLOMERADO'] = df_desempleo['AGLOMERADO'].astype(int)

    # Agregar columnas con mapeo
    for df in [df_empleo, df_desempleo]:
        df['lat'] = df['AGLOMERADO'].map(mapa_lat)
        df['lon'] = df['AGLOMERADO'].map(mapa_lon)
        df['nombre_aglomerado'] = df['AGLOMERADO'].map(mapa_nombre)

    return df_empleo, df_desempleo

## Generar mapa


def generar_mapa(df, color_positivo='red', color_negativo='green'):
    """
    Genera un mapa con círculos coloreados según el valor de la columna 'diferencia'.
    
    Parámetros:
    - df: DataFrame con columnas ['lat', 'lon','nombre_aglomerado', 'diferencia']
    - color_positivo: Color para diferencias positivas
    - color_negativo: Color para diferencias negativas
    """

    # Crear el mapa base centrado en Argentina
    m = folium.Map(location=(-33.457606, -65.346857), zoom_start=5, tiles='cartodbpositron')

    # Detectar automáticamente la tasa según columnas terminadas en _ini y _fin
    col_ini = [col for col in df.columns if col.endswith('_ini')]
    col_fin = [col for col in df.columns if col.endswith('_fin')]

    tasa_ini_col = col_ini[0]
    tasa_fin_col = col_fin[0]
    tasa_nombre = tasa_ini_col.replace('_ini', '')  # Ej: "Tasa de Empleo (%)"

    for _, row in df.iterrows():
        diferencia = row['diferencia']

        if pd.notnull(diferencia):
            color = color_positivo if diferencia > 0 else color_negativo
        else:
            color = 'gray'

        popup_text = (
            f"{row['nombre_aglomerado']}<br>"
            f"{tasa_nombre}<br>"
            f"Inicio: {row[tasa_ini_col]:.1f}% → Fin: {row[tasa_fin_col]:.1f}%<br>"
            f"Diferencia: {diferencia:.2f}%"
        )

        folium.CircleMarker(
            location=(row['lat'], row['lon']),
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=250)
        ).add_to(m)

    return m
