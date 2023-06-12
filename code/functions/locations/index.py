from common import say_hello

def handler(event, context):
    return {
        'statusCode': 200,
        'result':  say_hello() + ' locations'
    }
