from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator

default_args = {
    'owner': 'Jiliar Silgado',
    'start_date': datetime(2025, 6, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

with DAG(
    dag_id='DAG_Ventas',
    default_args=default_args,
    description='A simple DAG to apply concepts related with sensors [Creator]',
    schedule='@daily',
    tags=['Example', 'Engineering']
) as dag:
    
    start = EmptyOperator(task_id = 'start')
    extract_db = EmptyOperator(task_id = 'extract_db')
    transform_1 = EmptyOperator(task_id = 'transform_1')
    transform_2 = BashOperator(
        task_id = 'transform_2',
        bash_command = 'sleep 5'
    )
    ingest_1 = EmptyOperator(task_id = 'ingest1')
    ingest_2 = EmptyOperator(task_id = 'ingest2')
    end = EmptyOperator(task_id='end')

    start >> extract_db >> [transform_1, transform_2]
    transform_1 >> ingest_1
    transform_2 >> ingest_2
    [ingest_1, ingest_2] >> end