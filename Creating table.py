#Creating a table of users

from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator

#Define DAG
with DAG('user_processing', start_date=datetime(2023,8,24),
        schedule_interval='@daily', catchup=False) as dag:
          
#The postgres operator is used to execute a SQL request against a postgres database and create a table
          
    create_table = PostgresOperator(
        task_id='create_table', # Unique task idenifier
        postgres_conn_id='postgres', # id of the connection 
        sql=''' 
            CREATE TABLE IF NOT EXISTS users (
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    country TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL
                );
        '''

        )
# A postrgres connection must be created in the Airflow UI
