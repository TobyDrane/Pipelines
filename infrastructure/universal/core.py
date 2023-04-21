import pulumi_aws as aws
import pulumi_awsx as awsx

vpc = awsx.ec2.Vpc("pipelines-main-vpc")

cloudwatch_log_group = aws.cloudwatch.LogGroup("pipelines-prefect-log-group")

code_storage_bucket = aws.s3.Bucket(
    "prefect-code-storage",
    bucket="prefect-code-storage",
    acl="private"
)

ecr_registry = aws.ecr.Repository("prefect-pipelines")
