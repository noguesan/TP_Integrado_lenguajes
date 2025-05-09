import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from glob import glob 
import sys 
sys.path.append("..")
from constantes import DATA_CLEAN_PATH, DATA_RAW_PATH, DATA_PROCESSED_PATH
import csv 
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

