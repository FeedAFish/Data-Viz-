import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add dags directory to path so src modules can be imported
# Works both locally and in Docker
dags_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dags_dir)

from src.collect.aqicn import collect_all_air
from src.collect.meteo import collect_all_meteo
from src.db import insert_air_quality_records
from src.db import insert_meteo_records

# Define default arguments
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "start_date": datetime(2026, 5, 24),
}

# Define the DAG
dag = DAG(
    "update_air_quality_data",
    default_args=default_args,
    description="Update air quality data every hour at 5 minutes past",
    schedule_interval="5 * * * *",
    catchup=False,
)


# Define the task function
def collect_and_insert_air_quality_data():
    records = collect_all_air()
    if records:
        insert_air_quality_records(records)
    else:
        print("No records collected.")


def collect_and_insert_meteo_data():
    records = collect_all_meteo()
    if records:
        insert_meteo_records(records)
    else:
        print("No records collected.")


# Create a Python operator task
air_collect_dag = PythonOperator(
    task_id="update_air_quality_data",
    python_callable=collect_and_insert_air_quality_data,
    dag=dag,
)

meteo_collect_dag = PythonOperator(
    task_id="update_meteo_data",
    python_callable=collect_and_insert_meteo_data,
    dag=dag,
)

air_collect_dag >> meteo_collect_dag
