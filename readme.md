# 🌬️ Airflow ETL Pipeline - Remote Jobs

Pipeline de datos construido con **Apache Airflow** que extrae ofertas de trabajo remoto desde la API de [Remotive](https://remotive.com), las transforma, genera un archivo CSV limpio y visualiza los datos en un **Dashboard interactivo**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9.0-017CEE)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)

## 📁 Estructura del Proyecto

```
Airflow_Proyect/
├── dags/
│   ├── helpers/
│   │   ├── extract.py          # Extracción desde API
│   │   ├── transform.py        # Limpieza de datos
│   │   └── load.py             # Carga a CSV
│   ├── data/
│   │   ├── raw/                # JSON descargados (generado)
│   │   └── processed/          # CSV final (generado)
│   ├── job_etl_dag.py          # DAG principal del ETL
│   └── primer_dag.py           # DAG de prueba
├── dashboard/
│   ├── app.py                  # Aplicación Streamlit
│   ├── Dockerfile              # Imagen del dashboard
│   └── requirements.txt        # Dependencias del dashboard
├── plugins/                    # Plugins personalizados de Airflow
├── logs/                       # Logs de ejecución (generado)
├── docker-compose.yaml         # Configuración de Docker
├── requirements.txt            # Dependencias Python
├── .gitignore
└── README.md
```

## 🚀 Cómo Ejecutar

### Prerrequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Airflow_Proyect.git
   cd Airflow_Proyect
   ```

2. **Levantar los contenedores**
   ```bash
   docker-compose up -d --build
   ```

3. **Esperar 2-3 minutos** para que Airflow inicialice la base de datos

4. **Acceder a las aplicaciones**

   | Servicio | URL | Credenciales |
   |----------|-----|--------------|
   | **Airflow UI** | http://localhost:8080 | admin / admin |
   | **Dashboard** | http://localhost:8501 | - |

5. **Ejecutar el ETL**
   - En Airflow, activar el toggle de `job_etl_pipeline`
   - Click en "Trigger DAG" ▶️
   - Esperar a que termine (círculos verdes)
   - Ir al Dashboard para ver los resultados

### Detener el proyecto
```bash
docker-compose down
```

## 📊 DAGs Disponibles

| DAG | Descripción | Schedule |
|-----|-------------|----------|
| `primer_dag_prueba` | DAG de prueba con un simple "Hola Mundo" | Diario |
| `job_etl_pipeline` | Pipeline ETL completo de trabajos remotos | Diario |

## 🔄 Flujo del ETL

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Extract   │ ──▶ │  Transform   │ ──▶ │    Load     │
│  (API call) │     │  (Limpiar)   │     │   (CSV)     │
└─────────────┘     └──────────────┘     └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
   Remotive API      Filtrar campos      jobs.csv
   (JSON raw)        relevantes          (datos limpios)
```

1. **Extract**: Descarga trabajos remotos desde Remotive API
2. **Transform**: Limpia y estructura los datos (título, empresa, categoría, salario, fecha)
3. **Load**: Genera archivo `jobs.csv` listo para análisis

## 📈 Dashboard

El dashboard de Streamlit incluye:

- 📊 **Métricas generales**: Total de trabajos, con salario, empresas únicas
- 📁 **Gráfico de barras**: Trabajos por categoría
- 🏢 **Gráfico circular**: Top 10 empresas contratando
- 💰 **Análisis de salarios**: Distribución y comparación por categoría
- 📅 **Timeline**: Publicaciones por fecha
- 🔍 **Tabla interactiva**: Búsqueda y filtros en tiempo real

## 🛠️ Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Apache Airflow | 2.9.0 | Orquestación de workflows |
| PostgreSQL | 15 | Base de datos de metadatos |
| Streamlit | 1.29.0 | Dashboard interactivo |
| Plotly | 5.18.0 | Gráficos interactivos |
| Docker | - | Contenedorización |
| Python | 3.12 | Lenguaje principal |

## 📝 Comandos Útiles

```bash
# Ver estado de contenedores
docker ps

# Ver logs de Airflow
docker logs airflow_webserver --tail 50

# Ver logs del scheduler
docker logs airflow_scheduler --tail 50

# Reiniciar un servicio
docker-compose restart airflow

# Reconstruir el dashboard
docker-compose up -d --build dashboard
```

## 🗂️ Datos Generados

Después de ejecutar el ETL, encontrarás:

- `dags/data/raw/` - Archivos JSON crudos de la API
- `dags/data/processed/jobs.csv` - Datos limpios en CSV

Ejemplo de datos:
```csv
title,company,category,salary,url,pub_date
Senior Data Engineer,TechCorp,Software Development,$80k-$120k,https://...,2025-01-15
```

## 👩‍💻 Autora

**Camila**

---

⭐ Si te sirvió este proyecto, ¡dale una estrella!
