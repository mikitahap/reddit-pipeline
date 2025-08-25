from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from extract import Extractor
from transform import Transformer
from load import Loader

def extract_task(**kwargs):
    ti = kwargs['ti']
    extractor = Extractor()
    raw_data = extractor.extract()
    return raw_data

def transform_task(**kwargs):
    ti = kwargs['ti']
    transformer = Transformer(ti.xcom_pull(task_ids='extract_task', key='return_value'))
    modified_data = transformer.transform()
    return modified_data

def load_task(**kwargs):
    ti = kwargs['ti']
    loader = Loader(ti.xcom_pull(task_ids='transform_task', key='return_value'))
    loader.save_to_db()

with DAG(
    dag_id="etl_dag",
    start_date=datetime(2025, 8, 17),
    schedule = "@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="extract_task",
        python_callable=extract_task,
    )

    t2 = PythonOperator(
        task_id="transform_task",
        python_callable=transform_task,
    )

    t3 = PythonOperator(
        task_id="load_task",
        python_callable=load_task,
    )

    t1 >> t2 >> t3