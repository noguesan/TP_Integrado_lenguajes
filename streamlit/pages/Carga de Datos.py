import streamlit as st 
import sys 
import os
import csv 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.procesamientos.pindividuos import actualizar_individuos
from src.procesamientos.phogares import actualizar_hogar
from src.utils.funciones import  agrupar_por_anio_y_trimestre,obtener_fechas, analizar_archivos
from src.utils.constantes import DATA_CLEAN_PATH


def actualizar_todo(): 
    """
    Ejecuta la actualización de los datos de hogares e individuos.

    Returns:
        bool: True si la actualización se realizó correctamente.

    """
    try: 
        actualizar_hogar()
        actualizar_individuos()
        return True
    except:
        return False  
        

def mostrar_tiempo ():
    """
    Obtiene las fechas más reciente y más antigua de los datos individuales limpios.

    Returns:
        tuple: (mas_nuevo, mas_viejo), donde cada uno es una tupla con año y trimestre.
    """
    archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"

    with archivo_clean_path.open("r",encoding="utf-8") as archivo_individuos: 
        reader = csv.reader(archivo_individuos,delimiter=",")
        header = next(reader)
        lista_filas_individual = list(reader)

    anios_tri_individuos = agrupar_por_anio_y_trimestre(lista_filas_individual)
    mas_nuevo, mas_viejo = obtener_fechas(anios_tri_individuos)

    return mas_nuevo, mas_viejo

st.title(" Carga de Datos de EPH")  # Título principal de la sección

st.subheader("Fechas usadas en la aplicacion")

def finalizar_fechas ():
    """
    Devuelve los años y trimestres más nuevo y más viejo de los datos individuales.

    Returns:
        tuple: (mas_nuevo_anio, mas_viejo_anio, mas_nuevo_tri, mas_viejo_tri) como enteros.
    """
    mas_nuevo ,mas_viejo = mostrar_tiempo()
    return  int(mas_nuevo[0]) , int(mas_viejo[0]), int(mas_nuevo[1]) , int(mas_viejo[1])

mas_nuevo_anio , mas_viejo_anio, mas_nuevo_tri, mas_viejo_tri = finalizar_fechas()

if st.button(" Actualizar Dataset"):
    datos = actualizar_todo()  # Llama a la función para actualizar los datos
    if datos:
        st.success(" Datos actualizados correctamente.")  # Mensaje de éxitos
        mas_nuevo_anio , mas_viejo_anio, mas_nuevo_tri, mas_viejo_tri = finalizar_fechas()
        
        st.subheader(f' {mas_viejo_anio:02d}/{mas_viejo_tri} hasta {mas_nuevo_anio:02d}/{mas_nuevo_tri}')
    else: 
        st.error("Ocurrio un error al actualizar los datasets")



st.header("Comprobar si existen todos los archivos correctamente")

if st.button("Comprobar estado archivos"):
    faltantes = analizar_archivos()
    if len(faltantes) == 0: 
       st.success("No hay faltantes en los archivos")
    else: 
        for archivo in faltantes: 
            st.warning(f"Falta el archivo {archivo[0]} para el Trimestre {archivo[1][1]} en el año 20{archivo[2]}")   