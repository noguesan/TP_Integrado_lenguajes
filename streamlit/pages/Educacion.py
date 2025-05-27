import streamlit as st
import pandas as pd

st.title("Cantidad de personas según el máximo nivel educativo alcanzado")

# Cargar el dataset limpio
df = pd.read_csv("data/clean/usu_clean_individual.csv")
df_hogar = pd.read_csv("data/clean/usu_clean_hogar.csv")

# Ingreso manual del años
anio = st.number_input("Ingrese un año", step=1, format="%d")

# Filtrar por año
df_anio = df[df['ANO4'] == anio]

# --- Punto 1.6.1: Cantidad de personas por nivel educativo ---
st.subheader("Distribución general por nivel educativo")
conteo = df_anio['NIVEL_ED_str'].value_counts().reset_index()
conteo.columns = ['Nivel educativo', 'Cantidad de personas']
st.dataframe(conteo)
st.bar_chart(conteo.set_index('Nivel educativo'))

# --- Punto 1.6.2: Nivel educacional más común por grupo etario ---
st.subheader("Nivel educacional más común por grupo etario")

grupos = [
    ("20-30", 20, 30),
    ("30-40", 30, 40),
    ("40-50", 40, 50),
    ("50-60", 50, 60),
    ("60+", 60, 200)
]
opciones = [g[0] for g in grupos]
seleccionados = st.multiselect(
    "Seleccione los intervalos etarios a visualizar",
    opciones,
    default=opciones
)

resultados = []
for nombre, edad_min, edad_max in grupos:
    if nombre not in seleccionados:
        continue
    if nombre == "60+":
        df_grupo = df[df['CH06'] >= edad_min]
    else:
        df_grupo = df[(df['CH06'] >= edad_min) & (df['CH06'] < edad_max)]
    if not df_grupo.empty:
        nivel_comun = df_grupo['NIVEL_ED_str'].mode()[0]
        cantidad = (df_grupo['NIVEL_ED_str'] == nivel_comun).sum()
        resultados.append([nombre, nivel_comun, cantidad])
    else:
        resultados.append([nombre, "Sin datos", 0])

tabla_resultados = pd.DataFrame(resultados, columns=["Grupo de edad", "Nivel educativo más común", "Cantidad de personas"])
st.dataframe(tabla_resultados)

# --- Punto 1.6.3: Ranking y exportación ---
st.subheader("Ranking de los 5 aglomerados con mayor porcentaje de hogares con 2+ ocupantes con estudios universitarios o superiores finalizados")

# Filtrar solo hogares con al menos 2 personas con estudios universitarios o superiores finalizados
# Suponiendo que 'CODUSU' es el identificador de hogar y 'NIVEL_ED_str' está en df
universitarios = df[df['NIVEL_ED_str'] == "superior o universitario"]
conteo_hogar = universitarios.groupby('CODUSU').size().reset_index(name='cant_uni')
hogares_2mas = conteo_hogar[conteo_hogar['cant_uni'] >= 2]

# Unir con datos de hogar para obtener el aglomerado
hogares_2mas = hogares_2mas.merge(df_hogar[['CODUSU', 'AGLOMERADO']], on='CODUSU', how='left')

# Calcular porcentaje de hogares con 2+ universitarios por aglomerado
total_hogares = df_hogar.groupby('AGLOMERADO').size().reset_index(name='total_hogares')
hogares_con_2mas = hogares_2mas.groupby('AGLOMERADO').size().reset_index(name='hogares_2mas')
ranking = hogares_con_2mas.merge(total_hogares, on='AGLOMERADO')
ranking['porcentaje'] = 100 * ranking['hogares_2mas'] / ranking['total_hogares']
ranking = ranking.sort_values('porcentaje', ascending=False).head(5)

st.dataframe(ranking)

# Botón para exportar a CSV
csv = ranking.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Descargar ranking en CSV",
    data=csv,
    file_name='ranking_aglomerados.csv',
    mime='text/csv'
)
# --- Punto 1.6.4: Porcentaje de personas mayores a 6 años capaces e incapaces de leer y escribir ---
st.subheader("Porcentaje de personas mayores a 6 años capaces e incapaces de leer y escribir por año")
resultados_lectoescritura = []

for anio in sorted(df['ANO4'].unique()):
    df_anio = df[(df['ANO4'] == anio) & (df['CH06'] > 6)]
    total = len(df_anio)
    if total == 0:
        capaces = incapaces = 0
    else:
        capaces = (df_anio['CH09'] == 1).sum() / total * 100
        incapaces = (df_anio['CH09'] == 2).sum() / total * 100
    resultados_lectoescritura.append([anio, round(capaces, 2), round(incapaces, 2)])

tabla_lectoescritura = pd.DataFrame(resultados_lectoescritura, columns=["Año", "% Capaces de leer y escribir", "% Incapaces de leer y escribir"])
st.dataframe(tabla_lectoescritura)
                                                                     