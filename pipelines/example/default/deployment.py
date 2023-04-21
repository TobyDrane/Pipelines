import argparse

from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer

from flow import main

parser = argparse.ArgumentParser()

parser.add_argument("--name")
parser.add_argument("--image")

args = parser.parse_args()
config = vars(args)

deployment = Deployment.build_from_flow(
    flow=main,
    name=config['name'],
    infrastructure=DockerContainer.load("ecr-docker-container"),
    infra_overrides={
        "image": config["image"],
        "image_pull_policy": "ALWAYS"
    },
    path="/opt/prefect/flows",
    entrypoint="flow.py:main"
)

deployment.apply()
