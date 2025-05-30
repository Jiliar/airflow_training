from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Jiliar Silgado',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}
with DAG(
    dag_id='ex_movie_recommender',
    default_args=default_args,
    description='A simple dummy DAG for simulating movie recommender system',
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31),
    schedule='@monthly',
    tags=['Movie Recommender', 'Engineering']
) as dag:

    extract_internal_db_task = EmptyOperator(
        task_id='extract_internal_db_task',
        dag=dag
    )

    extract_external_api_task = EmptyOperator(
        task_id='extract_external_api_task',
        dag=dag
    )

    transform_data_task = EmptyOperator(
        task_id='transform_data_task',
        dag=dag
    )

    consumption_ml_model_task = EmptyOperator(
        task_id='consumption_ml_model_task',
        dag=dag
    )

    send_email_task = EmptyOperator(
        task_id='send_email_task',
        dag=dag
    )

    load_data_task = EmptyOperator(
        task_id='load_data_task',
        dag=dag
    )

    [extract_internal_db_task, extract_external_api_task] >> transform_data_task 
    transform_data_task  >> consumption_ml_model_task >> [send_email_task , load_data_task]