from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

##task01
def data_preProcess():
    print("data preprocessed")

#task02
def train_data():
    print("mopdel training...")

#task03
def eval_data():
    print("data revaluating....")

# defining our dag
with DAG(
    'ml_pipelines',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@weekly',
) as dag:
    

    #defiing task
    preprocess=PythonOperator(task_id="preprocess_task", python_callable=data_preProcess)
    training=PythonOperator(task_id="train_data", python_callable=train_data)
    evaluation=PythonOperator(task_id="evaluate_data", python_callable=eval_data)

    ## set dependencies/order of execution
    preprocess >> training >> evaluation