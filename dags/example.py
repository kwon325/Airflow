from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

with DAG(
    dag_id='example_dag',
    schedule_interval='@daily',
    start_date=datetime(2024, 12, 1),
    catchup=False
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> end
