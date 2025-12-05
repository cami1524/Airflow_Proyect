# 🌬️ Airflow ETL Pipeline - Remote Jobs

Pipeline de datos construido con **Apache Airflow** que extrae ofertas de trabajo remoto desde la API de [Remotive](https://remotive.com), las transforma y genera un archivo CSV limpio.

## 📁 Estructura del Proyecto
Airflow_Proyect/
├── dags/
│ ├── helpers/
│ │ ├── extract.py # Extracción desde API
│ │ ├── transform.py # Limpieza de datos
│ │ └── load.py # Carga a CSV
│ ├── data/
│ │ ├── raw/ # JSON descargados (generado)
│ │ └── processed/ # CSV final (generado)
│ ├── job_etl_dag.py # DAG principal del ETL
│ └── primer_dag.py # DAG de prueba
├── plugins/ # Plugins personalizados de Airflow
├── logs/ # Logs de ejecución (generado)
├── docker-compose.yaml # Configuración de Docker
├── requirements.txt # Dependencias Python
└── README.md


## 🚀 Cómo Ejecutar

### Prerrequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

### Pasos

1. **Clonar el repositorio**
   
   git clone https://github.com/tu-usuario/Airflow_Proyect.git
   cd Airflow_Proyect
   2. **Levantar los contenedores**
   
   docker-compose up -d
   3. **Esperar 1-2 minutos** para que Airflow inicialice

4. **Acceder a Airflow UI**
   - URL: http://localhost:8080
   - Usuario: `admin`
   - Contraseña: `admin`

5. **Ejecutar el DAG**
   - Activar el toggle de `job_etl_pipeline`
   - Click en "Trigger DAG" ▶️

### Detener el proyecto
docker-compose down## 📊 DAGs Disponibles

| DAG | Descripción | Schedule |
|-----|-------------|----------|
| `primer_dag_prueba` | DAG de prueba con un simple "Hola Mundo" | Diario |
| `job_etl_pipeline` | Pipeline ETL completo de trabajos remotos | Diario |

## 🔄 Flujo del ETL
Levantar los contenedores
   docker-compose up -dga trabajos desde Remotive API
2. **Transform**: Limpia y estructura los datos
3. **Load**: Genera archivo `jobs.csv`

## 🛠️ Tecnologías

- **Apache Airflow 2.9.0** - Orquestación de workflows
- **PostgreSQL 15** - Base de datos de metadatos
- **Docker & Docker Compose** - Contenedorización
- **Python 3.12** - Lenguaje de programación



## ✅ Estructura final

Airflow_Proyect/
├── dags/
│ ├── helpers/
│ │ ├── extract.py
│ │ ├── transform.py
│ │ └── load.py
│ ├── data/ # carpeta vacía o con .gitkeep
│ ├── job_etl_dag.py
│ └── primer_dag.py
├── plugins/ # puede estar vacía
├── docker-compose.yaml
├── requirements.txt
├── .gitignore
└── README.md

