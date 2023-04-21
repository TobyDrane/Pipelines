import pulumi_aws as aws

from core import vpc

security_group = aws.ec2.SecurityGroup(
    "pipelines-ecs-security-group",
    vpc_id=vpc.vpc_id
)

load_balancer_security_group = aws.ec2.SecurityGroup(
    "load-balancer-security-group",
    vpc_id=vpc.vpc_id
)

ecs_egress = aws.ec2.SecurityGroupRule(
    "pipelines-ecs-security-group-egress",
    type="egress",
    from_port=0,
    to_port=0,
    protocol=-1,
    cidr_blocks=["0.0.0.0/0"],
    security_group_id=security_group.id
)

ecs_ingress_alb = aws.ec2.SecurityGroupRule(
    "pipelines-ecs-alb-ingress",
    type="ingress",
    from_port=0,
    to_port=0,
    protocol="-1",
    source_security_group_id=load_balancer_security_group.id,
    security_group_id=security_group.id
)

alb_allow_http = aws.ec2.SecurityGroupRule(
    "load-balancer-security-group-allow-http",
    type="ingress",
    from_port=80,
    to_port=80,
    protocol="TCP",
    cidr_blocks=["0.0.0.0/0"],
    security_group_id=load_balancer_security_group.id
)

alb_allow_https = aws.ec2.SecurityGroupRule(
    "load-balancer-security-group-allow-https",
    type="ingress",
    from_port=443,
    to_port=443,
    protocol="TCP",
    cidr_blocks=["0.0.0.0/0"],
    security_group_id=load_balancer_security_group.id
)

alb_allow_egress = aws.ec2.SecurityGroupRule(
    "load-balancer-security-group-allow-egress",
    type="egress",
    from_port=0,
    to_port=0,
    protocol="-1",
    cidr_blocks=["0.0.0.0/0"],
    security_group_id=load_balancer_security_group.id
)
