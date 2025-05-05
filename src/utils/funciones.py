from glob import glob 
from src.utils.constantes import DATA_PROCESSED_PATH, DATA_RAW_PATH

# Funciones para unir archivos de datos y procesar la información (hogares y personas)

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

#Funciones para procesar la información de individuos

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

#Funciones para procesar la información de hogares

# IX_TOT: Cantidad de miembros del hogar (Columna 64)
def TIPO_HOGAR (new_fila,fila): 
    personas = int(fila[64])
    if personas == 1:
        new_fila.append("Unipersonal")
    elif personas == 2 or personas == 3 or personas == 4: 
        new_fila.append("Nuclear")
    else:
        new_fila.append(f"Extendido")
    

# IV4: Tipo de vivienda. (Columna 47)
def MATERIAL_TECHUMBRE (new_fila,fila): 
    material = int(fila[47])
    if material in [5,6,7]:
        new_fila.append("Material precario")
    elif material in [1,2,3,4]:
        new_fila.append("Material durable")
    else:
        new_fila.append("No aplica")
    

# IV2: ¿Cuántos ambientes/habitaciones tiene la vivienda en total? (Columna 12) 
# IX _Tot: Cantidad de miembros del hogar (Columna 64)
def DENSIDAD_HOGAR (new_fila,fila): 
    if fila[12] > fila[64]:
        new_fila.append("Bajo")
    elif fila[12] == fila[64] or fila[12] == fila[65]:
        new_fila.append("Medio")
    elif fila[12] < fila[64]:
        new_fila.append("Alto")

# Explicacion y sus respectivas columnas:
# IV6: tiene agua. (Columna 17)
# IV8: posee baño. (Columna 20)
# IV9: ubicación del baño. (Columna 21)
# IV11: desagüe del baño. (Columna 23)
# IV3: material de pisos interiores. (Columna 13)

def CONDICION_DE_HABITABILIDAD(new_fila, fila):
    # Reglas para clasificar como "insuficiente"
    if fila[17] == "3" or fila[20] == "2" or fila[21] == "3" or fila[23] == "4":
        new_fila.append("insuficiente")
    # Reglas para clasificar como "regular"
    elif fila[17] == "1" and fila[20] == "1" and fila[21] == "1" and fila[23] in ["1", "2"]:
        new_fila.append("regular")
    # Reglas para clasificar como "saludables"
    elif fila[17] == "1" and fila[20] == "1" and fila[21] == "1" and fila[23] == "1" and fila[13] in ["1", "2", "3"]:
        new_fila.append("saludables")
    # Reglas para clasificar como "buena"
    elif fila[17] == "1" and fila[20] == "1" and fila[21] == "1" and fila[23] == "1" and fila[13] == "1":
        new_fila.append("buena")

