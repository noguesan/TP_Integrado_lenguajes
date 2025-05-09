import streamlit as st 
from src.utils.funciones import actualizar_todo()

st.title(" Carga de Datos de EPH")  # Título principal de la sección

    # Botón para actualizar el dataset
if st.button(" Actualizar Dataset"):
    datos = actualizar_todo()  # Llama a la función para actualizar los datos
    if datos:
        st.success(" Datos actualizados correctamente.")  # Mensaje de éxito
