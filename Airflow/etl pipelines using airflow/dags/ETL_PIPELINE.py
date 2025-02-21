from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json

# Define the DAG with daily schedule
# catchup=False means it won't try to backfill missed runs
with DAG(
    dag_id='nasaAPOD_postgres', 
    start_date=days_ago(1), 
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    @task
    def create_table():
        """
        Creates the PostgreSQL table if it doesn't exist.
        Uses the PostgresHook to connect to the database and execute the DDL.
        """
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        
        # SQL to create table matching NASA APOD API response structure
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS apod_data(
                id SERIAL PRIMARY KEY,           -- Auto-incrementing ID
                title VARCHAR(255),              -- Title of the astronomy picture
                explanation TEXT,                -- Detailed explanation of the picture
                url TEXT,                        -- URL to the image
                date DATE,                       -- Date of the picture
                media_type VARCHAR(50)           -- Type of media (image/video)
            );
        '''
        postgres_hook.run(create_table_query)

    # Task to fetch data from NASA's APOD API
    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',                # Connection containing NASA API credentials
        endpoint='planetary/apod',              # NASA APOD API endpoint
        method='GET',
        # Get API key from Airflow connection's extra field
        data={"api_key": "{{conn.nasa_api.extra_dejson.api_key}}"},
        # Convert API response to JSON
        response_filter=lambda response: json.loads(response.text),
    )

    @task
    def transform_apod_data(response):
        """
        Transforms the API response by selecting and structuring required fields.
        
        Args:
            response (dict): Raw API response from NASA APOD
            
        Returns:
            dict: Transformed data with selected fields
        """
        return {
            'title': response.get('title', ''),          # Get title or empty string if missing
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }

    @task
    def load_data_to_postgres(apod_data):
        """
        Loads the transformed data into PostgreSQL database.
        
        Args:
            apod_data (dict): Transformed APOD data ready for insertion
        """
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        
        # SQL to insert data into the apod_data table
        insert_query = '''
            INSERT INTO apod_data (
                title,
                explanation,
                url,
                date,
                media_type
            ) VALUES (%s, %s, %s, %s, %s);
        '''
        
        # Execute insert with parameters from transformed data
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type'],
        ))

    # Define task instances
    create_table_task = create_table()
    extract_task = extract_apod
    transform_task = transform_apod_data(extract_task.output)
    load_task = load_data_to_postgres(transform_task)

    # Set up task dependencies (workflow)
    # create_table -> extract_apod -> transform_data -> load_data
    create_table_task >> extract_task >> transform_task >> load_task