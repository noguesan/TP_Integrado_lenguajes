import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from glob import glob 
from src.utils.constantes import DATA_PROCESSED_PATH, DATA_RAW_PATH

def unir_lineas(f,processed):
    for lines in f: 
        processed.write(lines)

def unir_archivos (tipo): 
    new_tipo = str(tipo) + "*"
    new_tipo_csv = str(tipo) + ".csv"
    encabezado = False
    archivo_processed = DATA_PROCESSED_PATH / new_tipo_csv
    
    with archivo_processed.open("w") as processed:

        for trimestre in DATA_RAW_PATH.iterdir():
            for usu in trimestre.iterdir():
                for archivo in usu.glob(new_tipo): 
                    with open(archivo,encoding="utf-8") as f:
                        if encabezado == False: 
                            unir_lineas(f,processed)
                            encabezado = True 
                        else: 
                            next(f) 
                            unir_lineas(f,processed)

def porcentaje(valor,total):
    return (valor / total) * 100