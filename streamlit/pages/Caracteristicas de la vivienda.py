import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.constantes import DATA_CLEAN_PATH

st.title("Características de la vivienda")

# --- Cargar datos de hogares usando pandas y DATA_CLEAN_PATH ---
archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_hogar.csv"
df = pd.read_csv(archivo_clean_path, delimiter=",")

# --- Filtros de año y aglomerado ---
anios = sorted(df['ANO4'].astype(str).unique())
aglomerados = sorted(df['AGLOMERADO'].astype(str).unique())

anio_seleccionado = st.selectbox("Seleccione un año", options=["Todos"] + anios)
aglomerado_seleccionado = st.selectbox("Seleccione un aglomerado (opcional)", options=["Todos"] + aglomerados)

# --- Filtrado de datos según selección ---
df_filtrado = df.copy()
if anio_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['ANO4'].astype(str) == anio_seleccionado]
if aglomerado_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['AGLOMERADO'].astype(str) == aglomerado_seleccionado]

# 1.4.1 Cantidad total de viviendas
st.subheader("1.4.1 Cantidad total de viviendas")
st.write(f"Total de viviendas: {len(df_filtrado)}")

# 1.4.2 Pie chart con proporción de viviendas según tipo
st.subheader("1.4.2 Proporción de viviendas según tipo")
if 'IV2' in df_filtrado.columns:
    tipo_counts = df_filtrado['IV2'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(tipo_counts, labels=tipo_counts.index, autopct='%1.1f%%')
    st.pyplot(fig1)
else:
    st.info("No se encontró la columna IV2 (tipo de vivienda) en el archivo.")

# 1.4.3 Material predominante en pisos por aglomerado
st.subheader("1.4.3 Material predominante en pisos por aglomerado")
if 'IV3' in df_filtrado.columns:
    materiales_por_aglo = df_filtrado.groupby('AGLOMERADO')['IV3'].agg(lambda x: x.mode()[0] if not x.mode().empty else None)
    st.write(materiales_por_aglo)
else:
    st.info("No se encontró la columna IV3 (material de pisos) en el archivo.")

# 1.4.4 Proporción de viviendas con baño dentro del hogar por aglomerado
st.subheader("1.4.4 Proporción de viviendas con baño dentro del hogar")
if 'IV8' in df_filtrado.columns:
    proporcion_banio = df_filtrado.groupby('AGLOMERADO')['IV8'].apply(lambda x: (x == 1).mean() * 100)
    st.write(proporcion_banio)
else:
    st.info("No se encontró la columna IV8 (baño dentro del hogar) en el archivo.")

# 1.4.5 Evolución del régimen de tenencia para un aglomerado específico
st.subheader("1.4.5 Evolución del régimen de tenencia")
if aglomerado_seleccionado != "Todos" and 'IV10' in df_filtrado.columns:
    tenencia_counts = df_filtrado['IV10'].value_counts()
    st.bar_chart(tenencia_counts)
else:
    st.info("Seleccione un aglomerado y asegúrese de que la columna IV10 (régimen de tenencia) exista.")

# 1.4.6 Cantidad de viviendas en villa de emergencia por aglomerado
st.subheader("1.4.6 Viviendas en villa de emergencia por aglomerado")
if 'IV12_1' in df_filtrado.columns:
    villas_por_aglo = df_filtrado.groupby('AGLOMERADO')['IV12_1'].apply(lambda x: (x == 1).sum())
    st.write(villas_por_aglo)
else:
    st.info("No se encontró la columna IV12_1 (villa de emergencia) en el archivo.")

# 1.4.7 Porcentaje de viviendas por CONDICION_DE_HABITABILIDAD
st.subheader("1.4.7 Porcentaje de viviendas por CONDICION_DE_HABITABILIDAD")
if 'CONDICION_DE_HABITABILIDAD' in df_filtrado.columns:
    cond_counts = df_filtrado['CONDICION_DE_HABITABILIDAD'].value_counts(normalize=True) * 100
    st.bar_chart(cond_counts)
else:
    st.info("No se encontró la columna CONDICION_DE_HABITABILIDAD en el archivo.")

# Botón para exportar resultados a CSV
if st.button("Exportar resultados a CSV"):
    df_filtrado.to_csv("resultados_filtrados.csv", index=False)
    st.success("Archivo exportado como resultados_filtrados.csv")