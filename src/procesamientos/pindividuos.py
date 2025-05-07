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