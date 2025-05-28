import streamlit as st
import csv
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.constantes import DATA_CLEAN_PATH

st.title("1.3 (P3) Características demográficas")
st.write("""
En esta sección se visualizará información relacionada a las características demográficas de la población argentina según la EPH.
""")

# --- Cargar datos de personas ---
archivo_personas_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"
with archivo_personas_path.open("r", encoding="utf-8") as archivo_personas:
    reader = csv.reader(archivo_personas, delimiter=",")
    header = next(reader)
    lista_filas_personas = [fila for fila in reader if len(fila) == len(header)]

# --- Filtros generales ---
anios = sorted(list(set([fila[1] for fila in lista_filas_personas])))
trimestres = sorted(list(set([fila[2] for fila in lista_filas_personas])))
aglomerados = sorted(list(set([fila[7] for fila in lista_filas_personas])))

# --- 1.3.1 Gráfico de barras por grupos de edad y sexo ---
st.subheader("1.3.1 Distribución por grupos de edad y sexo")
anio_seleccionado = st.selectbox("Seleccione un año", options=anios)
trimestre_seleccionado = st.selectbox("Seleccione un trimestre", options=trimestres)

# Aquí va el código para agrupar por grupos de edad (cada 10 años) y sexo, y graficar

# --- 1.3.2 Edad promedio por aglomerado ---
st.subheader("1.3.2 Edad promedio por aglomerado")
# Aquí va el código para calcular y mostrar la edad promedio por aglomerado para el último año y trimestre

# --- 1.3.3 Evolución de la dependencia demográfica ---
st.subheader("1.3.3 Evolución de la dependencia demográfica")
aglomerado_seleccionado = st.selectbox("Seleccione un aglomerado", options=aglomerados)
# Aquí va el código para calcular y mostrar la evolución de la dependencia demográfica

# --- 1.3.4 Media y mediana de la edad por año y trimestre ---
st.subheader("1.3.4 Media y mediana de la edad por año y trimestre")
# Aquí va el código para calcular y mostrar la media y mediana de la edad de la población por año y trimestre

