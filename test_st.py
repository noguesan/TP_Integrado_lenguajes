import streamlit as st
st.header('Mi primera app con Stremalit')
st.subheader('''Características de st.write 
             Muestra texto plano o con formato Markdown''')
st.set_page_config(layout="wide")
st.write('Hola **mundo**')
if st.button('Mostrar opciones'):
    st.write('# Soy un título')
    st.write(""" * se considera el Swiss Knife de Streamlit. Esto quiere decir que tiene la capacidad de renderizar diferentes cosas dependiendo lo que reciba como parámetro.
    """)
st.subheader('Contenido de variables simples')
x = 10
st.write(f"El valor de {x= }")

st.subheader('Contenido de estructuras')
my_list = [1, 2, 3, 4, 5]
st.write("La lista es:", my_list)