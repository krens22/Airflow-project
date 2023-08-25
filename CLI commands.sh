
docker-compose -f /Users/karenfernandes/Documents/Materials/airflow.apache.org_docs_apache-airflow_2.5.1_docker-compose.yaml ps

# To navigate the docker container where the scheduler of Airflow runs
docker exec -it materials-airflow-scheduler-1 /bin/bash 

# Lists all the commanda you can execute with CLI
airflow -h

# Run a single task instance on-demand, which can be useful for debugging and troubleshooting purposes.
airflow tasks test user_processing create_table 2023-08-24
