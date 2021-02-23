# coding: utf-8

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago

import json

from datetime import datetime, timedelta

import logging

import os

import sys
sys.path.insert(0, "../code/")

from extract import myextract
from transforme import mytransforme
from load import myload

def saveFile():
    # path = "/home/thewam/airflow_kafka_mongoDB/airflow/code"
    # with open(f"{path}test.txt", "w") as f:
    #     json.dump([path], f)
    print(sys.path)
    logging.waring(sys.path)

default_args = {
    'owner': "airflow",
    'depends_on_past' : False,
    'start_date' : days_ago(0,0,0,0),
    'email': ["toto.lapin.eu"],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 10,
    'retry_delay' : timedelta(minutes=1)
}

dag = DAG(
    'manga',
    default_args= default_args,
    description= 'dag for ETL manga',
    schedule_interval='50 * * * *'
)


# def myextract():
#     logging.info('extract')
#     return 0

run_etl = PythonOperator(
    task_id="myextract",
    python_callable=myextract,
    dag=dag
    )


# def mytransforme():

#     res = random.choice(["continue", "Stop"])
#     logging.info(res)
#     #saveFile()
#     return res


transf = BranchPythonOperator(
    task_id="branching",
    python_callable=mytransforme,
    provide_context=True,
    dag=dag
)

continue1 = DummyOperator(task_id='continue', dag=dag)
Stop = DummyOperator(task_id='stop', dag=dag)

# def myload():
#     logging.info("load")
#     return 2


loadData = PythonOperator(
    task_id="loadData",
    python_callable= myload,
    dag=dag
    )


alertLoic = EmailOperator(
        task_id='send_email',
        to='manoela.santidrian@gmail.com ',
        subject='Airflow Alert',
        html_content=""" <h3>Email Test</h3> """,
        dag=dag
)


run_etl >> transf
transf >> [continue1, Stop]
continue1 >> loadData
loadData >> alertLoic