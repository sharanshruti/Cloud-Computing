import boto3
import time

access_id_key = "AKIAW6VF2MA7SWAOORQC"
secret_access_key = "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"

ebsClient = boto3.client(
    "elasticbeanstalk",
    region_name="ap-south-1",
    aws_access_key_id=access_id_key,
    aws_secret_access_key=secret_access_key,
)

ebsClient.create_application_version(
    ApplicationName="website",
    AutoCreateApplication=True,
    Process=True,
    SourceBundle={
        "S3Bucket": "sidass4",
        "S3Key": "sid.zip",
    },
    VersionLabel="version 1.0",
)

while True:
    response = ebsClient.describe_application_versions(
        ApplicationName="website",
        VersionLabels=[
            "version 1.0",
        ],
        MaxRecords=123,
    )
    print(response)

    if response["ApplicationVersions"][0]["Status"] != "PROCESSED":
        time.sleep(3)
    else:
        break


response = ebsClient.create_environment(
    ApplicationName="website",
    EnvironmentName="my-env",
    SolutionStackName="64bit Amazon Linux 2 v5.5.6 running Node.js 16",
    VersionLabel="version 1.0",
    OptionSettings=[
        {
            "Namespace": "aws:autoscaling:launchconfiguration",
            "OptionName": "IamInstanceProfile",
            "Value": "I-am-role"}])