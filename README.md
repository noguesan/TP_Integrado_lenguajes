```
# TRABAJO-INTEGRADOR-EPH/
Desarrollo de una aplicación de búsqueda y visualización de información relacionada a la Encuesta Permanente de Hogares (EPH).

## Instalación de Dependencias

## Estructura del Proyecto

├── data/                       
│   ├── clean/               
│   │   ├── usu_hogar_modificado_T324.csv  
│   │   └── usu_individual_modificado_T324.csv
│   ├── processed/              
│   │   ├── usu_hogar.csv
│   │   └── usu_individual.csv
│   └── raw/                 
│       ├── usu_hogar_T324.txt
│       └── usu_individual_T324.txt
│
├── data/                      # datos
│   ├── raw/                   # Datos originales descargados de la EPH sin procesar.
│   ├── processed/             # Unifica los archivos 
│   └── clean/                 # Datos procesados, con las nuevas columnas 
│
├── notebooks/                 # Notebooks de Jupyter utilizados para análisis exploratorio, procesamiento y visualización.
│   ├── main.ipynb             # BORRAR
│   ├── main_v2.ipynb          # BORRAR
│   ├── main_hogares.ipynb     # Análisis centrado en la base de hogares._agregar las columnas 
│   ├── main_individuos.ipynb  # Análisis centrado en la base de individuos._ agregar las columnas
│   └── Sección_B.ipynb        # Desarrollo parte B.
│
├── src/                       # Módulos de código fuente
│   ├── consultas/             # BORAR ???????????????
│   │   └── consultas.py       # 
│   ├── procesamientos/        # Scripts de procesamiento y transformación de datos.
│   │   ├── phogares.py        # Procesamiento específico de la base de hogares.
│   │   └── pindividuos.py     # Procesamiento específico de la base de individuos.
│   ├── utils/                 # Funciones auxiliares y constantes generales.
│   │   ├── constantes.py      # PATH de las funciones
│   │   └── funciones.py       # Funciones correspondientes a la seccion B
│   └── __init__.py            # Hace que src sea un paquete de Python.
│
├── test/                      # Archivos de prueba utilizados para validar funciones y transformaciones.  # BORRAR
│   ├── usu_hogar_modificado_T324.csv
│   └── usu_individual_modificado_T324.csv
│
├── z_otros/                   # Documentación y recursos adicionales de contexto.
│   ├── EPH_consideraciones_metodologicas_2t20.pdf # BORAR 
│   ├── EPH_nota_metodologica_1_trim_2019.pdf      # BORAR 
│   ├── EPH_registro_3T2024_DisenoTablas.pdf       # Descripción del contenido de las tablas
│   ├── Gasetilla_EPHContinua.pdf                  # BORAR 
│   └── Python - Trabajo integrador parte 1.pdf    # Consigna del trabajo
│
├── .gitignore                 # Especifica archivos y carpetas que Git debe ignorar.
├── README.md                  # Descipcion contenido del proyecto.
├── Licencia                   # CREAR
├── Requerimientos             # CREAR
## Estructura del Proyecto
```
