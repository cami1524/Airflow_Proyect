import requests
from pathlib import Path
import json
from datetime import datetime

RAW_DIR = Path("/opt/airflow/dags/data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def extract_jobs(search="python"):
    """
    Descarga trabajos remotos desde la API de Remotive.
    Guarda el archivo JSON RAW.
    """
    url = "https://remotive.com/api/remote-jobs"
    params = {"search": search}

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json().get("jobs", [])

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    fname = RAW_DIR / f"jobs_raw_{ts}.json"

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(fname)
