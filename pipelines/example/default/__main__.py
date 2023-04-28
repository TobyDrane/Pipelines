import os
import pulumi

from infrastructure.core.lambdas import create_lambdas_from_source
from infrastructure.core.state_machine import create_state_machine \
    as core_create_state_machine

from utils.utils import extract_lambda_name_from_top_dir

TOP_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(TOP_DIR, 'src'))

created_lambdas = {}

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


def create_lambdas():
    for root, dirs, _ in os.walk(SRC_DIR):
        if (root != SRC_DIR) and (len(dirs) == 0):
            lambda_name = extract_lambda_name_from_top_dir(root)
            function = create_lambdas_from_source(lambda_name, root)
            created_lambdas[lambda_name] = function
            pulumi.export(f"{lambda_name}_arn", function.arn)


def create_state_machine():
    core_create_state_machine("example-default", created_lambdas, config)


if __name__ == "__main__":
    create_lambdas()
    create_state_machine()
