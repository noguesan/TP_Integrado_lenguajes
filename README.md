
# TRABAJO-INTEGRADOR-EPH/
Desarrollo de una aplicación de búsqueda y visualización de información relacionada a la Encuesta Permanente de Hogares (EPH).

## Instalación de Dependencias

## Estructura del Proyecto
```
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
├── streamlit
│   ├── Inicio.py
│   └── Pages
│       ├──Busqueda por tema.py
│       ├──Carga de datos.py
│       └── visualización.py
│
├── notebooks/                 # Notebooks de Jupyter utilizados para análisis exploratorio, procesamiento y visualización.
│   ├── mainA_hogares.ipynb     # Análisis centrado en la base de hogares._agregar las columnas 
│   ├── mainA_individuos.ipynb  # Análisis centrado en la base de individuos._ agregar las columnas
│   └── Main_B.ipynb     # Desarrollo parte B.
│
├── src/                       # Módulos de código fuente
│   ├── procesamientos/        # Scripts de procesamiento y transformación de datos.
│   │   ├── phogares.py        # Procesamiento específico de la base de hogares.
│   │   ├── pindividuos.py     # Procesamiento específico de la base de individuos.
│   │   └── __init__.py        # Hace que src sea un paquete de Python.
│   ├── utils/                 # Funciones auxiliares y constantes generales.
│   │   ├── constantes.py      # PATH de las funciones
│   │   ├── funciones.py       # Funciones correspondientes a la seccion B
│   │   └── __init__.py        # Hace que src sea un paquete de Python.
│   └── __init__.py            # Hace que src sea un paquete de Python.
│
│
├── z_otros/                   # Documentación y recursos adicionales de contexto.
│   ├── EPH_registro_3T2024_DisenoTablas.pdf       # Descripción del contenido de las tablas
│   └── Python - Trabajo integrador parte 1.pdf    # Consigna del trabajo
│
├── .gitignore                 # Especifica archivos y carpetas que Git debe ignorar.
└── README.md                  # Descipcion contenido del proyecto.

```
