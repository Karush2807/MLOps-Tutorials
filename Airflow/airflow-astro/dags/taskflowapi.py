from airflow import DAG
from airflow.decorators import task
from datetime import datetime

##define the dag

with DAG(
    dag_id='math_Sequence_withTASKFLOW', 
    start_date=datetime(2024, 1, 1),
    schedule='@monthly',
    catchup=False,
) as dag:
    
    #task1: start with initial number
    @task
    def start_number():
        initial_val=10
        print(f"starting_number: {initial_val}")
        return initial_val
    
    #task2: adding 5 to a  number
    @task
    def add_five(number):
        new_val=number+5
        print(f"add 5: {number}={new_val}")
        return new_val
    
    @task
    def multiply2(number):
        new_val=number*2
        print(f"multiply 2: {number}={new_val}")
        return new_val
    
    @task
    def sub_three(number):
        new_val=number-3
        print(f"subtract 3 - {number}={new_val}")
        return new_val
    
    @task
    def pow_2(number):
        new_val=number**2
        print(f"{number}^2= {new_val}")
        return new_val
    
    ##setting task dependencies
    start_value=start_number()
    added_values=add_five(start_value)
    multiplied_values=multiply2(added_values)
    subtracted_values=sub_three(multiplied_values)
    exponential_values=pow_2(subtracted_values)