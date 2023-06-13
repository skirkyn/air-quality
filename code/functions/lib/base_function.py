import base64
import http
import json

from utils import send_message_to_sqs

id_is_required = 'id is required'

delete = 'DELETE'
get = 'GET'
post = 'POST'
patch = 'PATCh'

method = 'method'
id = 'id'
page_size = 'page'
body = 'body'
query_parameters = 'queryStringParameters'
code = 'statusCode'
page_start = 'start'


def handle_request(event, queue_url: str):
    try:
        http_method = event['requestContext']['http'][method]
        if method not in [get, post, patch, delete]:
            raise MethodNotSupportedError(f'{http_method} not supported')
        if method == get:
            return read(event[query_parameters])
        elif method == delete:
            return send_delete(queue_url, event[query_parameters])
        else:
            return send_create_or_update(queue_url, json.loads(base64.b64decode(event[body])), http_method)

    except MethodNotSupportedError as e:
        return {
            code: http.HTTPStatus.METHOD_NOT_ALLOWED,
            body: str(e)
        }
    except BadRequestError as e:
        return {
            code: http.HTTPStatus.BAD_REQUEST,
            body: str(e)
        }
    except Exception as e:
        return {
            code: http.HTTPStatus.INTERNAL_SERVER_ERROR,
            body: str(e)
        }


def read(query_params: dict):
    if 'id' in query_params:
        return {
            code: http.HTTPStatus.OK,
            body: {}
        }  # todo add read from database
    else:

        start = query_params[page_start] if page_start in query_params else 0
        size = query_params[page_size] if page_size in query_params else 10  # todo magic number
        return {
            code: http.HTTPStatus.OK,
            body: {}
        }  # read page


def send_create_or_update(queue_url: str, body: dict, http_method: str):
    if http_method == patch and id not in body:
        raise BadRequestError('id is required')

    return {code: http.HTTPStatus.OK,
            body: send_message_to_sqs(queue_url, json.dumps({
                body: body,
                method: http_method
            }))}


def send_delete(queue_url: str, query_params: dict):
    if not id in query_params:
        raise BadRequestError(id_is_required)

    return {code: http.HTTPStatus.OK,
            body: send_message_to_sqs(queue_url, json.dumps({
                id: query_params[id],
                method: delete
            }))}



class MethodNotSupportedError(IOError):
    def __init__(self, error: str):
        self.error = error

    def __str__(self):
        return self.error


class BadRequestError(IOError):
    def __init__(self, error: str):
        self.error = error

    def __str__(self):
        return self.error
