import streamlit as st
import csv

st.set_page_config(page_title="Explorador EPH", layout="centered")
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Elegí una sección:", ["Inicio", "Carga de datos"])

ruta_archivo = "data/clean/usu_clean_individual.csv"

def cargar_datos_csv():
    datos = []
    try:
        with open("data/clean/usu_clean_individual.csv", "r", encoding="utf-8") as archivo:
            datos = list(csv.DictReader(archivo))
    except:
        st.error(" No se pudo cargar el archivo.")
    return datos


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
        datos = cargar_datos_csv()
        if datos:
            st.success(" Datos actualizados correctamente.")
    else:
        datos = cargar_datos_csv()

    if datos:
        try:
            anios = [int(fila["ANO4"]) for fila in datos if fila.get("ANO4")]
            trimestres = [int(fila["TRIMESTRE"]) for fila in datos if fila.get("TRIMESTRE")]

            anio_min = min(anios)
            anio_max = max(anios)

            trim_min = min([int(fila["TRIMESTRE"]) for fila in datos if int(fila["ANO4"]) == anio_min])
            trim_max = max([int(fila["TRIMESTRE"]) for fila in datos if int(fila["ANO4"]) == anio_max])

            st.info(f" El sistema contiene información desde el {trim_min:02d}/{anio_min} hasta el {trim_max:02d}/{anio_max}.")
        except Exception as e:
            st.error(f" No se pudo analizar el contenido del archivo: {e}")
    else:
        st.warning(" No se encontraron datos o el archivo está vacío.")