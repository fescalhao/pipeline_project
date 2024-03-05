from pathlib import Path
from airflow.utils import yaml
from jinja2 import Environment, FileSystemLoader


def build_spark_app_template(app_json_template: dict, spark_args: dict, app_name: str):
    templates_path = str(Path(__file__).parent.resolve())

    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template('template.yaml')

    app_json_template['metadata']['name'] = app_name
    app_json_template['spec']['arguments'] = spark_args

    content = template.render(app_json_template)

    return yaml.safe_load(content)
