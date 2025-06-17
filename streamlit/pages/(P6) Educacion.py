import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.title("1.6 (P6) Educacion")
st.subheader("Cantidad de personas según el máximo nivel educativo alcanzado")

# Cargar el dataset limpio
df = pd.read_csv("data/clean/usu_clean_individual.csv")
df_hogar = pd.read_csv("data/clean/usu_clean_hogar.csv")

# --- QUEDARSE SOLO CON EL ÚLTIMO TRIMESTRE DE CADA AÑO ---
ultimos_trimestres = df.groupby('ANO4')['TRIMESTRE'].max().reset_index()
df = df.merge(ultimos_trimestres, on=['ANO4', 'TRIMESTRE'])

# Selección de año
anios_disponibles = df['ANO4'].unique()
anio = st.selectbox("Seleccione un año", anios_disponibles)

# Filtrar por año
df_anio = df[df['ANO4'] == anio]

# --- Punto 1.6.1: Cantidad de personas por nivel educativo (ponderada) ---
st.subheader("Distribución general por nivel educativo")

conteo_ponderado = df_anio.groupby('NIVEL_ED_str')['PONDERA'].sum().reset_index()
conteo_ponderado.columns = ['Nivel educativo Maximo', 'Cantidad de personas']
st.dataframe(conteo_ponderado)
st.bar_chart(conteo_ponderado.set_index('Nivel educativo Maximo'))


# --- Punto 1.6.2: Nivel educacional más común por grupo etario 
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
        # Agrupar por nivel educativo y sumar la ponderación
        nivel_ponderado = df_grupo.groupby('NIVEL_ED_str')['PONDERA'].sum()
        nivel_comun = nivel_ponderado.idxmax()
        cantidad = nivel_ponderado.max()
        resultados.append([nombre, nivel_comun, int(cantidad)])
    else:
        resultados.append([nombre, "Sin datos", 0])

tabla_resultados = pd.DataFrame(resultados, columns=["Grupo de edad", "Nivel educativo más común", "Cantidad de personas (ponderada)"])
st.dataframe(tabla_resultados)
st.bar_chart(tabla_resultados.set_index("Grupo de edad")["Cantidad de personas (ponderada)"])

# --- Punto 1.6.3: Ranking y exportación 
st.subheader("Ranking de los 5 aglomerados con mayor porcentaje de hogares con 2+ ocupantes con estudios universitarios o superiores finalizados")

# Filtrar solo hogares con al menos 2 personas con estudios universitarios o superiores finalizados
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
st.line_chart(ranking.set_index('AGLOMERADO')['porcentaje'])


# Botón para exportar a CSV
csv = ranking.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Descargar ranking en CSV",
    data=csv,
    file_name='ranking_aglomerados.csv',
    mime='text/csv'
)

# --- Punto 1.6.4: Porcentaje de personas mayores a 6 años capaces e incapaces de leer y escribir 
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
st.bar_chart(tabla_lectoescritura[["% Capaces de leer y escribir","% Incapaces de leer y escribir"]],stack=False)
