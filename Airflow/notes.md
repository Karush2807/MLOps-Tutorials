## Apache-Airflow

1. open-source platform to programatically author, schedule and monitor all the workflows ( basically jo hmare workflows hote hai unhe dev se execution tk manage krne mein help krta hai )

2. used for data pipelines, across multiple platforms

**key concepts of apache airflow**

- DAG ( directed acylic graph ): collection of tests we want to schedule and run [directed-> ek specific sequence hona chahiye tasks ka], [acylic--> koi bhi task independent nhi hone chahiye]

- TASKS: individual unit of work in dag for eg-: python funciton, querying a database, sending a http request

3. Dependencies: taks in dag have dependecoes/fixed order which allow us to control the order of execution, airflow provides mechanisms like sewt_upstream and set_downstream to define these


**why AIRFLOW for MLOPS?**
it allow us to deine, automate, and monitor every step in ML pipeline

- orchestrating ml pipepline and etl pipeline
- task automation
- monitoring and alerts

Airflow allows us to define, automate, and monitor every step in an ML pipeline. It provides:

1. Orchestration of ML Pipelines & ETL Pipelines

Automates the flow of data preprocessing, model training, evaluation, and deployment.

Ensures that different stages execute in the correct order.

2. Task Automation

Helps automate repetitive ML tasks such as data ingestion, feature engineering, and retraining models.

Supports running ML tasks in parallel to improve efficiency.

3. Monitoring & Alerts

Provides real-time monitoring of workflows.

Enables alerts and notifications in case of failures or bottlenecks.

4. Integration with ML Frameworks

Easily integrates with TensorFlow, PyTorch, Scikit-learn, Spark, and other ML frameworks.

Works with cloud platforms like AWS, GCP, and Azure for large-scale ML model training and deployment.

5. Scalability & Flexibility

Supports dynamic DAG generation, making it adaptable to different ML workflows.

Can scale horizontally to handle large ML workloads efficiently.