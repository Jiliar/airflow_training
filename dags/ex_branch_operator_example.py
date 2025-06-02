import random
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator

default_args = {
    'owner': 'Jiliar Silgado',
    'start_date': datetime(2025, 6, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

def _extract():
    print('Extracting Data...')
    print('Counting Data...')
    return random.randing(0,10)

def _branch(**kwargs):
    ti = kwargs['ti']
    row = ti.xcom_pull(trask_ids='extract')
    if row > 5:
        return 'transform1'
    return 'predict_lost_data'


with DAG(
    dag_id='ex_branch_operator_test',
    default_args=default_args,
    description='A simple DAG to apply concepts related with branch operators',
    schedule='@daily',
    tags=['Example', 'Engineering']
) as dag:
    start = EmptyOperator(task_id = 'start')
    extract = PythonOperator(
        task_id = 'extract',
        python_callable=_extract
    )
    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=_branch
    )
    transform_1 = EmptyOperator(task_id = 'transform_1')
    transform_2 = EmptyOperator(task_id = 'transform_2')
    predict_lost_data = EmptyOperator(task_id = 'predict_lost_data')
    ingest = EmptyOperator(task_id = 'join_ingest',
                                triger_rule='one_success')
    end = EmptyOperator(task_id='end')

    start >> extract >> branch_task
    branch_task >> transform_1
    branch_task >> predict_lost_data >> transform_2
    [transform_1, transform_2] >> ingest >> end