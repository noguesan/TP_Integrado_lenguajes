# import streamlit as st
import sys
import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import streamlit as st 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.constantes import DATA_CLEAN_PATH



st.title("1.3 (P3) Características demográficas")
st.subheader("En esta pagina se visualiza los datos demograficos")

# Abrir el Archivo

archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"
df = pd.read_csv(archivo_clean_path, delimiter=",", low_memory=False)

# Seleccionar trimestres disponibles 

anios =  sorted(df["ANO4"].astype(str).unique())
trimestres = sorted(df['TRIMESTRE'].astype(str).unique())

anio_seleccionado = st.selectbox("Seleccione el año", options=anios)
if str(anio_seleccionado) not in anios:
    st.error("No se a encontrado el año en el sistema, seleccione otro")

tri_seleccionado = st.selectbox("Seleccione el trimestre a buscar", options=trimestres)

df = df[df["ANO4"] == int(anio_seleccionado)]

# Arreglando columna problematica
df['PP09A_ESP'] = df['PP09A_ESP'].fillna(0)

""" ACTIV 1.3.1 """

# Filtrando para resolver la primera actividad
df_filtrado = df[["PONDERA","CH04", "CH06"]].copy()

rango_anios = range(0,101,10)
etiquetas =  [f"{i}-{i+9}" for i in rango_anios[:-1]] 

# Convirtiendo edades en enteros y creando una nueva columna "grupos_edad" que clasifique a las edades
df_filtrado["CH06"] = pd.to_numeric(df_filtrado["CH06"], errors="coerce")
df_filtrado["grupos_edad"] = pd.cut(df_filtrado["CH06"], bins=rango_anios , labels=etiquetas)

# Convirtiendo los valores de sexo en Strings legibles
df_filtrado["CH04"] = df_filtrado["CH04"].apply(lambda x: "M" if x == 1 else "F")

df_filtrado = df_filtrado.groupby(["grupos_edad","CH04"])["PONDERA"].sum().reset_index()

# Separando un df por Hombres y Mujeres
df_hombres = df_filtrado[df_filtrado["CH04"] == 'M'].copy()
df_mujeres = df_filtrado[df_filtrado["CH04"] == 'F'].copy()

# Creando el grafico y mostrandolo 
x = np.arange(len(df_hombres.index))
ancho = 0.35 
valores_y = range(0,5000000, 1000000)
labels_y = ["0","1.000.000","2.000.000","3.000.000","4.000.000","5.000.000"]

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(x - ancho / 2 , df_hombres["PONDERA"], width=ancho, label="hombres")
ax.bar(x + ancho / 2 , df_mujeres["PONDERA"], width=ancho, label="mujeres")

ax.set_xlabel("grupos por edad") 
ax.set_ylabel("cantidad de gente") 

ax.set_xticks(x)
ax.set_xticklabels(df_hombres["grupos_edad"])
ax.set_yticklabels(labels_y)

ax.legend()

st.pyplot(fig)


