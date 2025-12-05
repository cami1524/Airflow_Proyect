import json
from pathlib import Path

PROCESSED_DIR = Path("/opt/airflow/dags/data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def transform_jobs(raw_path):
    """
    Lee el JSON RAW y devuelve una lista limpia de trabajos.
    """
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    for job in data:
        cleaned.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "category": job.get("category"),
            "salary": job.get("salary"),
            "url": job.get("url"),
            "pub_date": job.get("publication_date"),
        })

    out = PROCESSED_DIR / "jobs_clean.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    return str(out)
