import streamlit as st 
import sys 
import os
import csv 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.procesamientos.pindividuos import actualizar_individuos
from src.procesamientos.phogares import actualizar_hogar
from src.utils.funciones import  agrupar_por_anio_y_trimestre, obtener_fechas
from src.utils.constantes import DATA_CLEAN_PATH


def actualizar_todo(): 
    actualizar_hogar()
    actualizar_individuos()
    return True



def mostrar_tiempo ():
    archivo_clean_path = DATA_CLEAN_PATH / "usu_clean_individual.csv"

    archivo_individuos = archivo_clean_path.open("r",encoding="utf-8") 
    reader = csv.reader(archivo_individuos,delimiter=";")
    header = next(reader)

    new_list_i = []

    for elem in reader:
        new_elem = elem[0].split(',')
        new_list_i.append(new_elem)

    lista_filas_individual = new_list_i[:]
    anios_tri_individuos = agrupar_por_anio_y_trimestre(lista_filas_individual)
    mas_nuevo, mas_viejo = obtener_fechas(anios_tri_individuos)

    return mas_nuevo, mas_viejo



st.title(" Carga de Datos de EPH")  # Título principal de la sección

st.subheader("Fechas usadas en la aplicacion")
def finalizar_fechas ():
    mas_nuevo ,mas_viejo = mostrar_tiempo()
    return  int(mas_nuevo[0]) , int(mas_viejo[0]), int(mas_nuevo[1]) , int(mas_viejo[1])

mas_nuevo_anio , mas_viejo_anio, mas_nuevo_tri, mas_viejo_tri = finalizar_fechas()


if st.button(" Actualizar Dataset"):
    datos = actualizar_todo()  # Llama a la función para actualizar los datos
    if datos:
        st.success(" Datos actualizados correctamente.")  # Mensaje de éxitos
        mas_nuevo_anio , mas_viejo_anio, mas_nuevo_tri, mas_viejo_tri = finalizar_fechas()


st.subheader(f' {mas_viejo_anio:02d}/{mas_viejo_tri} hasta {mas_nuevo_anio:02d}/{mas_nuevo_tri}')
