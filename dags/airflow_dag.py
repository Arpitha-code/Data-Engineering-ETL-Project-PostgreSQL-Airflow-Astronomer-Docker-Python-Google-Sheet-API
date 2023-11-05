from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python_operator import PythonOperator
from write_data_to_postgres import write_gsheet_data_to_postgres
from write_summarized_data_to_postgres import write_summarized_data_to_google_sheet

# Define default DAG arguments
default_args = {
    'owner': 'Arpitha Jagadish',
    'start_date': datetime(2023,11,1),
    'retries': 2,
    'retry_delay': timedelta(seconds=5)
}

# Create the DAG 'etl_gsheet_data_to_postgres' with the specified default arguments and schedule interval
with DAG('etl_gsheet_data_to_postgres', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    # Define the 'start_task' as an empty task to represent the start of the DAG
    start_of_etl = EmptyOperator(task_id='start_of_etl')

    # Define the 'extract_and_upsert_to_postgres' task
    extract_and_upsert_to_postgres = PythonOperator(
        task_id='extract_and_upsert_to_postgres',
        python_callable=write_gsheet_data_to_postgres,
        retries=2,
        retry_delay=timedelta(seconds=10))
    
    # Define the 'extract_transform_and_load_to_google_sheet' task
    extract_transform_and_load_to_google_sheet = PythonOperator(
        task_id='extract_transform_and_load_to_google_sheet',
        python_callable=write_summarized_data_to_google_sheet,
        retries=2,
        retry_delay=timedelta(seconds=10))
    
    # Define the 'end_of_etl' as an empty task to represent the end of the DAG
    end_of_etl = EmptyOperator(task_id='end_of_etl')
    
    # Set task dependencies: extract_and_upsert_to_postgres runs before extract_transform_and_load_to_google_sheet
    start_of_etl >> extract_and_upsert_to_postgres >> extract_transform_and_load_to_google_sheet >> end_of_etl