import csv
import json
from pathlib import Path

OUTPUT = Path("/opt/airflow/dags/data/processed/jobs.csv")

def load_jobs_to_csv(clean_path):
    """
    Convierte JSON limpio en CSV.
    """
    with open(clean_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "company", "category", "salary", "url", "pub_date"])

        for row in data:
            writer.writerow([
                row["title"],
                row["company"],
                row["category"],
                row["salary"],
                row["url"],
                row["pub_date"],
            ])

    return str(OUTPUT)
