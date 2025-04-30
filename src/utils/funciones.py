from constantes import DATA_RAW_PATH , DATA_PROCESSED_PATH
from glob import glob 

def unir_lineas(f,processed):
    for lines in f: 
        processed.write(lines)

def unir_archivos_individuos (tipo): 
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
    
