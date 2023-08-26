from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator

 with DAG (f"{parent_dag_id}.{child_dag_id}", 
        start_date = datetime(2013,8,25),
        schedule_intervals=@daily,
        catchup = False) as dag:
