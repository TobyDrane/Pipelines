import json

import pulumi_aws as aws

task_execution_role = aws.iam.Role(
    "task-execution-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement":
            [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ],
        }
    )
)

logging_policy = aws.iam.Policy(
    "ecs-logging-policy",
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Resource": "*",
                "Action": [
                    "ssm:GetParameters",
                    "logs:CreateLogStream",
                    "logs:CreateLogGroup",
                    "logs:PutLogEvents"
                ]
            }]
        }
    )
)


aws.iam.RolePolicyAttachment(
    "logging-policy-attachment",
    role=task_execution_role.name,
    policy_arn=logging_policy.arn
)
