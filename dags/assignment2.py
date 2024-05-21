import sys
import os

# Add the parent directory of 'dags' to Python's path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
print("Parent directory:", parent_dir)
sys.path.insert(0, parent_dir)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from data_scrapping import extract_dawn_articles, extract_bbc_articles, preprocess_text, save_to_csv

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_extraction_transformation',
    default_args=default_args,
    description='A DAG to extract and transform data from Dawn.com and BBC.com',
    schedule_interval='@daily',
    start_date=datetime(2024, 5, 1),
    catchup=False
)

# Function to combine extraction and preprocessing
def extract_and_preprocess():
    # Extract data
    dawn_articles = extract_dawn_articles()
    bbc_articles = extract_bbc_articles()

    # Combine articles from both sources
    all_articles = dawn_articles + bbc_articles

    # Apply preprocessing to all articles
    for article in all_articles:
        article['description'] = preprocess_text(article['description'])

    # Save preprocessed data to CSV
    save_to_csv(all_articles, 'final_preprocessed_articles.csv')

# Task to initialize DVC
init_dvc_task = PythonOperator(
    task_id='init_dvc',
    python_callable=os.system,
    op_args=['dvc init'],
    dag=dag
)

# Task to add Google Drive remote for DVC
add_gdrive_remote_task = PythonOperator(
    task_id='add_gdrive_remote',
    python_callable=os.system,
    op_args=['dvc remote add -d myremote https://drive.google.com/drive/folders/1kAgmTiMxzY-Pj9IPAxajhjMvhWV7f6zG?usp=drive_link --force'],
    dag=dag
)

# Task to extract and preprocess data
extract_and_preprocess_task = PythonOperator(
    task_id='extract_and_preprocess',
    python_callable=extract_and_preprocess,
    dag=dag
)

# Task to add the CSV file to DVC
def add_to_dvc():
    os.system('dvc add final_preprocessed_articles.csv')

add_to_dvc_task = PythonOperator(
    task_id='add_to_dvc',
    python_callable=add_to_dvc,
    dag=dag
)

# Task to commit the changes to DVC
def commit_dvc():
    os.system('dvc commit -m "Added final preprocessed articles"')

commit_dvc_task = PythonOperator(
    task_id='commit_dvc',
    python_callable=commit_dvc,
    dag=dag
)

# Task to push the changes to the remote DVC storage
def push_to_dvc():
    os.system('dvc push')

push_to_dvc_task = PythonOperator(
    task_id='push_to_dvc',
    python_callable=push_to_dvc,
    dag=dag
)

# Define task dependencies
init_dvc_task >> add_gdrive_remote_task >> extract_and_preprocess_task
extract_and_preprocess_task >> add_to_dvc_task >> commit_dvc_task >> push_to_dvc_task
