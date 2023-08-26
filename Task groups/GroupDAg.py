from airflow import DAG
from airflow.operators.bash import BashOperator
from group.group_downloads import download_tasks
#Remove
#from airflow.operators.subdag import SubDagOperator
from subdags.subdag_downloads import subdag_downloads
from subdags.subdag_transforms import subdag_transforms
from datetime import datetime

with DAG('group_dag', start_date=datetime(2023, 8, 26), 
    schedule_interval='@daily', catchup=False) as dag:
    args = {'start_date': dag.start_date, 'schedule_interval': dag.schedule_interval, 'catchup':dag.catchup}

# All the tasks get replaced with the subdag operator for download tasks

    downloads = download_tasks()
#The task ID of the subdag operator must be used as the DAG ID of your sub DAG      

    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
    
    #transform = transform_tasks()
downloads >> check_files #>> transform
