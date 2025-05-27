import streamlit as st
import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.constantes import DATA_CLEAN_PATH

st.title("1.7 (P7) Ingresos")
st.write("""
El campo ITF es la sumatoria de los ingresos individuales totales de todos los componentes del hogar.
""")

# --- Cargar datos de hogares ---
archivo_hogares_path = DATA_CLEAN_PATH / "usu_clean_hogar.csv"
with archivo_hogares_path.open("r", encoding="utf-8") as archivo_hogares:
    reader = csv.reader(archivo_hogares, delimiter=",")
    header_hogar = next(reader)
    lista_filas_hogares = [fila for fila in reader if len(fila) == len(header_hogar)]

# --- Cargar datos de canasta básica ---
archivo_canasta_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv'))
with open(archivo_canasta_path, "r", encoding="utf-8") as archivo_canasta:
    reader = csv.reader(archivo_canasta, delimiter=",")
    header_canasta = next(reader)
    lista_filas_canasta = [fila for fila in reader if len(fila) == len(header_canasta)]

# --- Filtros de año y trimestre ---
anios = sorted(list(set([fila[1] for fila in lista_filas_hogares])))
trimestres = sorted(list(set([fila[2] for fila in lista_filas_hogares])))

anio_seleccionado = st.selectbox("Seleccione un año", options=anios)
trimestre_seleccionado = st.selectbox("Seleccione un trimestre", options=trimestres)

# --- Filtrar hogares de 4 integrantes ---
hogares_4 = [fila for fila in lista_filas_hogares if fila[5] == "4"]  # Ajustá el índice según tu header

# --- Filtrar por año y trimestre seleccionados ---
hogares_filtrados = [fila for fila in hogares_4 if fila[1] == anio_seleccionado and fila[2] == trimestre_seleccionado]

# --- Obtener valores de canasta básica para ese año y trimestre ---
canastas_filtradas = [fila for fila in lista_filas_canasta if fila[0] == anio_seleccionado and fila[1] == trimestre_seleccionado]
# Suponiendo que el archivo tiene columnas: año, mes, canasta_pobreza, canasta_indigencia

# --- Calcular cantidad y porcentaje de hogares bajo la línea de pobreza e indigencia ---
# (Ajustá los índices según tu header)
if canastas_filtradas:
    canasta_pobreza = float(canastas_filtradas[0][2])
    canasta_indigencia = float(canastas_filtradas[0][3])
    total_hogares = len(hogares_filtrados)
    bajo_pobreza = [h for h in hogares_filtrados if float(h[10]) < canasta_pobreza]  # ITF en columna 10, ajustar
    bajo_indigencia = [h for h in hogares_filtrados if float(h[10]) < canasta_indigencia]
    st.write(f"Total de hogares de 4 integrantes: {total_hogares}")
    st.write(f"Hogares bajo la línea de pobreza: {len(bajo_pobreza)} ({len(bajo_pobreza)/total_hogares*100:.2f}%)")
    st.write(f"Hogares bajo la línea de indigencia: {len(bajo_indigencia)} ({len(bajo_indigencia)/total_hogares*100:.2f}%)")
else:
    st.warning("No se encontró información de canasta básica para ese año y trimestre.")

st.info("Aclaración: los resultados no poseen valor estadístico. Los montos de la canasta básica pertenecen a CABA y la EPH es nacional. Solo se filtran hogares de 4 integrantes.")