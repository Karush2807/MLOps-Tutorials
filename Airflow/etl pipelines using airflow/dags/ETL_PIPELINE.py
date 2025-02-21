from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json
from airflow.hooks.base import BaseHook



## Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False

) as dag:
    
    ## step 1: Create the table if it doesnt exists

    @task
    def create_table():
        ## initialize the Postgreshook
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")

        ## SQL query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );


        """
        ## Execute the table creation query
        postgres_hook.run(create_table_query)


    # Fetch API key from Airflow connection
    conn = BaseHook.get_connection('nasa_api')
    api_key = conn.extra_dejson.get('api_key')
    ## Step 2: Extract the NASA API Data(APOD)-Astronomy Picture of the Day[Extract pipeline]
    ## https://api.nasa.gov/planetary/apod?api_key=8GGvuDfuk4F0nVg9QMntjRaX0I8YS8AYH5pADuop 
    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={"api_key": api_key},  # Pass API key here
        log_response=True
    )

    

    ## Step 3: Transform the data(Pick the information that i need to save)
    @task
    def transform_apod_data(response):
    # Parse the response string into a dictionary
        response_dict = json.loads(response)

        apod_data = {
            'title': response_dict.get('title', ''),
            'explanation': response_dict.get('explanation', ''),
            'url': response_dict.get('url', ''),
            'date': response_dict.get('date', ''),
            'media_type': response_dict.get('media_type', '')
        }
        return apod_data


    ## step 4:  Load the data into Postgres SQL
    @task
    def load_data_to_postgres(apod_data):
        ## Initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        ## Define the SQL Insert Query

        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """

        ## Execute the SQL Query

        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']


        ))



    ## step 5: Verify the data DBViewer


    ## step 6: Define the task dependencies
    ## Extract
    create_table() >> extract_apod  ## Ensure the table is create befor extraction
    api_response=extract_apod.output
    ## Transform
    transformed_data=transform_apod_data(api_response)
    ## Load
    load_data_to_postgres(transformed_data)