import boto3


s3_client = boto3.client("s3")


def list_s3():
    response = s3_client.list_all_buckets()
    return response
