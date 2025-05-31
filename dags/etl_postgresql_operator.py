import sys
import os

dags_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(dags_dir)
sys.path.append(project_root)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from components.functions.i_extract import IExtractData
from components.functions.extract.extract_data_functions import ExtractFunctions

from components.functions.i_transform import IBaseDataTransformer
from components.functions.transform.sales_data_transformer import SalesDataTransformer

from components.functions.i_load import ILoader
from components.functions.load.postgresql_loader import PostgresLoader

from utils.config_loader import ConfigLoader

config_loader = ConfigLoader(f"dags/resources/config/postgresql_operator_prop.json")

# Configure logging
default_args = {
    'owner': config_loader.get('owner', 'airflow'),
    'depends_on_past': config_loader.get('depends_on_past', False),
    'email_on_failure': config_loader.get('email_on_failure', False),
    'email_on_retry': config_loader.get('email_on_retry', False),
    'retries': config_loader.get('retries', 1),
    'retry_delay': timedelta(minutes=config_loader.get('retry_delay_minutes', 2))
}

# Define constants
api_url = config_loader.get('api_url')
api_key = config_loader.get('api_key')
output_path_bash = config_loader.get('output_path_bash')
output_path_python = config_loader.get('output_path_python')
output_path_transform = config_loader.get('output_path_transform')
conn_id = config_loader.get('conn_id')
sql_creation_file = config_loader.get('sql_creation_file')
table_name = config_loader.get('table_name')
headers = {'X-API-Key': api_key}

with DAG(
    dag_id='dag_etl_postgresql_operator',
    default_args=default_args,
    description='DAG ETL for PostgreSQL',
    start_date=datetime(2025, 5, 28),
    schedule=None,
    tags=['ETL', 'Engineering', 'PostgreSQL']
) as dag:

    # Initialize extract and transform functions
    extract_functions: IExtractData = ExtractFunctions(
        api_url,
        api_key,
        output_path_bash,
        output_path_python
    )

    transform_functions : IBaseDataTransformer = SalesDataTransformer(
        input_path_bash=output_path_bash,
        input_path_py=output_path_python,
        output_path=output_path_transform
    )

    loader : ILoader = PostgresLoader(conn_id, table_name, output_path_transform)

    # Define tasks
    get_api_python_task = PythonOperator(
        task_id='get_api_python',
        python_callable=extract_functions.get_api_python,
        dag=dag
    )
    
    get_api_bash_task = BashOperator(
        task_id='get_api_bash',
        bash_command=extract_functions.get_api_bash_command(),
        dag=dag
    )

    join_transform_task = PythonOperator(
        task_id='join_transform',
        python_callable=transform_functions.transform,
        dag=dag
    )

    check_exists_and_create_table = SQLExecuteQueryOperator(
        task_id='check_table_exists',
        conn_id= conn_id,
        sql=sql_creation_file,
        dag=dag
    )

    load_data_postgresql_task = PythonOperator(
        task_id='load_data_postgresql',
        python_callable=loader.load,
        op_kwargs={
            'conn_id': conn_id,
            'table': table_name,
            'csv_file': output_path_transform
        },
        dag=dag
    )

[ get_api_python_task, get_api_bash_task ] >> check_exists_and_create_table >> join_transform_task >> load_data_postgresql_task