import os

import boto3

region = os.getenv('aws_region')
sqs_client = boto3.client('sqs', region_name=region)


def send_message_to_sqs(queue_url: str, message: str):
    return sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )

