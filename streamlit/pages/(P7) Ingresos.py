import streamlit as st
# import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.constantes import DATA_CLEAN_PATH, PARENT_PATH
from src.utils.funciones import convertir_en_fecha
from src.utils.Filtros_Streamlit import mostrar_sidebar_con_filtros
import pandas as pd 
import matplotlib.pyplot as plt


st.title("1.7 (P7) Ingresos")

st.header("Datos y estadisticas sobre el ingreso ")
st.subheader("Personas dentro de la pobreza, indigencia, no pobreza y valores desconocidos")
# Abrir el archivo y seleccionar años y trimestres 


# ----------------------------------------
# # Abrir el archivo y seleccionar años y trimestres 

archivo = DATA_CLEAN_PATH / "usu_clean_hogar.csv"
# df = pd.read_csv(archivo, delimiter=",", low_memory=False)

# anios = df["ANO4"].unique()
# anio_selec = st.selectbox("seleccione el año a buscar", options= anios)
# anio_selec_df = df[df["ANO4"] == anio_selec]

# trimestres = anio_selec_df["TRIMESTRE"].unique()
# trim_selec = st.selectbox("seleccione el trimestre a buscar", options= trimestres)

# selec_df = anio_selec_df[anio_selec_df["TRIMESTRE"] == trim_selec] 
# =====================================
# Filtrado de la base de datos para los preprarar los dataframe necesarios
df,selec_df,df_filtrado_aglomerado ,df_tri_anio_selec = mostrar_sidebar_con_filtros(archivo)

# =====================================
# --------------------------------------


# Filtrar por hogares de 4 integrantes 

hogares_4_df = selec_df[["ANO4","TRIMESTRE","ITF","PONDERA"]][selec_df["IX_TOT"] >= 4].copy()

# abriendo el archivo de la canasta basica (cb = canasta basica), y convirtiendo las fechas de ambos 

ruta_cb = PARENT_PATH / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv"
cb = pd.read_csv(ruta_cb,delimiter=",")

# =====================================
anio_selec = selec_df['ANO4'].iloc[0]
trim_selec = selec_df['TRIMESTRE'].iloc[0]
# =====================================
fechas_selec = convertir_en_fecha(anio_selec,trim_selec)

cb["indice_tiempo"] = pd.to_datetime(cb["indice_tiempo"])

for elem in fechas_selec:
    pd.to_datetime(fechas_selec)

cb_selec = cb[cb["indice_tiempo"].between(fechas_selec[0], fechas_selec[1])]

promedios = { 
    "prom_pobreza" : ((cb_selec["linea_pobreza"].sum()) / 3 ).round(2),
    "prom_indigencia" : ((cb_selec["linea_indigencia"].sum()) / 3).round(2)
}

cb_selec_prom = pd.DataFrame([promedios])

def comprobar_promedio(valor): 
    if pd.isna(valor) or valor == 0: 
        return "Desconocido"
    elif valor <= cb_selec_prom["prom_indigencia"].iloc[0]:
        return "Indigencia"
    elif valor <= cb_selec_prom["prom_pobreza"].iloc[0]:
        return "Pobreza"
    else: 
        return "Clase media"
    
hogares_4_df["estado"] = hogares_4_df["ITF"].apply(comprobar_promedio)
hogares_s_desc = hogares_4_df[hogares_4_df["estado"] != "Desconocido"]

hogares_final = hogares_4_df[["estado","PONDERA"]].groupby(["estado"]).sum("PONDERA")
hogares_s_desc = hogares_s_desc[["estado","PONDERA"]].groupby(["estado"]).sum("PONDERA")

hogares_final = hogares_final.reset_index()
hogares_s_desc = hogares_s_desc.reset_index()

fig, ax = plt.subplots()
ax.pie(
    hogares_final["PONDERA"],
    labels=hogares_final["estado"],
    autopct="%1.1f%%",
    startangle=90
)
ax.axis("equal") 
st.pyplot(fig)
st.write("valores desconocidos son valores que eran 0 o nulos ")
st.header("Descartando a los valores desconocidos")


fig, ax = plt.subplots()
ax.pie(
    hogares_s_desc["PONDERA"],
    labels=hogares_s_desc["estado"],
    autopct="%1.1f%%",
    startangle=90
)
ax.axis("equal") 

st.pyplot(fig)