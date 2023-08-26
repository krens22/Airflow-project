# The producer DAG triggeres the dataset

from airflow import DAG, Dataset
from airflow.decorators import task

#Define the dataset with the uri that will interact with the DAG
from datetime import date, datetime

my_file = Dataset('/tmp/my_file.txt')

with DAG(
    dag_id='producer',
    schedule = "@daily",
    start_date = datetime(2023,8,24),
    cathup=False
):
#This task updates the dataset my_file
#As long as this DAG succeedes, the DAG that depends on this dataset i.e my_file, will be automatically be triggered
    @task(outlets=[my_file])
    def update_dataset():
        with open(my_file.url, "a+") as f:
            f.write("producer update")

update_dataset()
