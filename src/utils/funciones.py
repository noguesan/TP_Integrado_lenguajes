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
        
        for archivo in DATA_RAW_PATH.glob(new_tipo):
            
            with open(archivo) as f:
                if encabezado == False: 
                    unir_lineas(f,processed)
                    encabezado = True 
                else: 
                    f.next() 
                    unir_lineas(f,processed)
    
