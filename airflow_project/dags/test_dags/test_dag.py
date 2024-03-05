from airflow import DAG
import pendulum
import datetime

from airflow.models import TaskInstance
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="test_xcom",
    schedule=None,
    start_date=pendulum.datetime(2024, 2, 25, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["test_xcom"]
) as dag:
    def _get_values(ti: TaskInstance):
        values = ti.xcom_pull(key=None, dag_id="spark_test", task_ids=["spark_test"], include_prior_dates=True)
        print('----------------------')
        print(values)
        print('----------------------')

    test_bla = PythonOperator(
        task_id='test',
        python_callable=_get_values
    )
