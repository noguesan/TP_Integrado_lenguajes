import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Educacion")

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

# Funciones auxiliares
def tiene_dos_ocupantes(elem):
    return int(elem[64]) >= 2

def es_universitario(elem):
    return elem[26] in ["5", "6"]

def porcentaje(a, b):
    return 100 * a / b if b != 0 else 0

def calcular_ranking(ultimos_individuos, ultimos_hogares):
    hogares_CODUSU, individuos_CODUSU, hogares, individuos = [], [], [], []
    poblacion_total_aglomerado, encuestas_finales, porcentajes_finales = {}, {}, {}

    for elem in ultimos_hogares:
        if not tiene_dos_ocupantes(elem):
            continue
        hogares.append(elem)
        hogares_CODUSU.append(elem[0])

    for elem in ultimos_individuos:
        if not es_universitario(elem):
            continue
        individuos.append(elem)
        individuos_CODUSU.append(elem[0])

    for elem in hogares:
        if elem[7] not in poblacion_total_aglomerado:
            poblacion_total_aglomerado[elem[7]] = 0
        poblacion_total_aglomerado[elem[7]] += int(elem[8])

        if elem[0] not in individuos_CODUSU:
            continue

        if elem[7] not in encuestas_finales:
            encuestas_finales[elem[7]] = []
        encuestas_finales[elem[7]].append(elem)

    for aglomerado in encuestas_finales:
        poblacion_final_aglomerado = 0
        for elem in encuestas_finales[aglomerado]:
            poblacion_final_aglomerado += int(elem[8])
        porcentajes_finales[aglomerado] = porcentaje(
            poblacion_final_aglomerado, poblacion_total_aglomerado[aglomerado]
        )

    ranking = pd.DataFrame([
        {"Aglomerado": aglo, "Porcentaje": porcentajes_finales[aglo]}
        for aglo in sorted(porcentajes_finales, key=porcentajes_finales.get, reverse=True)[:5]
    ])
    return ranking

# Carga de datos
df_individuos = pd.read_csv("data/clean/usu_clean_individual.csv", dtype=str)
df_hogares = pd.read_csv("data/clean/usu_clean_hogar.csv", dtype=str)

# Selectores de año y trimestre
anios = sorted(df_individuos["ANO4"].astype(int).unique())
trimestres = sorted(df_individuos["TRIMESTRE"].astype(int).unique())

anio = st.selectbox("Elegí el año", anios)
trimestre = st.selectbox("Elegí el trimestre", trimestres)

# Filtrado según selección
individuos = df_individuos[(df_individuos["ANO4"].astype(int) == anio) & (df_individuos["TRIMESTRE"].astype(int) == trimestre)]
hogares = df_hogares[(df_hogares["ANO4"].astype(int) == anio) & (df_hogares["TRIMESTRE"].astype(int) == trimestre)]

ultimos_individuos = individuos.values.tolist()
ultimos_hogares = hogares.values.tolist()

if st.button("Calcular ranking"):
    ranking = calcular_ranking(ultimos_individuos, ultimos_hogares)
    st.dataframe(ranking)
    # Gráfico de líneas
    st.line_chart(ranking.set_index('Aglomerado')['Porcentaje'])
    csv = ranking.to_csv(index=False)
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