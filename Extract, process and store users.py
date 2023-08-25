from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import json
from pandas import json_normalize
from airflow.providers.postgres.hooks.postgres import PostgresHook

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
