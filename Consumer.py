from airflow import DAG, Dataset
from airflow.decorators import task

#Define the dataset with the uri that will interact with the DAG
from datetime import date, datetime

my_file = Dataset('/tmp/my_file.txt')

#As soon as the prodecer DAG updated the dataset, my_file, that would trigger the Consumer DAG
with DAG(
        dag_id='consumer',
        schedule = [my_file],
        start_date = datetime(2023,8,24),
        catchup=False
#This task reads the updated dataset  
):
    @task
    def read_dataset():
        with open(my_file.uri, "r") as f:
            print(f.read())
    
    read_dataset()








