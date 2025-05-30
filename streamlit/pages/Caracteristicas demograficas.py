# import streamlit as st
import sys
import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import streamlit as st 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.constantes import DATA_CLEAN_PATH
from src.utils.funciones import nombre_aglomerado



st.title("1.3 (P3) Características demográficas")
st.subheader("En esta pagina se visualiza los datos demograficos")

# Abrir el Archivo

archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"
df = pd.read_csv(archivo_clean_path, delimiter=",", low_memory=False)

# Seleccionar trimestres disponibles 

anios =  sorted(df["ANO4"].astype(str).unique())


anio_seleccionado = st.selectbox("Seleccione el año", options=anios)
if str(anio_seleccionado) not in anios:
    st.error("No se a encontrado el año en el sistema, seleccione otro")

df = df[df["ANO4"] == int(anio_seleccionado)]

trimestres = sorted(df['TRIMESTRE'].astype(str).unique())

tri_seleccionado = st.selectbox("Seleccione el trimestre a buscar", options=trimestres)

df = df[df["TRIMESTRE"] == int(tri_seleccionado)]


# Arreglando columna problematica
df['PP09A_ESP'] = df['PP09A_ESP'].fillna(0)

# ACTIV 1.3.1

## Filtrando para resolver la primera actividad
df_filtrado = df[["PONDERA","CH04", "CH06"]].copy()

rango_anios = range(0,101,10)
etiquetas =  [f"{i}-{i+9}" for i in rango_anios[:-1]] 

## Convirtiendo edades en enteros y creando una nueva columna "grupos_edad" que clasifique a las edades
df_filtrado["CH06"] = pd.to_numeric(df_filtrado["CH06"], errors="coerce")
df_filtrado["grupos_edad"] = pd.cut(df_filtrado["CH06"], bins=rango_anios , labels=etiquetas)

## Convirtiendo los valores de sexo en Strings legibles
df_filtrado["CH04"] = df_filtrado["CH04"].apply(lambda x: "M" if x == 1 else "F")

df_filtrado = df_filtrado.groupby(["CH04","grupos_edad"])["PONDERA"].sum().reset_index()

## Separando un df por Hombres y Mujeres
df_pivot = df_filtrado.pivot(index="grupos_edad",columns="CH04",values="PONDERA")

## Creando el grafico y mostrandolo 

st.bar_chart(df_pivot, stack=False)

# ACTIV 1.3.2

st.subheader("Promedio de edades para los aglomerados del ultimo archivo ingresado")

ultimo_anio = int(df["ANO4"].unique().max())
df_ult_anio = df[df["ANO4"] == ultimo_anio]
ultimo_trim = int(df_ult_anio["TRIMESTRE"].unique().max())

df_reciente = df_ult_anio[df_ult_anio["TRIMESTRE"] == ultimo_trim]

df_aglomerado = df_ult_anio[["AGLOMERADO","CH06"]].copy()
df_aglomerado['nombre_aglomerado'] = df_aglomerado['AGLOMERADO'].astype(str).apply(nombre_aglomerado)

df_aglomerado = df_aglomerado.groupby(["AGLOMERADO","nombre_aglomerado"]).mean("CH06")
df_aglomerado['CH06'] = df_aglomerado['CH06'].round(2)

df_aglomerado = df_aglomerado.rename(columns={'CH06': 'Promedio de edades',"nombre_aglomerado": "Nombre del aglomerado"})


st.dataframe(df_aglomerado)

# ACTIV 1.3.3 

aglo_seleccionado = st.number_input("Ingrese el Aglomerado", min_value=0, step=1, format="%d")

df_activos = df[(df["AGLOMERADO"] == aglo_seleccionado) & (df["CH06"].between(15,64,inclusive="both")) ][["AGLOMERADO","CH06","PONDERA"]].copy()
df_not_activos = df[(df["AGLOMERADO"] == aglo_seleccionado) & ( ~df["CH06"].between(15,64,inclusive="both")) ][["AGLOMERADO","CH06","PONDERA"]].copy()

df_activos = df_activos.groupby(["AGLOMERADO"]).sum("PONDERA")
df_not_activos = df_not_activos.groupby(["AGLOMERADO"]).sum("PONDERA")

df_not_activos["grupo"] = "no activos"
df_activos["grupo"] = "activos"

df_activos = df_activos.rename(columns={"PONDERA" : "PONDERA_A"})
df_not_activos = df_not_activos.rename(columns={"PONDERA" : "PONDERA_NA"})

df_union = df_activos.merge(df_not_activos, on="AGLOMERADO", how="inner")
df_union["Cociente Activos/noActivos"] = ( df_union["PONDERA_NA"] / df_union["PONDERA_A"]  ) * 100

st.dataframe(df_union[["PONDERA_A", "PONDERA_NA", "Cociente Activos/noActivos"]])
# HACER UNA GRAFICA DE TORTA DE ACTIVOS Y NO ACTIVOS 