from airflow.providors.http.sensors.http import HttpSensor

#Adding a sensor to check if A URL is available or not
is_api_available = HttpSensor(
        task_id = 'is_api_available',
        http_con_id = 'user_api',
        endpoint = 'api/',
        method='GET'
)
