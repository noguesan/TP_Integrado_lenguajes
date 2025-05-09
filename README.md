
# TRABAJO-INTEGRADOR-EPH/
Encuest.AR es una aplicación que facilita el acceso y análisis de los datos recolectados por la Encuesta Permanente de Hogares (EPH), un programa nacional realizado por el INDEC para conocer las características socioeconómicas de la población argentina. Permite visualizar y explorar información procesada de los datos crudos de la EPH, facilitando el análisis de las tendencias y características socioeconómicas de la población en distintas áreas como educación, ocupación y vivienda.

## Integrantes del grupo
Nogueira Santiago
Caselli Felipe
Benavidez GRegorio
Martins Thiago

## Uso de la aplicacion
Para iniciar la aplicación se debe ejecutar streamlit run streamlit/Inicio.py

interfaz de la aplicacion:
P1: Inicio: Contiene información general sobre la EPH y la aplicación.
P2: Carga de Datos: Muestra los datasets disponibles (actualmente con datos de 2023 y 2024). Puedes hacer clic en un botón para actualizar los datasets.
P3: Búsqueda por Tema: Aquí puedes explorar diferentes temas de la EPH, aunque esta sección está en desarrollo.
P4: Visualización: Presenta diferentes visualizaciones de los datos.

## Instalación de Dependencias
python 3.12.9
streamlit
otras librerias (sys, os, csv, src)


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
