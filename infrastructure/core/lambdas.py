import pulumi
import pulumi_aws as aws

from infrastructure.core.iam import lambda_role


def create_lambdas_from_source(lambda_name: str, source_path: str):
    function = aws.lambda_.Function(
        resource_name=lambda_name,
        role=lambda_role.arn,
        runtime="python3.9",
        handler="lambda.handler",
        code=pulumi.AssetArchive({
            '.': pulumi.FileArchive(source_path)
        })
    )
    return function
