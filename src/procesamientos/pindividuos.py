# Importar módulos necesarios
import sys 
import csv 
import os

# Agregar la ruta al sistema para importar módulos personalizados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importar funciones y constantes necesarias
from src.utils.funciones import unir_archivos  
from src.utils.constantes import DATA_CLEAN_PATH, DATA_PROCESSED_PATH  

def actualizar_clean_individuos():
    """
    Procesa y limpia los datos de individuos, agregando columnas derivadas como género, nivel educativo,
    condición laboral y si es universitario. Guarda el resultado en un nuevo archivo CSV limpio.
    """
    # Definir las rutas de los archivos de entrada y salida
    archivo_clean = DATA_CLEAN_PATH / "usu_clean_individual.csv"  
    archivo_processed = DATA_PROCESSED_PATH / "usu_individual.csv"  

    def new_fila(fila):
        """
        Transforma una fila agregando las nuevas columnas procesadas.

        Args:
            fila (list): Fila original del archivo CSV.

        Returns:
            list: Fila original con las nuevas columnas agregadas.
        """
        new_fila = fila  # Copiar la fila original
        ch04_str(new_fila, fila)  # Agregar columna de género
        nivel_ed(new_fila, fila)  # Agregar columna de nivel educativo
        condicion_laboral(new_fila, fila)  # Agregar columna de condición laboral
        universitario(new_fila, fila)  # Agregar columna de si es universitario
        return new_fila

    # Abrir el archivo limpio para escritura y el procesado para lectura
    with archivo_clean.open("w", newline="", encoding="utf-8") as f:
        with archivo_processed.open("r", encoding="utf-8") as p:
            lector = csv.reader(p, delimiter=";")  
            # Crear el encabezado con las nuevas columnas
            encabezado = next(lector) + ["CH04_str", "NIVEL_ED_str", "CONDICION_LABORAL", "UNIVERSITARIO"]
            escritor = csv.writer(f)  
            escritor.writerow(encabezado)  
            # Procesar cada fila del archivo procesado
            for fila in lector:
                new_fila_1 = new_fila(fila)  
                escritor.writerow(new_fila_1)  

def actualizar_individuos():
    """
    Ejecuta el proceso completo de actualización de los datos de individuos,
    uniendo archivos y limpiando los datos.
    """
    unir_archivos("usu_individual") 
    actualizar_clean_individuos()  

def ch04_str(new_fila, fila):  
    """
    Agrega una columna con el género basado en el campo CH04.

    Args:
        new_fila (list): Fila a modificar.
        fila (list): Fila original del archivo CSV.
    """
    if fila[11] == "1":  
        new_fila.append("masculino")
    else:  
        new_fila.append("femenino")

def nivel_ed(new_fila, fila):
    """
    Agrega una columna con el nivel educativo basado en el campo NIVEL_ED.

    Args:
        new_fila (list): Fila a modificar.
        fila (list): Fila original del archivo CSV.
    """
    if fila[26] == "1": 
        new_fila.append("primario incompleto")
    elif fila[26] == "2": 
        new_fila.append("primario completo")
    elif fila[26] == "3": 
        new_fila.append("secundario incompleto")
    elif fila[26] == "4": 
        new_fila.append("secundario completo")
    elif fila[26] == "5" or fila[26] == "6": 
        new_fila.append("superior o universitario")
    else:
        new_fila.append("sin informacion") 

def condicion_laboral(new_fila, fila):
    """
    Agrega una columna con la condición laboral basada en los campos CONDICION y CAT_OCUP.

    Args:
        new_fila (list): Fila a modificar.
        fila (list): Fila original del archivo CSV.
    """
    if fila[27] == "1":  
        if fila[28] == "1" or fila[28] == "2": 
            new_fila.append("ocupado autonomo")  
        elif fila[28] == "3" or fila[28] == "4" or fila[28] == "9": 
            new_fila.append("ocupado dependiente")  
    elif fila[27] == "2": 
        new_fila.append("desocupado")  
    elif fila[27] == "3": 
        new_fila.append("inactivo") 
    else: 
        new_fila.append("fuera de categoria")  

def universitario(new_fila, fila): 
    """
    Agrega una columna indicando si es universitario basado en la edad y nivel educativo.

    Args:
        new_fila (list): Fila a modificar.
        fila (list): Fila original del archivo CSV.
    """
    if fila[13] < "18":  
        new_fila.append("2")  
    else: 
        if fila[26] == "5" or fila[26] == "6":  
            new_fila.append("1")  
        else: 
            new_fila.append("0")
