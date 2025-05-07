import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.funciones import unir_archivos
from src.utils.constantes import DATA_CLEAN_PATH, DATA_PROCESSED_PATH
import csv 


def actualizar_clean_hogar():

    archivo_clean = DATA_CLEAN_PATH / "usu_clean_hogar.csv"
    archivo_processed = DATA_PROCESSED_PATH / "usu_hogar.csv"

    def new_fila (fila):
        new_fila = fila
        TIPO_HOGAR(new_fila,fila)
        MATERIAL_TECHUMBRE(new_fila,fila)
        DENSIDAD_HOGAR(new_fila,fila)
        CONDICION_DE_HABITABILIDAD(new_fila,fila)
        return new_fila

    with archivo_clean.open("w",newline="", encoding="utf-8") as f:
        with archivo_processed.open("r",encoding="utf-8") as p:
            lector = csv.reader(p,delimiter=";")
            encabezado = next(lector) + ["TIPO_HOGAR", "MATERIAL_TECHUMBRE","DENSIDAD_HOGAR","CONDICION_DE_HABITABILIDAD"]
            escritor = csv.writer(f)
            escritor.writerow(encabezado)
            for fila in lector:
                new_fila_1 = new_fila(fila) 
                escritor.writerow(new_fila_1)        

def actualizar_hogar():
    unir_archivos("usu_hogar")
    actualizar_clean_hogar()
    



#Funciones para procesar la información de hogares

def TIPO_HOGAR (new_fila,fila): 
    personas = int(fila[64]) # IX_TOT
    if personas == 1:
        new_fila.append("Unipersonal")
    elif personas == 2 or personas == 3 or personas == 4: 
        new_fila.append("Nuclear")
    else:
        new_fila.append(f"Extendido")
        
def MATERIAL_TECHUMBRE (new_fila,fila): 
    try: 
        material = int(fila[14]) # IV4
        if material in [5,6,7]:
            new_fila.append("Material precario")
        elif material in [1,2,3,4]:
            new_fila.append("Material durable")
        else:
            new_fila.append("No aplica")
    except: 
        new_fila.append("No tiene valor")

def DENSIDAD_HOGAR(new_fila, fila): 
    try:
        # Manejar valores vacíos con un valor predeterminado
        ambientes = int(fila[11]) if fila[11].strip() else 0  # IV2
        personas = int(fila[64]) if fila[64].strip() else 0  # IX_TOT

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

def CONDICION_DE_HABITABILIDAD(new_fila, fila):
    tiene_agua = fila[16] # IV6
    tiene_bano = fila[19] # IV8
    ubicacion_bano = fila[20] # IV9
    desague_bano = fila[22] # IV11
    material_pisos = fila[12] # IV3


    if tiene_agua == "1" or tiene_agua == "2": 
        if tiene_bano == "1" and( material_pisos == "1" or material_pisos == "2"):
            if ubicacion_bano == "1" and material_pisos == "1" and desague_bano == "1":
                    new_fila.append("buena")
            else:
                new_fila.append("saludables")
        else:
            new_fila.append("regular")
    else:
        new_fila.append("insuficiente")

    
    