import os

import pulumi
import pulumi_aws as aws

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))


def create_lambda(lambda_name, src_path):
    return aws.lambda_.Function(
        resource_name=lambda_name,
        role=lambda_role.arn,
        runtime="python3.9",
        handler="lambda.handler",
        code=pulumi.AssetArchive({
            '.': pulumi.FileArchive(src_path)
        })
    )


lambda_role = aws.iam.Role(
    'lambdaRole',
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }"""
)

lambda_role_policy = aws.iam.RolePolicy(
    'lambdaRolePolicy',
    role=lambda_role.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }]
    }"""
)

lambdas = {}

for root, dirs, files in os.walk(top_dir):
    if (root is not top_dir) and (len(dirs) == 0):
        key_name = root.replace(top_dir, "")
        src_path = top_dir + key_name + "/"
        lambda_name = ("example/default" + key_name).replace("/", "_")
        function = create_lambda(lambda_name, src_path)
        
        lambdas[lambda_name] = function

        pulumi.export(f"{lambda_name}_arn", function.arn)
