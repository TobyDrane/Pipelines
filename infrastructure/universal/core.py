import pulumi_aws as aws
import pulumi_awsx as awsx

vpc = awsx.ec2.Vpc("pipelines-main-vpc")

cloudwatch_log_group = aws.cloudwatch.LogGroup("pipelines-step-functions-log-group")

code_storage_bucket = aws.s3.Bucket(
    "step-functions-code-storage",
    bucket="step-functions-code-storage",
    acl="private"
)