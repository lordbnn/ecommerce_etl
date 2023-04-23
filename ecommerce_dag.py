from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ecommerce_etl import scrape_jumia,clean_data,load_json_to_postgres

default_args = {
    'owner': 'byron',
    'start_date': datetime(2023, 4, 23),
    'retries': 1
}

dag = DAG('ecommerce_webscraping', default_args=default_args, schedule_interval='@daily')


ingest_data_task = PythonOperator(
    task_id='scrape_data',
    python_callable=scrape_jumia,
    dag=dag
)

transform_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag
)


load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_json_to_postgres,
    dag=dag
)

ingest_data_task >> transform_data_task >> load_data_task