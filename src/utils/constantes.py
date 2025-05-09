from pathlib import Path 

# Define la ruta base de la carpeta "data", que está ubicada tres niveles arriba del archivo actual.
DATA_PATH = Path(__file__).parent.parent.parent / "data" 

# Ruta para los datos limpios.
DATA_CLEAN_PATH = DATA_PATH / "clean"

# Ruta para los datos procesados.
DATA_PROCESSED_PATH = DATA_PATH / "processed"

# Ruta para los datos crudos.
DATA_RAW_PATH = DATA_PATH / "raw"


