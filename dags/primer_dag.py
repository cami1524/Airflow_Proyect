from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="primer_dag_prueba",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
):
    tarea = BashOperator(
        task_id="hola_mundo",
        bash_command="echo 'Hola Camila, Airflow funciona!'"
    )
