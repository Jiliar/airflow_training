from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Jiliar Silgado',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

def _extract_data_1():
    print("Extracting data 1")

def _extract_data_2():
    print("Extracting data 2")
    raise ValueError("Simulated failure in extract_data_2")


with DAG(
    dag_id='trigger_rules_dag',
    default_args=default_args,
    description='A simple dummy DAG for simulating trigger rules',
    start_date=datetime(2025, 5, 29),
    schedule=None,
    tags=['Triggers Rules', 'Engineering']
) as dag:
    
    start_task = EmptyOperator(task_id='start_task')

    extract1 = PythonOperator(
        task_id='extract1',
        python_callable=_extract_data_1,
        dag=dag
    )
    extract2 = PythonOperator(
        task_id='extract2',
        python_callable=_extract_data_2,
        dag=dag
    )

    #Trigger rule:
    #end_task = EmptyOperator(task_id='end_task')
    #one_sucess
    end_task = PythonOperator(
        task_id='end_task',
        python_callable=lambda: print("End task executed after one success"),
        trigger_rule='one_success',
        dag=dag
    )

    start_task >> [extract1, extract2] >> end_task
