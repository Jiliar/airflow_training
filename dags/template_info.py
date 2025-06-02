from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    'owner': 'Jiliar Silgado',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

def print_context(**kwargs):
    for key, val in kwargs.items():
        print(f"Key - {key} - Value: {val} - Type: {type(val)}")

with DAG(
    dag_id='dag_template_info',
    default_args=default_args,
    description='A simple DAG to apply concepts related with templates',
    schedule=None,
    tags=['Example', 'Engineering']
) as dag:
    
    task_print_context = PythonOperator(
        task_id = 'task_print_context',
        python_callable=print_context
    )