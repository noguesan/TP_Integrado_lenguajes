import streamlit as st
import csv
import pandas as pd
import sys
import os
import folium
from streamlit_folium import st_folium

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.constantes import DATA_CLEAN_PATH
import src.utils.funciones_page_ActividadYEmpleo as fe

st.title("1.5 (P5) Actividad y empleo")
st.write("""
En esta sección se visualizará información relacionada a la actividad y empleo según la EPH.
""")

# --- Cargar datos de personas ---
archivo_personas_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"

try:
    df_personas = pd.read_csv(archivo_personas_path, encoding="utf-8", low_memory=False)
    st.success(f"Archivo cargado correctamente. Filas: {len(df_personas)}")
except Exception as e:
    st.error(f"No se pudo cargar el archivo: {e}")

# --- Filtros ---
## enlistar valores unicos en el dataFrame
anios = sorted(df_personas["ANO4"].dropna().unique().tolist())
trimestres = sorted(df_personas["TRIMESTRE"].dropna().unique().tolist())
aglomerados = sorted(df_personas["AGLOMERADO"].dropna().unique().tolist())

## SelectBox con las opciones
anio_seleccionado = st.selectbox("Seleccione un año", options=anios)
trimestre_seleccionado = st.selectbox("Seleccione un trimestre", options=trimestres)
aglomerado_seleccionado = st.selectbox("Seleccione un aglomerado (opcional)", options=["Todos"] + aglomerados)

# Filtrar la base
df_personas_filtrado = fe.filtrar_dataframe(df_personas, anio_seleccionado, trimestre_seleccionado, aglomerado_seleccionado)
#df_personas_filtrado_anoTrimestre = fe.filtrar_dataframe(df_personas, anio_seleccionado, trimestre_seleccionado, "Todos")
# df_filtrado_Aglomerado = df[(df['AGLOMERADO'] == 2)].copy()
# df_filtrado_AglomeradoAnoTrim = df[(df['ANO4'] == 2024) & (df['TRIMESTRE'] == 1) & (df['AGLOMERADO'] == 2)].copy()

################# 
# --- 1.5.1 Cantidad de desocupados por nivel educativo ---
st.subheader("1.5.1 Desocupados por nivel educativo")
# Aquí va el código para filtrar y mostrar la cantidad de desocupados según estudios alcanzados
tabla_EstadoNivel_ED = fe.resumen_nivel_educativo(df_personas_filtrado)
st.subheader("Resumen por Nivel Educativo y Condición de Actividad")
st.dataframe(tabla_EstadoNivel_ED, use_container_width=True)

# --- 1.5.2 Evolución de la tasa de desempleo y 1.5.3 Evolución de la tasa de empleo ---
st.subheader("1.5.2 Evolución de la tasa de desempleo y 1.5.3 Evolución de la tasa de empleo")
# Aquí va el código para calcular y graficar la evolución de la tasa de desempleo y empleo
tabla_tasas = fe.evolucion_tasas(df_personas)
st.dataframe(tabla_tasas, use_container_width=True)

# --- 1.5.4 Porcentaje de empleo estatal, privado y otro por aglomerado ---
st.subheader("1.5.4 Porcentaje de empleo estatal, privado y otro por aglomerado")
# Aquí va el código para calcular y mostrar los porcentajes por aglomerado
tabla_empleoEstatalPrivado = fe.calcular_empleo_por_aglomerado(df_personas)
st.dataframe(tabla_empleoEstatalPrivado, use_container_width=True)

# --- 1.5.5 Mapa de evolución de tasas por aglomerado ---
st.subheader("1.5.5 Mapa de evolución de tasas por aglomerado")

## Se divide en la siguientes  partes:
## 1 porcentajes y mostrar el mapa con puntos verdes/rojos según corresponda
## 2. Agregar coordenadas y nombres de aglomerados
## 3. Mostrar mapas
## 4. Botoneras para seleccionar los mapas
## ** Hay partes solo comentadas ya que sirven para ver que todo funcione adecuamente pero no se desea mostrarlas en la pagina


## 1 porcentajes y mostrar el mapa con puntos verdes/rojos según corresponda
df_comparacion_empleo, df_comparacion_desempleo = fe.evolucion_tasas_aglomerados(df_personas)
st.subheader("Comparacion tasa de EMPLEO")
st.dataframe(df_comparacion_empleo, use_container_width=True)
st.subheader("Comparacion tasa de DESEMPLEO")
st.dataframe(df_comparacion_desempleo, use_container_width=True)


## 2. Agregar coordenadas y nombres de aglomerados
df_comparacion_empleo, df_comparacion_desempleo = fe.agregar_coordenadas_a_tasas(
    df_comparacion_empleo,
    df_comparacion_desempleo
)

# # Mostrar resultados en Streamlit
# st.subheader("Comparación tasa de EMPLEO con coordandas")
# st.dataframe(df_comparacion_empleo, use_container_width=True)

# st.subheader("Comparación tasa de DESEMPLEO con coordandas")
# st.dataframe(df_comparacion_desempleo, use_container_width=True)


# ## 3. Mostrar mapas
# # Mostrar el mapa de empleo
# st.subheader("Mapa de evolución de la tasa de EMPLEO")
# mapa_empleo = fe.generar_mapa(df_comparacion_empleo)
# st_folium(mapa_empleo, width=700, height=400)

# # Mostrar el mapa de desempleo
# st.subheader("Mapa de evolución de la tasa de DESEMPLEO")
# mapa_desempleo = fe.generar_mapa(df_comparacion_desempleo, color_positivo='green', color_negativo='red')
# st_folium(mapa_desempleo, width=700, height=500)




## 4. Botoneras para seleccionar los mapas
## ** No funciona si esta el pasi 3 activado

st.subheader("Mapas de evolución de tasas")

# Selector para elegir qué mapa mostrar
opcion_mapa = st.radio(
    "Seleccioná qué mapa querés visualizar:",
    options=["Tasa de EMPLEO", "Tasa de DESEMPLEO"],
    horizontal=True
)

if opcion_mapa == "Tasa de EMPLEO":
    mapa_empleo = fe.generar_mapa(df_comparacion_empleo, color_positivo='green', color_negativo='red')
    st_folium(mapa_empleo, width=700, height=400)

elif opcion_mapa == "Tasa de DESEMPLEO":
    mapa_desempleo = fe.generar_mapa(df_comparacion_desempleo, color_positivo='red', color_negativo='green')
    st_folium(mapa_desempleo, width=700, height=500)