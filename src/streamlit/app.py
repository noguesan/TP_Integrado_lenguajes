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
            st.success(" Datos actualizados correctamente.")  # Mensaje de éxito

    # Variables para almacenar los datos cargados
    datos_ind = None  # Datos de individuos
    datos_hog = None  # Datos de hogares

    # Intentar cargar el archivo de datos de individuos
    try:
        with open("data/clean/usu_clean_individual.csv", mode="r", encoding="utf-8") as archivo_ind:
            lector_ind = csv.DictReader(archivo_ind)  # Leer el archivo como un diccionario
            datos_ind = [fila for fila in lector_ind]  # Convertir las filas en una lista
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de individuos: {e}")  # Mostrar error si ocurre

    # Intentar cargar el archivo de datos de hogares
    try:
        with open("data/clean/usu_clean_hogar.csv", mode="r", encoding="utf-8") as archivo_hog:
            lector_hog = csv.DictReader(archivo_hog)  # Leer el archivo como un diccionario
            datos_hog = [fila for fila in lector_hog]  # Convertir las filas en una lista
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de hogares: {e}")  # Mostrar error si ocurre

    # Procesar datos de individuos si existen
    if datos_ind:
        try:
            # Extraer los años y trimestres de los datos
            anios = [int(f["ANO4"]) for f in datos_ind if f.get("ANO4")]
            trimestres = [int(f["TRIMESTRE"]) for f in datos_ind if f.get("TRIMESTRE")]

            # Determinar el rango de años y trimestres
            anio_min = min(anios)
            anio_max = max(anios)
            trim_min = min([int(f["TRIMESTRE"]) for f in datos_ind if int(f["ANO4"]) == anio_min])
            trim_max = max([int(f["TRIMESTRE"]) for f in datos_ind if int(f["ANO4"]) == anio_max])

            # Mostrar información sobre el rango de datos
            st.info(f" Datos de individuos desde {trim_min:02d}/{anio_min} hasta {trim_max:02d}/{anio_max}.")
        except Exception as e:
            st.error(f"No se pudo analizar los datos de individuos: {e}")  # Mostrar error si ocurre
    else:
        st.warning(" No se encontraron datos de individuos o el archivo está vacío.")  # Advertencia si no hay datos

    # Procesar datos de hogares si existen
    if datos_hog:
        try:
            # Extraer los años y trimestres de los datos
            anios = [int(f["ANO4"]) for f in datos_hog if f.get("ANO4")]
            trimestres = [int(f["TRIMESTRE"]) for f in datos_hog if f.get("TRIMESTRE")]

            # Determinar el rango de años y trimestres
            anio_min = min(anios)
            anio_max = max(anios)
            trim_min = min([int(f["TRIMESTRE"]) for f in datos_hog if int(f["ANO4"]) == anio_min])
            trim_max = max([int(f["TRIMESTRE"]) for f in datos_hog if int(f["ANO4"]) == anio_max])

            # Mostrar información sobre el rango de datos
            st.info(f" Datos de hogares desde {trim_min:02d}/{anio_min} hasta {trim_max:02d}/{anio_max}.")
        except Exception as e:
            st.error(f"No se pudo analizar los datos de hogares: {e}")  # Mostrar error si ocurre
    else:
        st.warning(" No se encontraron datos de hogares o el archivo está vacío.")  # Advertencia si no hay datos