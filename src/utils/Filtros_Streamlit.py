import pandas as pd
import streamlit as st
from src.utils.constantes import DATA_CLEAN_PATH
import json
import os

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
        aglomerados_dict_str = json.load(f)

    # Convertir las claves del diccionario de str a int
    aglomerados_dict = {int(k): v for k, v in aglomerados_dict_str.items()}    

    return aglomerados_dict

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

    df_filtrado_Ano4Trimestre = df[
        (df["ANO4"] == anio) &
        (df["TRIMESTRE"] == trimestre)
    ]

    if aglomerado != "Todos":
        df_filtrado_aglomerado = df[df["AGLOMERADO"] == aglomerado]
        df_filtrado = df_filtrado_Ano4Trimestre[df_filtrado_Ano4Trimestre["AGLOMERADO"] == aglomerado]
    else:
        df_filtrado_aglomerado = df
        df_filtrado = df_filtrado_Ano4Trimestre


    return df_filtrado,df_filtrado_aglomerado ,df_filtrado_Ano4Trimestre


    # # Cargar archivo
    # archivo_personas_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"



def mostrar_sidebar_con_filtros(path):

    try:
        df = pd.read_csv(path, encoding="utf-8", low_memory=False)
        st.sidebar.success(f"Archivo cargado correctamente. Filas: {len(df)}")
    except Exception as e:
        st.sidebar.error(f"No se pudo cargar el archivo: {e}")
        return None, None, None, None

    # Diccionario Año → Trimestres
    anios_trimestres = {}
    for anio in sorted(df["ANO4"].dropna().unique()):
        trimestres = sorted(df[df["ANO4"] == anio]["TRIMESTRE"].dropna().unique())
        anios_trimestres[anio] = trimestres

    # Selectboxes
    anio_seleccionado = st.sidebar.selectbox("Seleccione un año", options=list(anios_trimestres.keys()))
    trimestres_disponibles = anios_trimestres[anio_seleccionado]
    trimestre_seleccionado = st.sidebar.selectbox("Seleccione un trimestre", options=trimestres_disponibles)

    # Aglomerados
    aglomerados_dict = cargar_aglomerados_coordenadas()
    opciones_aglomerados = [("Todos", "Todos")] + [
        (info["nombre"], codigo) for codigo, info in sorted(aglomerados_dict.items())
    ]
    aglomerado_nombre_seleccionado = st.sidebar.selectbox(
        "Seleccione un aglomerado (opcional)",
        options=opciones_aglomerados,
        format_func=lambda x: x[0]
    )
    aglomerado_seleccionado = aglomerado_nombre_seleccionado[1]

    # Filtrado
    df_filtrado,df_filtrado_aglomerado ,df_filtrado_Ano4Trimestre = filtrar_dataframe(df, anio_seleccionado, trimestre_seleccionado, aglomerado_seleccionado)

    return df, df_filtrado,df_filtrado_aglomerado ,df_filtrado_Ano4Trimestre