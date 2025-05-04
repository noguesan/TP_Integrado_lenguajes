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
        if fila[28] == 1 or fila[28] == 2 : 
            new_fila.append("ocupado autonomo")
        else:
            for i in ["3","4","9"]:
                if fila[28] == i: 
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
    
