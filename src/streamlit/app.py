import streamlit as st
import sys 
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.procesamientos.pindividuos import actualizar_individuos
from src.procesamientos.phogares import actualizar_hogar

def actualizar_todo():
    actualizar_hogar()
    actualizar_individuos()
    return True


st.set_page_config(page_title="Explorador EPH", layout="centered")
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Elegí una sección:", ["Inicio", "Carga de datos", "Buscar", "Visualizacion"])

if pagina == "Inicio":
    st.title(" Explorador de Datos EPH")

    st.markdown("""
    Bienvenido a esta aplicación interactiva para explorar los datos de la **Encuesta Permanente de Hogares (EPH)**.

    La EPH es una encuesta realizada por el INDEC que contiene información sobre:
    - Condiciones de vida.
    - Situación laboral.
    - Ingresos, educación, edad y otras características sociodemográficas.

    ---
    ### ¿Cómo usar esta aplicación?
    1. Ingresá a la sección **"Carga de datos"** para conocer el rango de información disponible.
    2. Si incorporaste nuevos archivos, presioná **"Actualizar Dataset"** para refrescar la base.
    """)
elif pagina == "Carga de datos":
    st.title(" Carga de Datos de EPH")

    if st.button(" Actualizar Dataset"):
        datos = actualizar_todo()  
        if datos:
            st.success(" Datos actualizados correctamente.")
    
    datos_ind = None
    datos_hog = None

    try:
        with open("data/clean/usu_clean_individual.csv", mode="r", encoding="utf-8") as archivo_ind:
            lector_ind = csv.DictReader(archivo_ind)
            datos_ind = [fila for fila in lector_ind]
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de individuos: {e}")

    try:
        with open("data/clean/usu_clean_hogar.csv", mode="r", encoding="utf-8") as archivo_hog:
            lector_hog = csv.DictReader(archivo_hog)
            datos_hog = [fila for fila in lector_hog]
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de hogares: {e}")
    
    
    # Procesar datos si existen
    if datos_ind:
        try:
            anios = [int(f["ANO4"]) for f in datos_ind if f.get("ANO4")]
            trimestres = [int(f["TRIMESTRE"]) for f in datos_ind if f.get("TRIMESTRE")]

            anio_min = min(anios)
            anio_max = max(anios)
            trim_min = min([int(f["TRIMESTRE"]) for f in datos_ind if int(f["ANO4"]) == anio_min])
            trim_max = max([int(f["TRIMESTRE"]) for f in datos_ind if int(f["ANO4"]) == anio_max])

            st.info(f" Datos de individuos desde {trim_min:02d}/{anio_min} hasta {trim_max:02d}/{anio_max}.")
        except Exception as e:
            st.error(f"No se pudo analizar los datos de individuos: {e}")
    else:
        st.warning(" No se encontraron datos de individuos o el archivo está vacío.")

    if datos_hog:
        try:
            anios = [int(f["ANO4"]) for f in datos_hog if f.get("ANO4")]
            trimestres = [int(f["TRIMESTRE"]) for f in datos_hog if f.get("TRIMESTRE")]

            anio_min = min(anios)
            anio_max = max(anios)
            trim_min = min([int(f["TRIMESTRE"]) for f in datos_hog if int(f["ANO4"]) == anio_min])
            trim_max = max([int(f["TRIMESTRE"]) for f in datos_hog if int(f["ANO4"]) == anio_max])

            st.info(f" Datos de hogares desde {trim_min:02d}/{anio_min} hasta {trim_max:02d}/{anio_max}.")
        except Exception as e:
            st.error(f"No se pudo analizar los datos de hogares: {e}")
    else:
        st.warning(" No se encontraron datos de hogares o el archivo está vacío.")