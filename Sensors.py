from airflow.providors.http.sensors.http import HttpSensor

#Adding a sensor to check if A URL is available or not
is_api_available = HttpSensor(
        task_id = 'is_api_available',
        http_con_id = 'user_api',
        endpoint = 'api/',
        method='GET'
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
