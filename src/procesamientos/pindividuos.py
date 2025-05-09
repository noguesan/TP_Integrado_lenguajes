# Importar módulos necesarios
import sys 
import csv 
import os

# Agregar la ruta al sistema para importar módulos personalizados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importar funciones y constantes necesarias
from src.utils.funciones import unir_archivos  # Función para unir archivos raw
from src.utils.constantes import DATA_CLEAN_PATH, DATA_PROCESSED_PATH  # Rutas de archivos

# Función para procesar y limpiar los datos de individuos
def actualizar_clean_individuos():
    # Definir las rutas de los archivos de entrada y salida
    archivo_clean = DATA_CLEAN_PATH / "usu_clean_individual.csv"  # Archivo limpio de salida
    archivo_processed = DATA_PROCESSED_PATH / "usu_individual.csv"  # Archivo procesado de entrada

    # Función interna para transformar una fila
    def new_fila(fila):
        new_fila = fila  # Copiar la fila original
        ch04_str(new_fila, fila)  # Agregar columna de género
        nivel_ed(new_fila, fila)  # Agregar columna de nivel educativo
        condicion_laboral(new_fila, fila)  # Agregar columna de condición laboral
        universitario(new_fila, fila)  # Agregar columna de si es universitario
        return new_fila

    # Abrir el archivo limpio para escritura y el procesado para lectura
    with archivo_clean.open("w", newline="", encoding="utf-8") as f:
        with archivo_processed.open("r", encoding="utf-8") as p:
            lector = csv.reader(p, delimiter=";")  # Leer el archivo procesado como CSV
            # Crear el encabezado con las nuevas columnas
            encabezado = next(lector) + ["CH04_str", "NIVEL_ED_str", "CONDICION_LABORAL", "UNIVERSITARIO"]
            escritor = csv.writer(f)  # Crear un escritor para el archivo limpio
            escritor.writerow(encabezado)  # Escribir el encabezado en el archivo limpio
            # Procesar cada fila del archivo procesado
            for fila in lector:
                new_fila_1 = new_fila(fila)  # Transformar la fila
                escritor.writerow(new_fila_1)  # Escribir la fila transformada en el archivo limpio

# Función principal para actualizar los datos de individuos
def actualizar_individuos():
    unir_archivos("usu_individual")  # Combinar los archivos raw en un archivo procesado
    actualizar_clean_individuos()  # Limpiar y procesar los datos

# Función para agregar una columna con el género basado en el campo CH04
def ch04_str(new_fila, fila):  
    if fila[11] == "1":  # Si el valor es "1", es masculino
        new_fila.append("masculino")
    else:  # Si no, es femenino
        new_fila.append("femenino")

# Función para agregar una columna con el nivel educativo basado en el campo NIVEL_ED
def nivel_ed(new_fila, fila):
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
        new_fila.append("sin informacion")  # Si no coincide con ninguna categoría, agregar "sin información"

# Función para agregar una columna con la condición laboral basada en los campos CONDICION y CAT_OCUP
def condicion_laboral(new_fila, fila):
    if fila[27] == "1":  # Si está ocupado
        if fila[28] == "1" or fila[28] == "2": 
            new_fila.append("ocupado autonomo")  # Autónomo
        elif fila[28] == "3" or fila[28] == "4" or fila[28] == "9": 
            new_fila.append("ocupado dependiente")  # Dependiente
    elif fila[27] == "2": 
        new_fila.append("desocupado")  # Desocupado
    elif fila[27] == "3": 
        new_fila.append("inactivo")  # Inactivo
    else: 
        new_fila.append("fuera de categoria")  # Categoría desconocida

# Función para agregar una columna indicando si es universitario basado en la edad y nivel educativo
def universitario(new_fila, fila): 
    if fila[13] < "18":  # Si es menor de 18 años
        new_fila.append("2")  # No aplica
    else: 
        if fila[26] == "5" or fila[26] == "6":  # Si tiene nivel superior o universitario
            new_fila.append("1")  # Es universitario
        else: 
            new_fila.append("0")  # No es universitario
