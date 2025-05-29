# import streamlit as st
import sys
import os
import numpy as np
import pandas as pd 
import streamlit as st 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.constantes import DATA_CLEAN_PATH

st.title("1.3 (P3) Características demográficas")
st.subheader("En esta pagina se visualiza los datos demograficos")
# Abrir el Archivo
archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_hogar.csv"
df = pd.read_csv(archivo_clean_path, delimiter=",")

# Seleccionar trimestres disponibles 
anios =  sorted(df["ANO4"].astype(str).unique())
trimestres = sorted(df['TRIMESTRE'].astype(str).unique())

anio_seleccionado = st.number_input("Ingrese un año")
if str(anio_seleccionado) not in anios:
    st.error("No se a encontrado el año en el sistema, seleccione otro")
tri_seleccionado = st.selectbox("Seleccione el trimestre a buscar", options=trimestres)