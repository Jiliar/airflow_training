from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta
from airflow.decorators import task_group
from components.functions.i_extract import IExtractData
from components.functions.extract.extract_data_functions import ExtractFunctions

from utils.config_loader import ConfigLoader

config_loader = ConfigLoader(f"dags/resources/config/marketing_analysis_gcp_prop.json")


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
gcp_conn_id = config_loader.get('gcp_conn_id')
headers = {'X-API-Key': api_key}
bucket = config_loader.get('bucket')
platforms = config_loader.get('platforms')
destination_template = config_loader.get('destination_template_path')
output_template = config_loader.get('output_template_file_path')
big_query_data_set = config_loader.get('bigquery_dataset')
schemas = config_loader.get('schemas')
sql_view_creation_file = config_loader.get('sql_view_creation_file')

@task_group(group_id='extract_platforms_data')
def extract_platform_data():
    for platform in platforms:
        formatted_output = output_template.format(platform=platform)
        extract_functions: IExtractData = ExtractFunctions(
            api_url.get(platform),
            api_key,
            None,
            formatted_output
        )
        PythonOperator(
            task_id=f'extract_data_task_{platform}',
            python_callable=extract_functions.get_api_python,
            op_args=[],
        )

@task_group(group_id='transfer_platforms_data_to_cloud_storage')
def transfer_platforms_data_to_cloud_storage():
    for platform in platforms:
        formatted_output = output_template.format(platform=platform)
        formatted_dst = destination_template.format(file=formatted_output).replace("/tmp/", "")

        LocalFilesystemToGCSOperator(
            task_id=f'transfer_to_cloud_storage_task_{platform}',
            src=formatted_output,
            dst=formatted_dst,
            bucket=bucket,
            gcp_conn_id=gcp_conn_id,
        )

@task_group(group_id='transfer_data_from_cloud_storage_to_big_query')
def transfer_data_from_cloud_storage_to_big_query():
    for platform in platforms:
        formatted_output = output_template.format(platform=platform)
        formatted_dst = destination_template.format(platform=platform, file=formatted_output).replace("/tmp/", "")
        schema_fields = schemas.get(platform)
        if not schema_fields:
            raise ValueError(f"No schema defined for platform: {platform}")
        
        GCSToBigQueryOperator(
            task_id=f'transfer_to_big_query_task_{platform}',
            bucket=bucket,
            source_objects=[formatted_dst],
            destination_project_dataset_table=f"{big_query_data_set}.{platform}",
            schema_fields=schema_fields,
            source_format='CSV',
            skip_leading_rows=1,
            write_disposition='WRITE_TRUNCATE',
            gcp_conn_id=gcp_conn_id,
        )

with DAG(
    dag_id='etl_marketing_analysis_gcp',
    default_args=default_args,
    description='Dag for ETL process of marketing process',
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31),
    schedule=None,
    tags=['Marketing', 'Engineering']
) as dag:
    
    start_task = PythonOperator(
        task_id='start_task',
        python_callable=lambda: print("Starting ETL process for marketing analysis"),
        dag=dag
    )

    end_task = PythonOperator(
        task_id='end_task',
        python_callable=lambda: print("ETL process for marketing analysis completed"),
        dag=dag
    )

    create_insights_view = BigQueryInsertJobOperator(
        task_id='create_insights_view',
        configuration={
            "query": {
                "query": sql_view_creation_file,
                "useLegacySql": False
            }
        },
        location="us-east1",
        dag = dag,
        gcp_conn_id=gcp_conn_id,
    )

    start_task >> extract_platform_data() >> transfer_platforms_data_to_cloud_storage() >> transfer_data_from_cloud_storage_to_big_query() >> create_insights_view >> end_task
