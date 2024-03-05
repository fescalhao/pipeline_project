def get_spark_arguments(data: dict) -> dict:
    return {
        "project": data["project"],
        "layer": data["layer"],
        "entity": data["entity"],
        "aws_user_access_key": data["aws_user_access_key"],
        "aws_user_secret_key": data["aws_user_secret_key"],
        "aws_assume_role_arn": data["aws_assume_role_arn"]
    }
