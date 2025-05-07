<<<<<<< HEAD
import sys 
sys.path.append("..")
from src.utils.funciones import unir_archivos
from src.utils.funciones import ch04_str, nivel_ed, condicion_laboral, universitario 
from src.utils.constantes import DATA_CLEAN_PATH, DATA_PROCESSED_PATH
import csv 

def actualizar_clean_individuos():

    archivo_clean = DATA_CLEAN_PATH / "usu_clean_individual.csv"
    archivo_processed = DATA_PROCESSED_PATH / "usu_individual.csv"

    def new_fila (fila):
        new_fila = fila
        ch04_str(new_fila,fila)
        nivel_ed(new_fila,fila)
        condicion_laboral(new_fila,fila)
        universitario(new_fila,fila)
        return new_fila

    with archivo_clean.open("w",newline="", encoding="utf-8") as f:
        with archivo_processed.open("r",encoding="utf-8") as p:
            lector = csv.reader(p,delimiter=";")
            encabezado = next(lector) + ["CH04_str", "NIVEL_ED_str","CONDICION_LABORAL","UNIVERSITARIO"]
            escritor = csv.writer(f)
            escritor.writerow(encabezado)
            for fila in lector:
                new_fila_1 = new_fila(fila) 
                escritor.writerow(new_fila_1)        



def actualizar_individuos():
    unir_archivos("usu_individual")
    actualizar_clean_individuos()
def actualizar_hogares():
    unir_archivos("usu_hogar")
=======
def ch04_str (new_fila,fila):  
    if fila[11] == "1": 
        new_fila.append("masculino")
    else: 
        new_fila.append("femenino")

def nivel_ed (new_fila,fila):
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

def condicion_laboral (new_fila,fila):
    if fila[27] == "1":
        if fila[28] == "1" or fila[28] == "2" : 
            new_fila.append("ocupado autonomo")
        elif fila[28] == "3" or fila[28] == "4" or fila[28] == "9" : 
            new_fila.append("ocupado dependiente")
           
    elif fila[27] == "2": 
        new_fila.append("desocupado")
    elif fila[27] == "3": 
        new_fila.append("inactivo")
    else: 
        new_fila.append("fuera de categoria")
    
def universitario (new_fila,fila): 
    if fila[13] < "18":
        new_fila.append("2")
    else: 
        if fila[26] == "5" or fila[26] == "6":
            new_fila.append("1")
        else: 
            new_fila.append("0")
>>>>>>> 2cf3c2c70bb72165a324c9bbc1bbbf8c82802058
