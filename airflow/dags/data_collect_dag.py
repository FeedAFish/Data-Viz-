import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add src directory to path to import custom modules
sys.path.insert(0, "/opt/airflow/src")

from collect.aqicn import collect_all
from db import insert_air_quality_records

# Define default arguments
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "start_date": datetime(2026, 3, 24),
}

# Define the DAG
dag = DAG(
    "update_air_quality_data",
    default_args=default_args,
    description="Update air quality data every 5 minutes",
    schedule_interval="*/5 * * * *",
    catchup=False,
)


# Define the task function
def print_hello_world():
    """Collect air quality data from all cities and insert into database."""
    print("Collecting air quality data...")
    records = collect_all()
    if records:
        insert_air_quality_records(records)
    else:
        print("No records collected.")


# Create a Python operator task
hello_task = PythonOperator(
    task_id="update_air_quality_data",
    python_callable=print_hello_world,
    dag=dag,
)
