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
    dag_id='ex_social_networks_analysis',
    default_args=default_args,
    description='A simple dummy DAG for simulating social networks analysis for fashion brand',
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31),
    schedule=None,
    tags=['Social Networks', 'Fashion Brands', 'Engineering']
) as dag:
    
    extract_facebook_api_task = EmptyOperator(
        task_id='extract_facebook_api_task',
        dag=dag
    )
    extract_instagram_api_task = EmptyOperator(
        task_id='extract_instagram_api_task',
        dag=dag
    )
    extract_twitter_api_task = EmptyOperator(
        task_id='extract_twitter_api_task',
        dag=dag
    )
    transform_data_task = EmptyOperator(
        task_id='transform_data_task',
        dag=dag
    )
    nlp_predict_sentiment_task = EmptyOperator(
        task_id='predict_sentiment_task',
        dag=dag
    )
    ingest_data_task = EmptyOperator(
        task_id='ingest_data_task',
        dag=dag
    )

    [extract_facebook_api_task, extract_instagram_api_task, extract_twitter_api_task] >> transform_data_task
    transform_data_task >> nlp_predict_sentiment_task >> ingest_data_task