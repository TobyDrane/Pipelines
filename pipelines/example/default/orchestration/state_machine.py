import json
import pulumi
import pulumi_aws as aws

from pipelines.example.default.orchestration.lambdas import lambdas

sfn_role = aws.iam.Role(
    'sfnRole',
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "states.eu-west-2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }"""
)

sfn_role_policy = aws.iam.RolePolicy(
    'sfnRolePolicy',
    role=sfn_role.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:InvokeFunction"
                ],
                "Resource": "*"
            }

        ]
    }"""
)

config = [
    {
        "lambda_name": "example_default_lambda1",
        "next": "example_default_lambda2"
    },
    {
        "lambda_name": "example_default_lambda2",
        "next": None
    }
]
    
def create_state_machine_definition():
    def state_definition_function(arns, lambda_names):
        name_to_arn_map = dict(zip(lambda_names, arns[0]))
        states_map = {}
        for config_item in config:
            lambda_name = config_item["lambda_name"]
            config_next = config_item["next"]

            states_map[lambda_name] = {
                "Type": "Task",
                "Resource": name_to_arn_map[lambda_name],
            }

            if config_next is None:
                states_map[lambda_name]["End"] = True
            else:
                states_map[lambda_name]["Next"] = config_next

        return f"""{{
            "Comment": "Example state machine function",
            "StartAt": "{config[0]["lambda_name"]}",
            "States": {json.dumps(states_map)}
        }}"""

    lambda_arns = [value.arn for _, value in lambdas.items()]
    lambda_names = [key for key, _ in lambdas.items()]
    return pulumi.Output.all(lambda_arns).apply(lambda arns: state_definition_function(arns, lambda_names))

state_machine = aws.sfn.StateMachine(
    "state-machine",
    role_arn=sfn_role.arn,
    definition=create_state_machine_definition()
)
