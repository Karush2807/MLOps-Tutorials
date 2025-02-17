# ETL Pipelines (Extract, Transform, Load)

## Data Sources
The data can come from multiple sources:
1. **APIs**
2. **Internal Databases**
3. **IoT Devices**

## Role of a Data Engineer
A data engineer's role is to:
- Extract data from various sources.
- Perform preprocessing and transformation.
- Convert data to JSON format.
- Load the transformed data into a database (PostgreSQL, SQL, MongoDB).

## ETL Flow
```
APIs ---> Transform ---> JSON ---> Database (PostgreSQL, SQL, MongoDB)
```

## Using Apache Airflow for Scheduling
Since this ETL process needs to be scheduled periodically (e.g., weekly for data collection), we use **Apache Airflow** to automate and manage the workflow.

### Example Airflow DAG for ETL Process
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import psycopg2

def extract():
    url = "https://api.example.com/data"
    response = requests.get(url)
    data = response.json()
    with open("/tmp/raw_data.json", "w") as f:
        json.dump(data, f)

def transform():
    with open("/tmp/raw_data.json", "r") as f:
        data = json.load(f)
    transformed_data = [{"id": d["id"], "value": d["value"]} for d in data]
    with open("/tmp/transformed_data.json", "w") as f:
        json.dump(transformed_data, f)

def load():
    conn = psycopg2.connect(
        dbname="mydb", user="user", password="password", host="localhost", port="5432"
    )
    cursor = conn.cursor()
    with open("/tmp/transformed_data.json", "r") as f:
        data = json.load(f)
    for row in data:
        cursor.execute("INSERT INTO my_table (id, value) VALUES (%s, %s)", (row["id"], row["value"]))
    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "etl_pipeline",
    default_args=default_args,
    schedule_interval="@weekly",
    catchup=False,
)

extract_task = PythonOperator(task_id="extract", python_callable=extract, dag=dag)
transform_task = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
load_task = PythonOperator(task_id="load", python_callable=load, dag=dag)

extract_task >> transform_task >> load_task
