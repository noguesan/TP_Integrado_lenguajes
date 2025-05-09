# Importar módulos necesarios
import sys 
import os
import csv

# Agregar la ruta al sistema para importar módulos personalizados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importar funciones y constantes necesarias
from src.utils.funciones import unir_archivos  
from src.utils.constantes import DATA_CLEAN_PATH, DATA_PROCESSED_PATH  

# Función para procesar y limpiar los datos de hogares
def actualizar_clean_hogar():
    # Definir las rutas de los archivos de entrada y salida
    archivo_clean = DATA_CLEAN_PATH / "usu_clean_hogar.csv"  
    archivo_processed = DATA_PROCESSED_PATH / "usu_hogar.csv"  

    # Función interna para transformar una fila
    def new_fila(fila):
        new_fila = fila  # Copiar la fila original
        TIPO_HOGAR(new_fila, fila)  # Agregar columna de tipo de hogar
        MATERIAL_TECHUMBRE(new_fila, fila)  # Agregar columna de material de techumbre
        DENSIDAD_HOGAR(new_fila, fila)  # Agregar columna de densidad del hogar
        CONDICION_DE_HABITABILIDAD(new_fila, fila)  # Agregar columna de condición de habitabilidad
        return new_fila

    # Abrir el archivo limpio para escritura y el procesado para lectura
    with archivo_clean.open("w", newline="", encoding="utf-8") as f:
        with archivo_processed.open("r", encoding="utf-8") as p:
            lector = csv.reader(p, delimiter=";")  
            # Crear el encabezado con las nuevas columnas
            encabezado = next(lector) + ["TIPO_HOGAR", "MATERIAL_TECHUMBRE", "DENSIDAD_HOGAR", "CONDICION_DE_HABITABILIDAD"]
            escritor = csv.writer(f)  
            escritor.writerow(encabezado)  
            # Procesar cada fila del archivo procesado
            for fila in lector:
                new_fila_1 = new_fila(fila)  
                escritor.writerow(new_fila_1)  

# Función principal para actualizar los datos de hogares
def actualizar_hogar():
    unir_archivos("usu_hogar")  
    actualizar_clean_hogar() 

# Función para clasificar el tipo de hogar según el número de personas
def TIPO_HOGAR(new_fila, fila): 
    personas = int(fila[64])  # IX_TOT: Número total de personas en el hogar
    if personas == 1:
        new_fila.append("Unipersonal")  
    elif personas in [2, 3, 4]: 
        new_fila.append("Nuclear") 
    else:
        new_fila.append("Extendido")  

# Función para clasificar el material de la techumbre
def MATERIAL_TECHUMBRE(new_fila, fila): 
    try: 
        material = int(fila[14])  # IV4: Material de la techumbre
        if material in [5, 6, 7]:
            new_fila.append("Material precario")  
        elif material in [1, 2, 3, 4]:
            new_fila.append("Material durable")  
        else:
            new_fila.append("No aplica") 
    except: 
        new_fila.append("No tiene valor") 

# Función para clasificar la densidad del hogar según el número de personas y ambientes
def DENSIDAD_HOGAR(new_fila, fila): 
    try:
        # Manejar valores vacíos con un valor predeterminado
        ambientes = int(fila[11]) if fila[11].strip() else 0  # IV2: Número de ambientes
        personas = int(fila[64]) if fila[64].strip() else 0  # IX_TOT: Número total de personas

        # Clasificar densidad del hogar
        if ambientes > personas:
            new_fila.append("Bajo")  
        elif ambientes == personas or ambientes == personas + 1:
            new_fila.append("Medio")  
        elif ambientes < personas:
            new_fila.append("Alto")  
    except ValueError:
        # En caso de error, agregar un valor predeterminado
        new_fila.append("Datos inválidos")

# Función para clasificar la condición de habitabilidad del hogar
def CONDICION_DE_HABITABILIDAD(new_fila, fila):
    tiene_agua = fila[16]  # IV6: Disponibilidad de agua
    tiene_bano = fila[19]  # IV8: Disponibilidad de baño
    ubicacion_bano = fila[20]  # IV9: Ubicación del baño
    desague_bano = fila[22]  # IV11: Tipo de desagüe del baño
    material_pisos = fila[12]  # IV3: Material de los pisos

    # Clasificar la condición de habitabilidad
    if tiene_agua in ["1", "2"]:  
        if tiene_bano == "1" and material_pisos in ["1", "2"]:  
            if ubicacion_bano == "1" and material_pisos == "1" and desague_bano == "1":
                new_fila.append("buena") 
            else:
                new_fila.append("saludables") 
        else:
            new_fila.append("regular")  
    else:
        new_fila.append("insuficiente")  


