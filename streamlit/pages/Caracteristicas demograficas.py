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
st.subheader("En esta pagina se visualiza los datos demograficos de los archivos")

# Abrir el Archivo
st.header("Poblacion para el año y trimestre ingresado")
archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"
df = pd.read_csv(archivo_clean_path, delimiter=",", low_memory=False)
df['PP09A_ESP'] = df['PP09A_ESP'].fillna(0)
# Seleccionar trimestres disponibles 

anios =  sorted(df["ANO4"].astype(str).unique())
aglomerados = sorted(df["AGLOMERADO"].unique())

anio_seleccionado = st.selectbox("Seleccione el año", options=anios)
if str(anio_seleccionado) not in anios:
    st.error("No se a encontrado el año en el sistema, seleccione otro")

df_anio_selec = df[df["ANO4"] == int(anio_seleccionado)].copy()

trimestres = sorted(df_anio_selec['TRIMESTRE'].astype(str).unique())

tri_seleccionado = st.selectbox("Seleccione el trimestre a buscar", options=trimestres)

df_tri_anio_selec = df_anio_selec[df_anio_selec["TRIMESTRE"] == int(tri_seleccionado)]

# ACTIV 1.3.1

## Filtrando para resolver la primera actividad
df_filtrado = df_tri_anio_selec[["PONDERA","CH04", "CH06"]].copy()

rango_anios = range(0,101,10)
etiquetas =  [f"{i}-{i+9}" for i in rango_anios[:-1]] 

## Convirtiendo edades en enteros y creando una nueva columna "grupos_edad" que clasifique a las edades
df_filtrado["CH06"] = pd.to_numeric(df_filtrado["CH06"], errors="coerce")
df_filtrado["grupos_edad"] = pd.cut(df_filtrado["CH06"], bins=rango_anios , labels=etiquetas)

## Convirtiendo los valores de sexo en Strings legibles
df_filtrado["CH04"] = df_filtrado["CH04"].apply(lambda x: "Masculino" if x == 1 else "Femenino")

df_filtrado = df_filtrado.groupby(["CH04","grupos_edad"])["PONDERA"].sum().reset_index()

## Separando un df por Hombres y Mujeres
df_pivot = df_filtrado.pivot(index="grupos_edad",columns="CH04",values="PONDERA")

## Creando el grafico y mostrandolo 

st.bar_chart(df_pivot, stack=False)

# ACTIV 1.3.2

st.header("Promedio de edades para los aglomerados del ultimo archivo ingresado")

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

st.header("Evolucion del Cociente de activos e inactivos por aglomerado")
aglo_seleccionado = st.selectbox("Elija un aglomerado",options= aglomerados)

df_activos = df[(df["AGLOMERADO"] == aglo_seleccionado) & (df["CH06"].between(15,64,inclusive="both")) ][["ANO4","TRIMESTRE","PONDERA"]].copy()
df_inactivos = df[(df["AGLOMERADO"] == aglo_seleccionado) & ( ~df["CH06"].between(15,64,inclusive="both")) ][["ANO4","TRIMESTRE","PONDERA"]].copy()

df_activos = df_activos.groupby(["ANO4","TRIMESTRE"]).sum("PONDERA").reset_index()
df_inactivos = df_inactivos.groupby(["ANO4","TRIMESTRE"]).sum("PONDERA").reset_index()

df_activos["grupo"] = "activos"
df_inactivos["grupo"] = "inactivos"

df_union = pd.concat([df_inactivos, df_activos])

df_union['periodo'] = df_union['ANO4'].astype(str) + 'T' + df_union['TRIMESTRE'].astype(str)

df_union = df_union.pivot(index="periodo",columns="grupo",values="PONDERA")

df_union["cociente"] = (df_union["inactivos"] / df_union["activos"] * 100).round(2)

st.table(df_union)
st.bar_chart(df_union[["activos","inactivos"]],stack=False)

# ACTIV 1.3.4

st.header("Evolucion de la edad media ")

df_edad = df[["ANO4","PONDERA","TRIMESTRE","CH06"]].copy()

df_edad['periodo'] = df_edad['ANO4'].astype(str) + 'T' + df_edad['TRIMESTRE'].astype(str)

df_edad = df_edad.groupby(["ANO4","CH06","TRIMESTRE","periodo"]).sum("PONDERA")
df_edad= df_edad.reset_index()

df_edad = df_edad.pivot(index="CH06", columns="periodo",values="PONDERA")

df_edad.index.name = 'edad'

# Calculamos la media ponderada de la edad por periodo
media_edad_ponderada = ((df_edad.mul(df_edad.index, axis=0)).sum() / df_edad.sum() ).round(2)

media_edad_ponderada_df = media_edad_ponderada.to_frame(name='media_edad')

st.dataframe(media_edad_ponderada_df)
st.line_chart(media_edad_ponderada_df)

datos = []
for columna in df_edad.columns: 
    serie = df_edad[columna].dropna()
    datos.append({"periodo" : columna , "mediana" : serie.index.to_series().median()})
    
df_nuevo = pd.DataFrame(datos)
df_nuevo = df_nuevo.set_index("periodo")

st.header("Mediana de las edades")
st.dataframe(df_nuevo)