from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag_downloads import subdag_downloads
 
from datetime import datetime
 
with DAG('group_dag', start_date=datetime(2023, 8, 26), 
    schedule_interval='@daily', catchup=False) as dag:
    args = {'start_date': dag.start_date, 'schedule_interval': dag.schedule_interval, 'catchup':dag.catchup}

# All the tasks get replaced with the subdag operator
    downloads = SubDagOperator(
      task_id='donwloads',
      subdag=subdag_downloads(dag.dag_id,'downloads',args))
#The task ID of the subdag operator must be used as the DAG ID of your sub DAG      
 
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
 
    transform_a = BashOperator(
        task_id='transform_a',
        bash_command='sleep 10'
    )
 
    transform_b = BashOperator(
        task_id='transform_b',
        bash_command='sleep 10'
    )
 
    transform_c = BashOperator(
        task_id='transform_c',
        bash_command='sleep 10'
    )
 
   downloads >> check_files >> [transform_a, transform_b, transform_c]
