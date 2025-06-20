
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
├── .gitignore                 # Especifica archivos y carpetas que Git debe ignorar.
├── aglomerados_coordenadas.json # datos de las coordenadas de los aglomerados
├── estructura.txt             # Archivo con la estructura del proyecto.
├── License.txt                # Licencia
├── README.md                  # Descipción contenido del proyecto.
├── requirements.txt           # Requerimientos para uso del programa
├── resultados_filtrados.csv
├── valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv
│
├── data/                        # Datos divididos en etapas de procesamiento.
│   ├── clean/                  # Datos limpios y procesados para análisis.
│   │   ├── usu_clean_hogar.csv
│   │   ├── usu_clean_individual.csv
│   │   ├── usu_hogar_modificado_T324.csv  
│   │   └── usu_individual_modificado_T324.csv
│   │
│   ├── processed/              # Datos procesados listos para usar.
│   │   ├── usu_hogar.csv
│   │   └── usu_individual.csv
│   │
│   └── raw/                   # Datos en crudo originales.
│       ├── EPH_usu_1_Trim_2024_txt/
│       │   └── EPH_usu_1er_Trim_2024_txt/
│       │       ├── usu_hogar_T124.txt
│       │       └── usu_individual_T124.txt
│       │
│       ├── EPH_usu_2_Trim_2024_txt/
│       │   └── EPH_usu_2do_Trim2024_txt/
│       │       ├── usu_hogar_T224.txt
│       │       └── usu_individual_T224.txt
│       │
│       └── EPH_usu_3er_Trim_2023_txt/
│           └── EPH_usu_3er_Trimm_2023_txt/
│               ├── usu_hogar_T323.txt
│               └── usu_individual_T323.txt
│
├── notebooks/                 # Notebooks de Jupyter utilizados para análisis exploratorio, procesamiento y visualización.
│   ├── mainA_hogares.ipynb     # Análisis centrado en la base de hogares._agregar las columnas 
│   ├── mainA_individuos.ipynb  # Análisis centrado en la base de individuos._ agregar las columnas
│   └── Main_B.ipynb            # Desarrollo parte B.
│
├── src/                       # Módulos de código fuente
│   ├── st_test.ipynb          # Notebook para pruebas en src
│   ├── __init__.py            # Hace que src sea un paquete de Python.
│   │
│   ├── procesamientos/        # Scripts de procesamiento y transformación de datos.
│   │   ├── phogares.py        # Procesamiento específico de la base de hogares.
│   │   ├── pindividuos.py     # Procesamiento específico de la base de individuos.
│   │   └── __init__.py        # Hace que src sea un paquete de Python.
│   │
│   ├── utils/                 # Funciones auxiliares y constantes generales.
│   │   ├── constantes.py      # PATH de las funciones
│   │   ├── Filtros_Streamlit.py # Tiene los filtros de la sidebar de las pagianas 3, 4, 5, y 7 
│   │   ├── funciones.py       # Funciones correspondientes a la seccion B
│   │   ├── funciones_page_ActividadYEmpleo.py # Funciones auxiliares de la pagina Actividad y empleo.py
│   │   └── __init__.py        # Hace que src sea un paquete de Python.
│   │
│   └── __pycache__/           # Archivos compilados de Python
│
├── streamlit                  # Aplicación Streamlit
│   ├── Inicio.py
│   └── pages/                 # Páginas divididas por temas
│       ├── (P2) Carga de Datos.py
│       ├── (P3) Caracteristicas demograficas.py
│       ├── (P4) Caracteristicas de la vivienda.py
│       ├── (P5) Actividad y empleo.py
│       ├── (P6) Educacion.py
│       └── (P7) Ingresos.py
│
└── z_otros/                   # Documentación y recursos adicionales de contexto.
    ├── EPH_registro_3T2024_DisenoTablas.pdf       # Descripción del contenido de las tablas
    ├── Python - Trabajo integrador parte 1.pdf    # Consigna del trabajo
    └── Trabajo Integrador 2025 - Parte 2.pdf
```