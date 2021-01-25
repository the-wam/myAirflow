
# coding: utf-8

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

import logging

default_args = {
    'owner': "airflow",
    'depends_on_past' : False,
    'start_date' : days_ago(0,0,0,0),
    'email': ["toto.lapin.eu"],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay' : timedelta(minutes=1)
}

dag = DAG(
    'manga',
    default_args= default_args,
    description= 'dag for ETL manga',
    schedule_interval='1 * * * *'
)


def myextract():
    logging.info('extract')
    return 0

run_etl = PythonOperator(
    task_id="myextract",
    python_callable=myextract,
    dag=dag
    )


def mytransforme():

    res = random.choice(["continue", "Stop"])
    logging.info(res)
    return res


transf = BranchPythonOperator(
    task_id="branching",
    python_callable=mytransforme,
    provide_context=True,
    dag=dag
)

continue1 = DummyOperator(task_id='continue', dag=dag)
Stop = DummyOperator(task_id='stop', dag=dag)

def myload():
    logging.info("load")
    return 2


run_test = PythonOperator(
    task_id="load1",
    python_callable= myload,
    dag=dag
    )



run_etl >> transf
transf >> [continue1, Stop]
continue1 >> run_test