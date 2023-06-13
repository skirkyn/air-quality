import os

from base_function import handle_request

queue_url = os.getenv('alerts_queue_url')


def handler(event, context):
    return handle_request(event, queue_url)