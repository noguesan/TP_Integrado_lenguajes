import streamlit as st
import pandas as pd

# Configuración básica de la app
st.set_page_config(page_title="EPH App", layout="centered")

# Sidebar con las páginas
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Elegí una sección:", ["Inicio", "Carga de datos", "Busqueda", "Visualizacion"])
ruta_archivo = "usu_clean_individual.csv"

def cargar_datos():
    try:
        return pd.read_csv(ruta_archivo)
    except FileNotFoundError:
        st.error("El archivo no se encontró. Verifica que esté en la carpeta correcta.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error("El archivo está vacío o tiene un formato incorrecto.")
        return pd.DataFrame()

# Página 1 (Inicio))
if pagina == "Inicio":
    st.title("Explorador de la Encuesta Permanente de Hogares (EPH)")

    st.markdown("""
    Bienvenidos a esta aplicación para visualizar datos de la **EPH**.

    La Encuesta Permanente de Hogares (EPH) es una encuesta del INDEC que recopila datos sobre:
    - Las condiciones de vida de la población.
    - Características de los hogares y de las personas: edad, educación, ingresos, empleo, etc.

    En esta app vamos a poder explorar esa información una vez que carguemos los datos.
    """)
# Página 2 (Carga)
elif pagina == "Carga de datos":
    st.title("Carga de datos")
    try:
        if st.button("Actualizar Dataset"):
            df = cargar_datos()
            if not df.empty:
                st.success("Datos actualizados correctamente.")
        else:
            df = cargar_datos()

        if not df.empty and "ANO4" in df.columns and "TRIMESTRE" in df.columns:
            min_anio = df["ANO4"].min()
            max_anio = df["ANO4"].max()
            min_trim = df[df["ANO4"] == min_anio]["TRIMESTRE"].min()
            max_trim = df[df["ANO4"] == max_anio]["TRIMESTRE"].max()
            st.info(f"El sistema contiene información desde el {min_trim:02d}/{min_anio} hasta el {max_trim:02d}/{max_anio}.")
        elif not df.empty:
            st.warning("No se encontraron columnas de año y trimestre en el dataset.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")