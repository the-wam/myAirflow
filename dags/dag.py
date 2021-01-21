from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

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
    'deezer',
    default_args= default_args,
    description= 'my first DAG',
    schedule_interval='@daily'
)


def just_a_function():
    print('coucou')
    return 0

run_etl = PythonOperator(
    task_id="whole_deezer_etl",
    python_callable=just_a_function,
    dag=dag
    )

def toto():
    print("toto")
    return 1

run_test = PythonOperator(
    task_id="test",
    python_callable= toto,
    dag=dag
    )

run_etl >> run_test