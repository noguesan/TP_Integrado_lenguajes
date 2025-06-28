import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.constantes import DATA_CLEAN_PATH

st.title("1.4 (P4) Características de la vivienda")

# --- Cargar datos de hogares usando pandas y DATA_CLEAN_PATH ---
archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_hogar.csv"

# # =====================================
from src.utils.Filtros_Streamlit import mostrar_sidebar_con_filtros

# Filtrado de la base de datos para los preprarar los dataframe necesarios
df,df_filtrado_aglo,df_filtrado_Solo_aglomerado ,df_filtrado = mostrar_sidebar_con_filtros(archivo_clean_path)

# =====================================

# 1.4.1 Cantidad total de viviendas 
st.subheader("Cantidad total de viviendas ")
if 'PONDERA' in df_filtrado_aglo.columns:
    total_viviendas = df_filtrado_aglo['PONDERA'].sum()
    st.write(f"Total de viviendas: {int(total_viviendas)}")
else:
    st.info("No se encontró la columna PONDERA en el archivo.")

# 1.4.2 Pie chart con proporción de viviendas según tipo 
st.subheader("Proporción de viviendas según tipo ")
if 'IV1' in df_filtrado_aglo.columns and 'PONDERA' in df_filtrado_aglo.columns:
    tipos_dict = {
        1: "Casa",
        2: "Departamento",
        3: "Pieza de inquilinato",
        4: "Pieza en hotel/pensión",
        5: "Local no construido para habitación"
    }
    tipo_counts = df_filtrado_aglo.groupby('IV1')['PONDERA'].sum()
    tipo_counts.index = tipo_counts.index.astype(float).astype(int).map(tipos_dict)
    fig1, ax1 = plt.subplots()
    explode = [0.05] * len(tipo_counts)
    wedges, texts, autotexts = ax1.pie(
        tipo_counts,
        labels=None,  # No mostrar etiquetas en el gráfico
        autopct='%1.1f%%',
        explode=explode,
        startangle=90,
        textprops={'fontsize': 10}
    )
    ax1.set_title("Proporción de viviendas según tipo")
    ax1.axis('equal')
    # Agregar leyenda afuera del gráfico
    ax1.legend(wedges, tipo_counts.index, title="Tipo de vivienda", loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig1)
else:
    st.info("No se encontró la columna IV1 o PONDERA en el archivo.")

# --- Diccionario de nombres de aglomerados ---
aglomerado_dict = {
    "02": "Gran La Plata",
    "03": "Bahía Blanca - Cerri",
    "04": "Gran Rosario",
    "05": "Gran Santa Fé",
    "06": "Gran Paraná",
    "07": "Posadas",
    "08": "Gran Resistencia",
    "09": "Comodoro Rivadavia - Rada Tilly",
    "10": "Gran Mendoza",
    "12": "Corrientes",
    "13": "Gran Córdoba",
    "14": "Concordia",
    "15": "Formosa",
    "17": "Neuquén - Plottier",
    "18": "Santiago del Estero - La Banda",
    "19": "Jujuy - Palpalá",
    "20": "Río Gallegos",
    "22": "Gran Catamarca",
    "23": "Gran Salta",
    "25": "La Rioja",
    "26": "Gran San Luis",
    "27": "Gran San Juan",
    "29": "Gran Tucumán - Tafí Viejo",
    "30": "Santa Rosa - Toay",
    "31": "Ushuaia - Río Grande",
    "32": "Ciudad Autonoma de Buenos Aires",
    "33": "Partidos del GBA",
    "34": "Mar del Plata",
    "36": "Río Cuarto",
    "38": "San Nicolás - Villa Constitución",
    "91": "Rawson - Trelew",
    "93": "Viedma - Carmen de Patagones"
}

# 1.4.3 Material predominante en pisos por aglomerado
st.subheader("Material predominante en pisos por aglomerado ")
if 'IV3' in df_filtrado.columns and 'PONDERA' in df_filtrado.columns:
    pisos_dict = {
        1: "Mosaico/Baldosa/Madera/Cerámica/Alfombra",
        2: "Cemento/Ladrillo fijo",
        3: "Ladrillo suelto/Tierra"
    }
    def moda_ponderada(x):
        return x.groupby(x).apply(lambda y: df_filtrado.loc[y.index, 'PONDERA'].sum()).idxmax()
    materiales_por_aglo = df_filtrado.groupby('AGLOMERADO')['IV3'].agg(moda_ponderada)
    materiales_por_aglo = materiales_por_aglo.map(pisos_dict)
    idx = materiales_por_aglo.index.astype(str)
    nombres = idx.map(aglomerado_dict)
    materiales_por_aglo.index = nombres.where(nombres.notna(), idx)
    st.write(materiales_por_aglo)
else:
    st.info("No se encontró la columna IV3 o PONDERA en el archivo.")

# 1.4.4 Proporción de viviendas con baño dentro del hogar por aglomerado
st.subheader("Proporción de viviendas con baño dentro del hogar por aglomerado")
if 'IV8' in df_filtrado.columns and 'PONDERA' in df_filtrado.columns:
    def prop_ponderada(x):
        pondera_total = df_filtrado.loc[x.index, 'PONDERA'].sum()
        pondera_con_banio = df_filtrado.loc[x.index][x == 1]['PONDERA'].sum()
        return (pondera_con_banio / pondera_total) * 100 if pondera_total > 0 else 0
    proporcion_banio = df_filtrado.groupby('AGLOMERADO')['IV8'].agg(prop_ponderada)
    idx = proporcion_banio.index.astype(str)
    nombres = idx.map(aglomerado_dict)
    proporcion_banio.index = nombres.where(nombres.notna(), idx)
    st.write(proporcion_banio)
else:
    st.info("No se encontró la columna IV8 en el archivo.")

# 1.4.6 Cantidad de viviendas en villa de emergencia por aglomerado 
st.subheader("Viviendas en villa de emergencia por aglomerado")
if 'IV12_3' in df_filtrado.columns and 'PONDERA' in df_filtrado.columns:
    villas_por_aglo = df_filtrado[df_filtrado['IV12_3'] == 1].groupby('AGLOMERADO')['PONDERA'].sum()
    idx = villas_por_aglo.index.astype(str)
    nombres = idx.map(aglomerado_dict)
    villas_por_aglo.index = nombres.where(nombres.notna(), idx)
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    villas_por_aglo.plot(kind='bar', ax=ax5)
    ax5.set_ylabel("Cantidad de viviendas en villa de emergencia")
    ax5.set_xlabel("Aglomerado")
    ax5.set_title("Viviendas en villa de emergencia por aglomerado")
    st.pyplot(fig5)
    st.write(villas_por_aglo)
else:
    st.info("No se encontró la columna IV12_3 o PONDERA en el archivo.")

# 1.4.7 Porcentaje de viviendas por CONDICION_DE_HABITABILIDAD por aglomerado
st.subheader("Porcentaje de viviendas por CONDICION_DE_HABITABILIDAD por aglomerado")
if 'CONDICION_DE_HABITABILIDAD' in df_filtrado.columns and 'PONDERA' in df_filtrado.columns:
    cond_counts = df_filtrado.pivot_table(
        index='AGLOMERADO',
        columns='CONDICION_DE_HABITABILIDAD',
        values='PONDERA',
        aggfunc='sum',
        fill_value=0
    ) 
    idx = cond_counts.index.astype(str)
    nombres = idx.map(aglomerado_dict)
    cond_counts.index = nombres.where(nombres.notna(), idx)
    cond_perc = cond_counts.div(cond_counts.sum(axis=1), axis=0) * 100
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    cond_perc.plot(kind='bar', stacked=True, ax=ax6)
    ax6.set_ylabel("Porcentaje (%)")
    ax6.set_xlabel("Aglomerado")
    ax6.set_title("Porcentaje de viviendas por condición de habitabilidad")
    st.pyplot(fig6)
    st.dataframe(cond_perc)
else:
    st.info("No se encontró la columna CONDICION_DE_HABITABILIDAD o PONDERA en el archivo.")

# Botón para exportar resultados a CSV
if st.button("Exportar resultados a CSV"):
    df_filtrado.to_csv("resultados_filtrados.csv", index=False)
    st.success("Archivo exportado como resultados_filtrados.csv")