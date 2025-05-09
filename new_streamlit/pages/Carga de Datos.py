import streamlit as st 
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.procesamientos.pindividuos import actualizar_individuos
from src.procesamientos.phogares import actualizar_hogar


def actualizar_todo(): 
    actualizar_hogar()
    actualizar_individuos()
    return True
    

st.title(" Carga de Datos de EPH")  # Título principal de la sección



if st.button(" Actualizar Dataset"):
    datos = actualizar_todo()  # Llama a la función para actualizar los datos
    if datos:
        st.success(" Datos actualizados correctamente.")  # Mensaje de éxito
