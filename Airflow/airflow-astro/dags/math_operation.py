## defining a tag where the task are as followed: 
# 1. start with a number
# 2. add 5 to it
# 3. mutilply the result by 2
# 4. subtract 3 from result5. 
# 5. compute the square of the result

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# define funciton for each task

def start_time(**context):
    context["ti"].xcom_push(key='current_value', value=10)
    print("starting number 10")

def add_five(**context):
    current_val=context["ti"].xcom_pull(key='current_value', task_ids='start_task')
    new_val=current_val + 5 #this current val will come from contex
    context["ti"].xcom_push(key='current_value', value=new_val)
    print(f"add 5: {current_val}+5={new_val}")

def multiply_by2(**context):
    current_val=context["ti"].xcom_pull(key="current_value", task_ids='add5_task')
    new_val=current_val * 2
    context["ti"].xcom_push(key='current_value', value=new_val)
    print(f"multiply 2: {current_val}*2={new_val}")


def sub3(**context):
    current_val=context["ti"].xcom_pull(key="current_value", task_ids='multiply2_task')
    new_val=current_val-3
    context["ti"].xcom_push(key='current_value', value=new_val)
    print(f"subtract 3: {current_val}-3={new_val}")

def power2(**context):
    current_val=context["ti"].xcom_pull(key="current_value", task_ids='sub3_Task')
    new_val=current_val**2
    context["ti"].xcom_push(key='current_value', value=new_val)
    print(f"subtract 3: {current_val}^2={new_val}")

#defing the dag
with DAG(
    dag_id='math_sequence_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@once',
)as dag:
    
    #definng tasks
    start_task=PythonOperator(
        task_id='start_task',
        python_callable=start_time, 
        provide_context=True
    )

    add5_task=PythonOperator(
        task_id='add5_task', 
        python_callable=add_five,
        provide_context=True
    )

    multiply2_task = PythonOperator(
        task_id='multiply2_task',
        python_callable=multiply_by2, 
        provide_context=True
    )

    sub3_task=PythonOperator(
        task_id='sub3_Task', 
        python_callable=sub3, 
        provide_context=True
    )

    pow2_task=PythonOperator(
        task_id='pow2_task', 
        python_callable=sub3, 
        provide_context=True
    )

    #setting order of execution
    start_task >> add5_task >> multiply2_task >> sub3_task >> pow2_task

