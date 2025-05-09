import streamlit as st
import sys 
import os
import csv

# Agregar la ruta al sistema para importar módulos personalizados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importar funciones para actualizar datos de individuos y hogares
from src.procesamientos.pindividuos import actualizar_individuos
from src.procesamientos.phogares import actualizar_hogar

# Función para actualizar todos los datos
def actualizar_todo():
    actualizar_hogar()
    actualizar_individuos()
    return True

def cargar_datos_csv(path):
    try:
        with open(path, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return [fila for fila in lector]
    except Exception as e:
        st.error(f"No se pudo cargar el archivo {os.path.basename(path)}: {e}")
        return None

def mostrar_tiempo(datos, nombre_archivo):
    try:
        anios = [int(f["ANO4"]) for f in datos if f.get("ANO4")]
        anio_min = min(anios)
        anio_max = max(anios)

        trim_min = min(int(f["TRIMESTRE"]) for f in datos if int(f["ANO4"]) == anio_min)
        trim_max = max(int(f["TRIMESTRE"]) for f in datos if int(f["ANO4"]) == anio_max)

        st.info(f" Datos del archivo **{nombre_archivo}** desde {trim_min:02d}/{anio_min} hasta {trim_max:02d}/{anio_max}.")
    except Exception as e:
        st.error(f"No se pudo analizar los datos del archivo {nombre_archivo}: {e}")

st.set_page_config(page_title="Explorador EPH", layout="centered")

# Crear un menú lateral con opciones de navegación
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Elegí una sección:", ["Inicio", "Carga de datos", "Buscar", "Visualizacion"])

# Sección "Inicio" de la aplicación
if pagina == "Inicio":
    st.title(" Explorador de Datos EPH")

    # Descripción introductoria de la aplicación
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

# Sección "Carga de datos" de la aplicación
elif pagina == "Carga de datos":
    st.title(" Carga de Datos de EPH")  # Título principal de la sección

    # Botón para actualizar el dataset
    if st.button(" Actualizar Dataset"):
        datos = actualizar_todo()  # Llama a la función para actualizar los datos
        if datos:
            st.success(" Datos actualizados correctamente.")


    datos_ind = cargar_datos_csv("data/clean/usu_clean_individual.csv")
    datos_hog = cargar_datos_csv("data/clean/usu_clean_hogar.csv")
    
    if datos_ind:
        mostrar_tiempo(datos_ind, "individuos")
    else:
        st.warning("No se encontraron datos de individuos o el archivo está vacío.")

    # Procesar datos de hogares si existen
    if datos_hog:
        mostrar_tiempo(datos_hog, "hogares")
    else:
        st.warning("No se encontraron datos de hogares o el archivo está vacío.")
