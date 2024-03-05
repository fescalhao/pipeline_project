import datetime

import pendulum
import pathlib
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.utils import yaml

with DAG(
    dag_id="spark_pi",
    schedule=None,
    start_date=pendulum.datetime(2024, 2, 25, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["spark_pi"]
) as dag:

    file = f'{pathlib.Path(__file__).parent.resolve()}/spark-py-pi.yaml'
    print(file)
    spark_template_spec = yaml.safe_load(open(file))

    spark_pi = SparkKubernetesOperator(
        task_id="spark_pi_task",
        name="spark_pi",
        namespace="default",
        kubernetes_conn_id="k8s_conn",
        template_spec=spark_template_spec,
        delete_on_termination=False,
        log_events_on_failure=True,
        in_cluster=True,
        container_logs=True,
        dag=dag
    )

