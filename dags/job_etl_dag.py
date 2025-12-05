from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from helpers.extract import extract_jobs
from helpers.transform import transform_jobs
from helpers.load import load_jobs_to_csv

default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def _transform_jobs(**kwargs):
    ti = kwargs['ti']
    raw_path = ti.xcom_pull(task_ids='extract_jobs')
    return transform_jobs(raw_path)

def _load_jobs(**kwargs):
    ti = kwargs['ti']
    clean_path = ti.xcom_pull(task_ids='transform_jobs')
    return load_jobs_to_csv(clean_path)

with DAG(
    dag_id="job_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args
):

    extract_task = PythonOperator(
        task_id="extract_jobs",
        python_callable=extract_jobs
    )

    transform_task = PythonOperator(
        task_id="transform_jobs",
        python_callable=_transform_jobs
    )

    load_task = PythonOperator(
        task_id="load_jobs_csv",
        python_callable=_load_jobs
    )

    extract_task >> transform_task >> load_task
