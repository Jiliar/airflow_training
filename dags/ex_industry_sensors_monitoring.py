from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.decorators import task_group

default_args = {
    'owner': 'Jiliar Silgado',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}


@task_group(group_id='extract_sensor_data_group')
def extract_sensor_data():
    list_sensors = [f"sensor_{i}" for i in range(1, 31)]
    for sensor in list_sensors:
        extract_task = PythonOperator(
            task_id=f'extract_{sensor}_task',
            python_callable=lambda sensor_name: print(f"Extracting data from {sensor_name}"),
            op_args=[sensor],
            dag=dag
        )
    return extract_task


with DAG(
    dag_id='ex_industry_sensors_monitoring',
    default_args=default_args,
    description='A simple dummy DAG for simulating sensors monitoring in an industry',
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31),
    schedule='@weekly',
    tags=['Industry Sensors', 'Engineering']
) as dag:
    
    start_task = EmptyOperator(
        task_id='start_task',
        dag=dag
    )

    data_base_ingestion_task = EmptyOperator(
        task_id='data_base_ingestion_task',
        dag=dag
    )
    transform_data_task = EmptyOperator(
        task_id='transform_data_task',
        dag=dag
    )
    data_analysis_task = EmptyOperator(
        task_id='data_analysis_task',
        dag=dag
    )
    alerting_task = EmptyOperator(
        task_id='alerting_task',
        dag=dag
    )
    update_dashboard_task = EmptyOperator(
        task_id='update_dashboard_task',
        dag=dag
    )

    end_task = EmptyOperator(
        task_id='end_task',
        dag=dag
    )
    start_task >> extract_sensor_data() >> data_base_ingestion_task
    data_base_ingestion_task >> transform_data_task >> data_analysis_task
    data_analysis_task >> [alerting_task, update_dashboard_task] >> end_task
