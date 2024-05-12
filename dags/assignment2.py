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
from data_extraction import extract_dawn_links, extract_dawn_articles, extract_bbc_links, extract_bbc_articles
from data_transformation import preprocess_text, load_from_csv, save_to_csv
import os

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

# Initialize DVC in the project directory
init_dvc_task = PythonOperator(
    task_id='init_dvc',
    python_callable=os.system,
    op_args=['dvc init'],
    dag=dag
)

# Add Google Drive remote for DVC
add_gdrive_remote_task = PythonOperator(
    task_id='add_gdrive_remote',
    python_callable=os.system,
    op_args=['dvc remote add -d myremote https://drive.google.com/drive/folders/1kAgmTiMxzY-Pj9IPAxajhjMvhWV7f6zG?usp=drive_link --force'],
    dag=dag
)

# Task to extract links from Dawn.com
extract_dawn_links_task = PythonOperator(
    task_id='extract_dawn_links',
    python_callable=extract_dawn_links,
    dag=dag
)

# Task to extract articles from Dawn.com
extract_dawn_articles_task = PythonOperator(
    task_id='extract_dawn_articles',
    python_callable=extract_dawn_articles,
    dag=dag
)

# Task to extract links from BBC.com
extract_bbc_links_task = PythonOperator(
    task_id='extract_bbc_links',
    python_callable=extract_bbc_links,
    dag=dag
)

# Task to extract articles from BBC.com
extract_bbc_articles_task = PythonOperator(
    task_id='extract_bbc_articles',
    python_callable=extract_bbc_articles,
    dag=dag
)

# Update the task to preprocess Dawn.com articles to remove the usage of save_to_csv
preprocess_dawn_articles_task = PythonOperator(
    task_id='preprocess_dawn_articles',
    python_callable=preprocess_text,
    op_kwargs={'data': extract_dawn_articles()},  # Load directly from extraction
    dag=dag
)

# Update the task to preprocess BBC.com articles to remove the usage of save_to_csv
preprocess_bbc_articles_task = PythonOperator(
    task_id='preprocess_bbc_articles',
    python_callable=preprocess_text,
    op_kwargs={'data': extract_bbc_articles()},  # Load directly from extraction
    dag=dag
)

# Task to save preprocessed Dawn.com articles to CSV
# save_preprocessed_dawn_articles_task = PythonOperator(
#     task_id='save_preprocessed_dawn_articles',
#     python_callable=save_to_csv,
#     op_kwargs={'data': preprocess_dawn_articles_task.output, 'filename': 'preprocessed_dawn_articles.csv'},
#     dag=dag
# )

# Task to save preprocessed BBC.com articles to CSV
# save_preprocessed_bbc_articles_task = PythonOperator(
#     task_id='save_preprocessed_bbc_articles',
#     python_callable=save_to_csv,
#     op_kwargs={'data': preprocess_bbc_articles_task.output, 'filename': 'preprocessed_bbc_articles.csv'},
#     dag=dag
# )

# Define task dependencies
init_dvc_task >> add_gdrive_remote_task
add_gdrive_remote_task >> extract_dawn_links_task
add_gdrive_remote_task >> extract_bbc_links_task
extract_dawn_links_task >> extract_dawn_articles_task
extract_bbc_links_task >> extract_bbc_articles_task
extract_dawn_articles_task >> preprocess_dawn_articles_task
extract_bbc_articles_task >> preprocess_bbc_articles_task
# preprocess_dawn_articles_task >> save_preprocessed_dawn_articles_task
# preprocess_bbc_articles_task >> save_preprocessed_bbc_articles_task
