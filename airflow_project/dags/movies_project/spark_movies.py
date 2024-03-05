import datetime
import pendulum
from airflow import DAG
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow_project.dags.utils.spark_app_template.builder import build_spark_app_template
from movie_utils import get_spark_arguments

with DAG(
        dag_id="spark_movies",
        schedule=None,
        start_date=pendulum.datetime(2024, 2, 25, tz="UTC"),
        catchup=False,
        dagrun_timeout=datetime.timedelta(minutes=60),
        tags=["movies_project"]
) as dag:
    movies_silver_var: dict = Variable.get(key="movies_project_silver", deserialize_json=True)
    entities = movies_silver_var.pop("entities")
    app_json_template = movies_silver_var.pop("app_template")

    for entity in entities:
        movies_silver_var["entity"] = entity
        spark_args = get_spark_arguments(movies_silver_var)
        app_name = (f'{movies_silver_var.get("project")}_'
                    f'{movies_silver_var.get("entity")}_'
                    f'{movies_silver_var.get("layer")}')

        app_template = build_spark_app_template(app_json_template, spark_args, app_name)

        SparkKubernetesOperator(
            task_id=f"spark_movies_{movies_silver_var.get('layer')}_{movies_silver_var.get('entity')}task",
            namespace="default",
            kubernetes_conn_id="k8s_conn",
            template_spec=app_template,
            delete_on_termination=False,
            log_events_on_failure=True,
            in_cluster=True,
            container_logs=True,
            dag=dag
        )
