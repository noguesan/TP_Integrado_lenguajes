import streamlit as st
import csv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.constantes import DATA_CLEAN_PATH
from src.utils.funciones import agrupar_por_aglomerado, agrupar_por_anio_y_trimestre

st.title("1.5 (P5) Actividad y empleo")
st.write("""
En esta sección se visualizará información relacionada a la actividad y empleo según la EPH.
""")

# --- Cargar datos de personas ---
archivo_personas_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"
with archivo_personas_path.open("r", encoding="utf-8") as archivo_personas:
    reader = csv.reader(archivo_personas, delimiter=",")
    header = next(reader)
    lista_filas_personas = []
    for fila in reader:
        if len(fila) == len(header):
            lista_filas_personas.append(fila)
        elif len(fila) > 0:
            st.warning(f"Fila problemática: {fila} (tiene {len(fila)} columnas, debería tener {len(header)})")

st.info(f"Filas válidas: {len(lista_filas_personas)}")

# --- Filtros generales ---
anios = sorted(list(set([fila[1] for fila in lista_filas_personas])))
trimestres = sorted(list(set([fila[2] for fila in lista_filas_personas])))
aglomerados = sorted(list(set([fila[7] for fila in lista_filas_personas])))

anio_seleccionado = st.selectbox("Seleccione un año", options=anios)
trimestre_seleccionado = st.selectbox("Seleccione un trimestre", options=trimestres)
aglomerado_seleccionado = st.selectbox("Seleccione un aglomerado (opcional)", options=["Todos"] + aglomerados)

# --- 1.5.1 Cantidad de desocupados por nivel educativo ---
st.subheader("1.5.1 Desocupados por nivel educativo")
# Aquí va el código para filtrar y mostrar la cantidad de desocupados según estudios alcanzados

# --- 1.5.2 Evolución de la tasa de desempleo ---
st.subheader("1.5.2 Evolución de la tasa de desempleo")
# Aquí va el código para calcular y graficar la evolución de la tasa de desempleo

# --- 1.5.3 Evolución de la tasa de empleo ---
st.subheader("1.5.3 Evolución de la tasa de empleo")
# Aquí va el código para calcular y graficar la evolución de la tasa de empleo

# --- 1.5.4 Porcentaje de empleo estatal, privado y otro por aglomerado ---
st.subheader("1.5.4 Porcentaje de empleo estatal, privado y otro por aglomerado")
# Aquí va el código para calcular y mostrar los porcentajes por aglomerado

# --- 1.5.5 Mapa de evolución de tasas por aglomerado ---
st.subheader("1.5.5 Mapa de evolución de tasas por aglomerado")
# Aquí va el código para calcular los porcentajes y mostrar el mapa con puntos verdes/rojos según corresponda