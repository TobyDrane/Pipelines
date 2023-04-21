import os
import pulumi
import pulumi_aws as aws

from core import vpc
from load_balancer import load_balancer, load_balancer_target_group
from iam import task_execution_role
from security import security_group, load_balancer_security_group

cloudwatch_log_group = aws.cloudwatch.LogGroup("pipelines-log-group")

cluster = aws.ecs.Cluster("pipelines-main-cluster")

container_definitions = pulumi.Output.json_dumps([{
    "name": "prefect-server",
    "image": "prefecthq/prefect:2-python3.9",
    "entryPoint": ["bash", "-c"],
    "stopTimeout": 120,
    "command": ["prefect server start"],
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": pulumi.Output.all(cloudwatch_log_group.id, pulumi.get_stack()).apply(lambda arn_and_stack: {
            "awslogs-group": arn_and_stack[0],
            "awslogs-region": "eu-west-2",
            "awslogs-stream-prefix": f"{arn_and_stack[1]}-prefect-server"
        })
    },
    "portMappings": [
        {
            "containerPort": 4200,
            "hostPort": 4200,
            "protocol": "tcp"
        }
    ],
    "environment": [
        {
            "name": "PREFECT_LOGGING_LEVEL",
            "value": "DEBUG"
        },
        {
            "name": "PREFECT_SERVER_API_HOST",
            "value": "0.0.0.0"
        },
        {
            "name": "PREFECT_UI_API_URL",
            "value": pulumi.Output.all(load_balancer.dns_name).apply(lambda dns_name: f"http://{dns_name[0]}/api")
        }
    ]
}])

agent_container_deinitions = pulumi.Output.json_dumps([{
    "name": "prefect-agent",
    "image": "prefecthq/prefect:2-python3.9",
    "entryPoint": ["bash", "-c"],
    "stopTimeout": 120,
    "networkMode": "awsvpc",
    "command": [f"aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin {os.environ['AWS_ACCOUNT']}.dkr.ecr.eu-west-2.amazonaws.com", "prefect agent start --pool default-agent-pool --work-queue default"],
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": pulumi.Output.all(cloudwatch_log_group.id, pulumi.get_stack()).apply(lambda arn_and_stack: {
            "awslogs-group": arn_and_stack[0],
            "awslogs-region": "eu-west-2",
            "awslogs-stream-prefix": f"{arn_and_stack[1]}-prefect-agent"
        })
    },
    "portMappings": [
        {
            "containerPort": 4200,
            "hostPort": 4200,
            "protocol": "tcp"
        }
    ],
    "environment": [
        {
            "name": "PREFECT_API_URL",
            "value": pulumi.Output.all(load_balancer.dns_name).apply(lambda dns_name: f"http://{dns_name[0]}/api")
        }
    ]
}])

task_definition = aws.ecs.TaskDefinition(
    "prefect-task-definition",
    family="prefect-task-definition",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=task_execution_role.arn,
    memory="1024",
    cpu="512",
    container_definitions=container_definitions
)

agent_task_definition = aws.ecs.TaskDefinition(
    "prefect-agent-task-definition",
    family="prefect-agent-task-definition",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=task_execution_role.arn,
    memory="1024",
    cpu="512",
    container_definitions=agent_container_deinitions
)

service = aws.ecs.Service(
    "prefect-service",
    cluster=cluster.arn,
    launch_type="FARGATE",
    desired_count=1,
    task_definition=task_definition.arn,
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
        assign_public_ip=False,
        subnets=vpc.subnets,
        security_groups=[security_group.id, load_balancer_security_group.id]
    ),
    load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
        target_group_arn=load_balancer_target_group.arn,
        container_name="prefect-server",
        container_port=4200
    )]
)

# agent_service = aws.ecs.Service(
#     "prefect-agent-service",
#     cluster=cluster.arn,
#     launch_type="FARGATE",
#     desired_count=1,
#     task_definition=agent_task_definition.arn,
#     network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
#         assign_public_ip=False,
#         subnets=vpc.subnets,
#         security_groups=[security_group.id, load_balancer_security_group.id]
#     )
# )
