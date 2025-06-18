# =======================================================
# Librerias
# =======================================================

import streamlit as st
import pandas as pd
import sys
import os
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# =======================================================
# Preparaacion de datos
# ======================================================= 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.constantes import DATA_CLEAN_PATH
import src.utils.funciones_page_ActividadYEmpleo as fe
from src.utils.Filtros_Streamlit import mostrar_sidebar_con_filtros

# path de base de datos
archivo_personas_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"
# Filtrado de la base de datos para los preprarar los dataframe necesarios
df_personas,df_personas_filtrado,df_filtrado_aglomerado ,df_filtrado_Ano4Trimestre = mostrar_sidebar_con_filtros(archivo_personas_path)

# =======================================================
# Contenido de la pagina
# ======================================================= 

st.title("1.5 (P5) Actividad y empleo")
st.write("""
En esta sección se visualizará información relacionada a la actividad y empleo según la EPH.
""")

# Incisos 
# =======================================================
# --- 1.5.1 Cantidad de desocupados por nivel educativo ---
st.subheader("1.5.1 Desocupados por nivel educativo")
# Calcular cantidad de desocupados según estudios alcanzados
tabla_EstadoNivel_ED = fe.resumen_nivel_educativo(df_personas_filtrado)
# Aplicar resaltado a la columna 'Desocupados'
tabla_EstadoNivel_ED_resaltada = fe.resaltar_columnas(tabla_EstadoNivel_ED, 'Desocupado')
# Imprimir tabla
st.subheader("Resumen por Nivel Educativo y Condición de Actividad")
st.dataframe(tabla_EstadoNivel_ED_resaltada, use_container_width=True)

# Crear gráfico
df_para_graficar = tabla_EstadoNivel_ED.reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(
    df_para_graficar['NIVEL_ED_DESC'], 
    df_para_graficar['Desocupado'], 
    color='orange'
)
ax.set_xlabel('Cantidad de desocupados')
ax.set_title('Desocupados por nivel educativo')
plt.tight_layout()

# Mostrar en Streamlit
st.pyplot(fig)

# =======================================================
# --- 1.5.2 Evolución de la tasa de desempleo y 1.5.3 Evolución de la tasa de empleo ---
st.subheader("1.5.2 Evolución de la tasa de desempleo y 1.5.3 Evolución de la tasa de empleo")
# Calcular evolución de la tasa de desempleo y empleo
tabla_tasas = fe.evolucion_tasas(df_personas)
# Aplicar resaltado a la columna 'Desocupados'
tabla_tasas_resaltada = fe.resaltar_columnas(tabla_tasas, ['Tasa de Desempleo (%)', 'Tasa de Empleo (%)'])
# Imprimir tabla
st.dataframe(tabla_tasas_resaltada, use_container_width=True)

# Grafico:
# Crear columna de periodo
#tabla_tasas['Periodo'] = + 'Año: ' + tabla_tasas['ANO4'].astype(str) + ' Trimestre: ' + tabla_tasas['TRIMESTRE'].astype(str)
tabla_tasas['Periodo'] = '!=|A' +tabla_tasas['ANO4'].astype(str) + ' T' + tabla_tasas['TRIMESTRE'].astype(str)

fig1, ax1 = plt.subplots()
ax1.plot(tabla_tasas['Periodo'], tabla_tasas['Tasa de Empleo (%)'], marker='o', color='green')
ax1.set_title('Evolución de la Tasa de Empleo')
ax1.set_xlabel('Periodo')
ax1.set_ylabel('Tasa de Empleo (%)')
ax1.grid(True)
st.pyplot(fig1)

# =======================================================
# --- 1.5.4 Porcentaje de empleo estatal, privado y otro por aglomerado ---
st.subheader("1.5.4 Porcentaje de empleo estatal, privado y otro por aglomerado")
# Aquí va el código para calcular y mostrar los porcentajes por aglomerado
tabla_empleoEstatalPrivado = fe.obtener_tabla_empleo_con_nombresAglomeardo(df_filtrado_Ano4Trimestre)
st.dataframe(tabla_empleoEstatalPrivado, use_container_width=True)

def graficar_empleo_por_aglomerado(df):
    """
    Genera un gráfico de barras apiladas con % Estatal, % Privado y % Otro para cada aglomerado.
    
    Parámetros:
    - df: DataFrame que contiene las columnas:
        - 'nombre_aglomerado'
        - '% Estatal'
        - '% Privado'
        - '% Otro'
    """

    # Ordenar por Total Ocupados si existe la columna
    if 'Total Ocupados' in df.columns:
        df = df.sort_values(by='Total Ocupados', ascending=False)

    # Etiquetas (eje X) y valores (alturas)
    labels = df['nombre_aglomerado']
    estatal = df['% Estatal']
    privado = df['% Privado']
    otro = df['% Otro']

    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar barras apiladas
    ax.bar(labels, estatal, label='% Estatal', color='#ffcc99')
    ax.bar(labels, privado, bottom=estatal, label='% Privado', color='#99ccff')
    ax.bar(labels, otro, bottom=estatal + privado, label='% Otro', color='#cccccc')

    # Estética
    ax.set_ylabel('% del total de ocupados')
    ax.set_title('Distribución porcentual del empleo por aglomerado')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()

    # Mostrar en Streamlit
    st.pyplot(fig)

graficar_empleo_por_aglomerado(tabla_empleoEstatalPrivado)

# =======================================================
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
## ** No funciona si esta el paso "3. Mostrar mapas" activado

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