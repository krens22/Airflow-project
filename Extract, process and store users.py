
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providors.http.sensors.http import HttpSensorfrom airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
from pandas import json_normalize

# Define a function to pull the data that has been downloaded by the task extract
def _process_user(ti):
    user = ti.xcom_pull(task_ids='extract_user')
    user = user['results'][0]
    processed_user = json_normalize({
        'firstname' : user['name']['first'],
        'lastname' : user['name']['last'],
        'username' : user['login']['username'],
        'password' : user['login']['password'],
        'email' : user['email']
    })
    processed_user.to_csv('tmp/processed_user.csv', index=None, header=False) 

#Define a function to interact with the postgres database using the postgres hook
def _store_user():
    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(
        sql = "COPY users FROM stdin WITH DELIMITER as ','",
        filename = '/tmp/processed_user.csv'
    )

#Define DAG
with DAG('user_processing', start_date=datetime(2023,8,24),
        schedule_interval='@daily', catchup=False) as dag:

#Add a sensor
is_api_available = HttpSensor(
        task_id = 'is_api_available',
        http_con_id = 'user_api',
        endpoint = 'api/',
        method='GET',
        
#Extract the user data from the API
extract_user = SimpleHttpOperator(
        task_id = 'extract_user',
        http_con_id = 'user_api',
        endpoint = 'api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text), #Extract the data and transform it in a Json format
        log_response = True
    )

#Process user data 
process_user = PythonOperator(
        task_id = 'process_user',
        python_callable = _process_user #Function
    )
#Store user data
store_user = PythonOperator(
    task_id = 'store_user'
    python_callable=_store_user
)


#Define dependancies in the correct order at the end of the dag file
#big-shift operator indicates that you want to execute create table first and then check if the API is available.
create_table >> is_api_available >> extract_user >> process_user >> store_user

#The final data pipeline would be visible in the graph view
