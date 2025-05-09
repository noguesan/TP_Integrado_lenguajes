from glob import glob 
from pathlib import Path 
import csv

# Define la ruta base de la carpeta "data", que está ubicada tres niveles arriba del archivo actual.
DATA_PATH = Path(__file__).parent.parent.parent / "data" 

# Ruta para los datos limpios.
DATA_CLEAN_PATH = DATA_PATH / "clean"

# Ruta para los datos procesados.
DATA_PROCESSED_PATH = DATA_PATH / "processed"

# Ruta para los datos crudos.
DATA_RAW_PATH = DATA_PATH / "raw"
# Función que escribe todas las líneas de un archivo en otro archivo.

def unir_lineas(f, processed):
    for lines in f: 
        processed.write(lines)
        min = lines[1]
    return min

# Función que combina múltiples archivos de un tipo específico en un único archivo CSV.
def unir_archivos(tipo): 
    # Define el patrón de búsqueda para los archivos y el nombre del archivo combinado.
    new_tipo = str(tipo) + "*"
    new_tipo_csv = str(tipo) + ".csv"
    encabezado = False  
    archivo_processed = DATA_PROCESSED_PATH / new_tipo_csv  

    existe_min = False
    

    # Abre el archivo combinado en modo escritura.
    with archivo_processed.open("w") as processed:

        # Itera sobre los trimestres en la carpeta de datos crudos.
        for trimestre in DATA_RAW_PATH.iterdir():
    
            # Itera sobre los usuarios dentro de cada trimestre.
            for usu in trimestre.iterdir():
                # Busca archivos que coincidan con el patrón definido.
                for archivo in usu.glob(new_tipo): 
                    # Abre cada archivo encontrado.
                    with open(archivo, encoding="utf-8") as f:
                        if encabezado == False: 
                            # Si no se ha escrito el encabezado, escribe todas las líneas.
                            unir_lineas(f, processed)
                            encabezado = True  # Marca que el encabezado ya fue escrito.
                        else: 
                            # Si el encabezado ya fue escrito, omite la primera línea.
                            next(f) 
                            unir_lineas(f, processed)

# Función que calcula el porcentaje de un valor respecto a un total.
def porcentaje(valor, total):
    return (valor / total) * 100

def separar_por_trimestre(dict_anios): 
    dict_final = {}
    for anio in dict_anios:
        dict_temporal = {}
        
        for filas in dict_anios[anio]:
            trimestre = filas[2]
            if trimestre not in dict_temporal: 
                dict_temporal[trimestre] = []
            dict_temporal[trimestre].append(filas)

        dict_final[anio] = dict_temporal
    return dict_final


def agrupar_por_anio_y_trimestre(filas, col_anio=1):
    grupos = {}
    for fila in filas:
        anio = fila[col_anio]
        if anio not in grupos:
            grupos[anio] = []
        grupos[anio].append(fila)
    grupos_final = separar_por_trimestre(grupos)
    return grupos_final

def obtener_fechas (dict_trimestres): 
    max_anio = max(dict_trimestres.keys())
    max_trimestre = max(dict_trimestres[max_anio].keys())
    
    min_anio = min(dict_trimestres.keys())
    min_trimestre = min(dict_trimestres[min_anio].keys())

    return (max_anio,max_trimestre), (min_anio,min_trimestre)

# Funciones de la Sección B

def separar_por_trimestre(dict_anios): 
    dict_final = {}
    for anio in dict_anios:
        dict_temporal = {}
        
        for filas in dict_anios[anio]:
            trimestre = filas[2]
            if trimestre not in dict_temporal: 
                dict_temporal[trimestre] = []
            dict_temporal[trimestre].append(filas)

        dict_final[anio] = dict_temporal
    return dict_final


def agrupar_por_anio_y_trimestre(filas, col_anio=1):
    grupos = {}
    for fila in filas:
        anio = fila[col_anio]
        if anio not in grupos:
            grupos[anio] = []
        grupos[anio].append(fila)
    grupos_final = separar_por_trimestre(grupos)
    return grupos_final

def agrupar_por_aglomerado(filas, col_aglomerado):
    grupos = {}
    for fila in filas:
        aglo = fila[col_aglomerado]
        if aglo not in grupos:
            grupos[aglo] = []
        grupos[aglo].append(fila)
    return grupos

def obtener_archivo_reciente (dict_trimestres): 
    max_anio = max(dict_trimestres.keys())
    max_trimestre = max(dict_trimestres[max_anio].keys())
    return dict_trimestres[max_anio][max_trimestre]

def obtener_archivo_viejo (dict_trimestres):
    min_anio = min(dict_trimestres.keys())
    min_trimestre = min(dict_trimestres[min_anio].keys())
    return dict_trimestres[min_anio][min_trimestre]

# -------------------------

# funciones a agregar a Funciones.py
def nombre_aglomerado(codigo):
    """
    Devuelve el nombre del aglomerado a partir de su código.
    """
    dic_aglomerados = {
        '2': 'Gran La Plata',
        '3': 'Bahía Blanca - Cerri',
        '4': 'Gran Rosario',
        '5': 'Gran Santa Fé',
        '6': 'Gran Paraná',
        '7': 'Posadas',
        '8': 'Gran Resistencia',
        '9': 'Comodoro Rivadavia - Rada Tilly',
        '10': 'Gran Mendoza',
        '12': 'Corrientes',
        '13': 'Gran Córdoba',
        '14': 'Concordia',
        '15': 'Formosa',
        '17': 'Neuquén - Plottier',
        '18': 'Santiago del Estero - La Banda',
        '19': 'Jujuy - Palpalá',
        '20': 'Río Gallegos',
        '22': 'Gran Catamarca',
        '23': 'Gran Salta',
        '25': 'La Rioja',
        '26': 'Gran San Luis',
        '27': 'Gran San Juan',
        '29': 'Gran Tucumán - Tafí Viejo',
        '30': 'Santa Rosa - Toay',
        '31': 'Ushuaia - Río Grande',
        '32': 'Ciudad Autónoma de Buenos Aires',
        '33': 'Partidos del GBA',
        '34': 'Mar del Plata',
        '36': 'Río Cuarto',
        '38': 'San Nicolás - Villa Constitución',
        '91': 'Rawson - Trelew',
        '93': 'Viedma - Carmen de Patagones'
    }
    return dic_aglomerados.get(codigo)

def suma_ponderada(filas, condicion, col_pondera):
    """
    Calcula la suma ponderada de una determinada columna, considerando solo las filas que cumplen una condición.

    Parámetros:
    - filas: lista de listas, donde cada sublista representa una fila de datos.
    - condicion: función que recibe una fila y devuelve True si debe ser considerada en la suma.
    - col_pondera: índice entero que indica la posición de la columna que contiene el valor ponderador.

    Retorna:
    - Un número entero que representa la suma ponderada de las filas que cumplen con la condición.
    """
    total = 0
    for fila in filas:
        if condicion(fila):
            total += int(fila[col_pondera])
    return total
