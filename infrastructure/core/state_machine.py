from typing import Dict, List

import json
import pulumi
import pulumi_aws as aws

from infrastructure.core.iam import sfn_role

def create_state_machine_definition(arns: List, lambda_names: List, config):
    # Create a mapping between the lambda names and their arn
    name_to_arn_map = dict(zip(lambda_names, arns[0]))
    states_map = {}

    for config_item in config:
        lambda_name = config_item["lambda_name"]
        config_next = config_item["next"]

        states_map[lambda_name] = {
            "Type": "Task",
            "Resource": name_to_arn_map[lambda_name]
        }

        # They have not specified a next so we assume this is the termination state
        if config_next is None:
            states_map[lambda_name]["End"] = True
        else:
            states_map[lambda_name]["Next"] = config_next

    # Return valid state machine object
    return f"""{{
        "Comment": "Example state machine function",
        "StartAt": "{config[0]["lambda_name"]}",
        "States": {json.dumps(states_map)}
    }}"""


def create_state_machine(state_machine_name: str, lambdas_dict: Dict, config) -> None:
    state_machine_definition = pulumi.Output.all([value.arn for value in lambdas_dict.values()]).apply(
        lambda arns: create_state_machine_definition(arns, lambdas_dict.keys(), config)
    )

    aws.sfn.StateMachine(
        resource_name=state_machine_name,
        role_arn=sfn_role.arn,
        definition=state_machine_definition
    )
