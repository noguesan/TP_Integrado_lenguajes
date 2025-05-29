from glob import glob 
from pathlib import Path 
import csv
DATA_PATH = Path(__file__).parent.parent.parent / "data" 

# Ruta para los datos limpios.
DATA_CLEAN_PATH = DATA_PATH / "clean"

# Ruta para los datos procesados.
DATA_PROCESSED_PATH = DATA_PATH / "processed"

# Ruta para los datos crudos.
DATA_RAW_PATH = DATA_PATH / "raw"



def unir_lineas(f, processed):
    """
    Escribe todas las líneas de un archivo en otro archivo.

    Args:
        f (file object): Archivo de lectura.
        processed (file object): Archivo de escritura.

    Returns:
        str: El segundo carácter de la última línea procesada (puede usarse para control interno).
    """
    for lines in f: 
        processed.write(lines)
      

def unir_archivos(tipo): 
    """
    Combina múltiples archivos de un tipo específico en un único archivo CSV.

    Args:
        tipo (str): Prefijo del tipo de archivo a combinar (por ejemplo, 'usu_individual').

    Crea un archivo CSV combinado en la carpeta de datos procesados.
    """
    new_tipo = str(tipo) + "*"
    new_tipo_csv = str(tipo) + ".csv"
    encabezado = False  
    archivo_processed = DATA_PROCESSED_PATH / new_tipo_csv  

    with archivo_processed.open("w") as processed:
        for trimestre in DATA_RAW_PATH.iterdir():
            for usu in trimestre.iterdir():
                for archivo in usu.glob(new_tipo): 
                    with open(archivo) as f:
                        if encabezado == False: 
                            unir_lineas(f, processed)
                            encabezado = True
                        else: 
                            next(f) 
                            unir_lineas(f, processed)


def porcentaje(valor, total):
    """
    Calcula el porcentaje de un valor respecto a un total.

    Args:
        valor (float or int): Valor parcial.
        total (float or int): Valor total.

    Returns:
        float: Porcentaje correspondiente.
    """
    return (valor / total) * 100

def separar_por_trimestre(dict_anios): 
    """
    Separa un diccionario de años en subdiccionarios por trimestre.

    Args:
        dict_anios (dict): Diccionario con años como claves y listas de filas como valores.

    Returns:
        dict: Diccionario anidado por año y trimestre.
    """
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
    """
    Agrupa filas por año y trimestre.

    Args:
        filas (list): Lista de filas (listas).
        col_anio (int): Índice de la columna año.

    Returns:
        dict: Diccionario anidado por año y trimestre.
    """
    grupos = {}
    for fila in filas:
        anio = fila[col_anio]
        if anio not in grupos:
            grupos[anio] = []
        grupos[anio].append(fila)
    grupos_final = separar_por_trimestre(grupos)
    return grupos_final

def agrupar_por_aglomerado(filas, col_aglomerado):
    """
    Agrupa filas por código de aglomerado.

    Args:
        filas (list): Lista de filas (listas).
        col_aglomerado (int): Índice de la columna aglomerado.

    Returns:
        dict: Diccionario con códigos de aglomerado como claves y listas de filas como valores.
    """
    grupos = {}
    for fila in filas:
        aglo = fila[col_aglomerado]
        if aglo not in grupos:
            grupos[aglo] = []
        grupos[aglo].append(fila)
    return grupos

def obtener_archivo_reciente(dict_trimestres): 
    """
    Obtiene la lista de filas correspondiente al año y trimestre más reciente.

    Args:
        dict_trimestres (dict): Diccionario anidado por año y trimestre.

    Returns:
        list: Lista de filas del archivo más reciente.
    """
    max_anio = max(dict_trimestres.keys())
    max_trimestre = max(dict_trimestres[max_anio].keys())
    return dict_trimestres[max_anio][max_trimestre]

def obtener_archivo_viejo(dict_trimestres):
    """
    Obtiene la lista de filas correspondiente al año y trimestre más antiguo.

    Args:
        dict_trimestres (dict): Diccionario anidado por año y trimestre.

    Returns:
        list: Lista de filas del archivo más antiguo.
    """
    min_anio = min(dict_trimestres.keys())
    min_trimestre = min(dict_trimestres[min_anio].keys())
    return dict_trimestres[min_anio][min_trimestre]

def obtener_fechas (dict_trimestres): 
    max_anio = max(dict_trimestres.keys())
    max_trimestre = max(dict_trimestres[max_anio].keys())
    
    min_anio = min(dict_trimestres.keys())
    min_trimestre = min(dict_trimestres[min_anio].keys())

    return (max_anio,max_trimestre), (min_anio,min_trimestre)


def nombre_aglomerado(codigo):
    """
    Devuelve el nombre del aglomerado a partir de su código.

    Args:
        codigo (str): Código del aglomerado.

    Returns:
        str or None: Nombre del aglomerado o None si no existe.
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

    Args:
        filas (list): Lista de listas, donde cada sublista representa una fila de datos.
        condicion (function): Función que recibe una fila y devuelve True si debe ser considerada en la suma.
        col_pondera (int): Índice de la columna que contiene el valor ponderador.

    Returns:
        int: Suma ponderada de las filas que cumplen con la condición.
    """
    total = 0
    for fila in filas:
        if condicion(fila):
            total += int(fila[col_pondera])
    return total


def buscar_trimestre_faltante(archivos,archivos_faltantes):
    new_archivos = list()

    for elem in archivos: 
        new_archivos.append(elem.split("_"))

    if len(new_archivos) == 1: 
        archivos_faltantes.append([new_archivos[0][1] , new_archivos[0][2][:2] , new_archivos[0][2][2:4]])
                                #Tipo(individual/hogar) # trimestre         # anio
        estado = True
    return archivos_faltantes 


def analizar_archivos():
    archivos_faltantes = list()
    for trimestre in DATA_RAW_PATH.iterdir(): 
        for usu in trimestre.iterdir(): 
            archivos_encontrados = [archivo.stem for archivo in usu.glob("usu_*")]
            buscar_trimestre_faltante(archivos_encontrados,archivos_faltantes)  
    return archivos_faltantes
