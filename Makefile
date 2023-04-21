-include .env
export

PYTHON_VERSION=3.10.6

AWS_REGION=eu-west-2
ECR_URL=$(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_REPO_NAME=prefect-pipelines-fc813ca
ECR_REPO_URL=$(ECR_URL)/$(ECR_REPO_NAME)
IMAGE_TAG=$$(git rev-parse HEAD)
IMAGE=$(ECR_REPO_URL):$(IMAGE_TAG)
GIT_HASH=$$(git rev-parse --short HEAD)

python-setup:
	pyenv install --skip-existing $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)

venv:
	pyenv exec python -m venv .venv
	. .venv/bin/activate && \
	pip install .

infra/remove:
	pulumi stack rm

infra/init:
	pulumi login $(INFRA_BUCKET)
	pulumi stack init organization/pipelines/main

DIR=./pipelines/$(instance)/$(layer)

infra/apply:
	PYTHONPATH=$(DIR)/ pulumi up --config-file $(DIR)/Pulumi.main.yaml

infra-universal/apply:
	PYTHONPATH=./infrastructure/universal pulumi up --config-file ./infrastructure/universal/Pulumi.main.yaml

infra-universal/destroy:
	PYTHONPATH=./infrastructure/universal pulumi destroy --config-file ./infrastructure/universal/Pulumi.main.yaml

docker/login:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_URL)

docker/build:
	docker buildx build --platform linux/amd64 --build-arg CODE_PATH=$(instance)/$(layer) --build-arg GIT_HASH=$(GIT_HASH) -t $(IMAGE) ./pipelines

docker/push:
	docker push $(IMAGE)

pipeline-deployment/build:
	python $(DIR)/deployment.py --name $(instance)-$(layer) --image $(IMAGE)

pipeline-deployment/apply:
	prefect deployment apply