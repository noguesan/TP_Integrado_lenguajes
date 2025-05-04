import streamlit as st
import os
import re

# Configuración básica de la app
st.set_page_config(page_title="EPH App", layout="centered")

# Sidebar con las páginas
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Elegí una sección:", ["Inicio", "Carga de datos", "Busqueda", "Visualizacion"])

# Página 1 - Inicio
if pagina == "Inicio":
    st.title("Explorador de la Encuesta Permanente de Hogares (EPH)")

    st.markdown("""
    Bienvenidos a esta aplicación para visualizar datos de la **EPH**.

    La Encuesta Permanente de Hogares (EPH) es una encuesta del INDEC que recopila datos sobre:
    - Las condiciones de vida de la población.
    - Características de los hogares y de las personas: edad, educación, ingresos, empleo, etc.

    En esta app vamos a poder explorar esa información una vez que carguemos los datos.
    """)
  
        