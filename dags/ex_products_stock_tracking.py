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
    dag_id='ex_products_stock_tracking',
    default_args=default_args,
    description='A simple dummy DAG for simulating movie recommender system',
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31),
    schedule=None,
    tags=['Product Stock', 'Engineering']
) as dag:
    
    products_sales_task = EmptyOperator(
        task_id='sell_products_task',
        dag=dag
    )
    product_stock_task = EmptyOperator(
        task_id='product_stock_task',
        dag=dag
    )
    products_shopping_task = EmptyOperator(
        task_id='buy_products_task',
        dag=dag
    )
    transform_data_task = EmptyOperator(
        task_id='transform_data_task',
        dag=dag
    )
    predict_product_stock_task = EmptyOperator(
        task_id='predict_product_stock_task',
        dag=dag
    )
    update_data_base_task = EmptyOperator(
        task_id='update_data_base_task',
        dag=dag
    )
    send_email_task = EmptyOperator(
        task_id='send_email_task',
        dag=dag
    )

    [products_sales_task, products_shopping_task, product_stock_task] >> transform_data_task
    transform_data_task >> predict_product_stock_task
    predict_product_stock_task >> [update_data_base_task, send_email_task]
