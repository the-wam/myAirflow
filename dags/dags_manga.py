# coding: utf-8

# import library airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago

# import library for time
from datetime import datetime, timedelta

# add path
import sys

sys.path.insert(0, "../code/")

# import my package
from extract import my_extract
from transforme import my_transforme
from load import my_load


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(0, 0, 0, 0),
    "email": ["toto.lapin.eu"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 10,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "manga",
    default_args=default_args,
    description="dag for ETL manga",
    schedule_interval="50 * * * *",
)


run_etl = PythonOperator(task_id="myextract", python_callable=my_extract, dag=dag)

transf = BranchPythonOperator(
    task_id="branching", python_callable=my_transforme, provide_context=True, dag=dag
)

continue1 = DummyOperator(task_id="continue", dag=dag)
Stop = DummyOperator(task_id="stop", dag=dag)


loadData = PythonOperator(task_id="loadData", python_callable=my_load, dag=dag)


alertLoic = EmailOperator(
    task_id="send_email",
    to="manoela.santidrian@gmail.com ",
    subject="Airflow Alert",
    html_content=""" <h3>Email Test</h3> """,
    dag=dag,
)


run_etl >> transf
transf >> [continue1, Stop]
continue1 >> loadData
loadData >> alertLoic
