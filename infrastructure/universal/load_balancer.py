import pulumi_aws as aws

from core import vpc
from security import load_balancer_security_group

load_balancer = aws.lb.LoadBalancer(
    "prefect-pipeline-lb",
    internal=False,
    load_balancer_type="application",
    subnets=vpc.public_subnet_ids,
    security_groups=[load_balancer_security_group.id]
)

load_balancer_target_group = aws.lb.TargetGroup(
    "prefect-pipeline-tg",
    port=80,
    protocol="HTTP",
    vpc_id=vpc.vpc_id,
    target_type="ip",
    health_check=aws.lb.TargetGroupHealthCheckArgs(
        healthy_threshold=3,
        interval=300,
        protocol="HTTP",
        matcher="200",
        path="/api/health",
        port=4200
    )
)

load_balancer_listener = aws.lb.Listener(
    "prefect-pipeline-lb-listener",
    load_balancer_arn=load_balancer.arn,
    port=80,
    protocol="HTTP",
    default_actions=[aws.lb.ListenerDefaultActionArgs(
        type="forward",
        target_group_arn=load_balancer_target_group.arn
    )]
)
