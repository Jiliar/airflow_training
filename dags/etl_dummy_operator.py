from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from datetime import datetime

default_args = {
    'owner': 'Jiliar Silgado',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

with DAG(
    dag_id='dag_etl_dummy_operator',
    default_args=default_args,
    description='A simple dummy operator DAG',
    start_date=datetime(2025, 5, 28),
    schedule=None,
    tags=['ETL', 'Engineering']
) as dag:

    get_api_bash = EmptyOperator(task_id='get_api_bash')
    get_api_python = EmptyOperator(task_id='get_api_python')
    join_transform = EmptyOperator(task_id='join_transform')
    load_data_postgresql = EmptyOperator(task_id='load_data_postgresql')

    [ get_api_bash, get_api_python ] >> join_transform >> load_data_postgresql