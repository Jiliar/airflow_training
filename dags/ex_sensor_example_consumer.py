from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
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
    dag_id='DAG_Analitica_MKT',
    default_args=default_args,
    description='A simple DAG to apply concepts related with sensors [Consumer]',
    schedule=None,
    tags=['Example', 'Engineering']
) as dag:
    start = EmptyOperator(task_id = 'start')
    db_ventas_row_task = ExternalTaskSensor(
        task_id = 'db_ventas_row',
        external_dag_id = 'DAG_Ventas',
        external_task_id = 'transform_2',
        allowed_states=['success'] 
    )
    mkt_data_task = EmptyOperator(task_id = 'mkt_data')
    join_transform = EmptyOperator(task_id = 'join_transform')
    ingest = EmptyOperator(task_id = 'ingest')
    
    end = EmptyOperator(task_id='end')
    start >> [db_ventas_row_task, mkt_data_task] >> join_transform >> ingest >> end