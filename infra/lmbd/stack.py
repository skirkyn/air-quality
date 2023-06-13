import os
from os import path

from aws_cdk import (
    Stack,
    aws_apigatewayv2_alpha as api_gtw,
    aws_apigatewayv2_authorizers_alpha as auth,
    aws_apigatewayv2_integrations_alpha as intgr,
    aws_cognito as cognito,
    aws_lambda as lmbd,
    aws_sqs as sqs,
    aws_rds as rds,
    aws_lambda_python_alpha as lmbd_python, Duration,
)
from constructs import Construct

from config import lambda_config


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, user_pool: cognito.UserPool,
                 user_pool_client: cognito.UserPoolClient, db_cluster: rds.ServerlessCluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        curr_dir = os.path.dirname(os.path.abspath(__file__))
        base_functions = path.join(curr_dir, lambda_config.functions_dir)

        lib_layer = lmbd_python.PythonLayerVersion(self, id=lambda_config.lib_layer,
                                                   entry=path.join(base_functions, lambda_config.lib_name),
                                                   compatible_runtimes=[lmbd.Runtime.PYTHON_3_9]
                                                   )

        locations_function = lmbd_python.PythonFunction(self, lambda_config.locations_name,
                                                        runtime=lmbd.Runtime.PYTHON_3_9,
                                                        timeout=Duration.minutes(1),
                                                        entry=path.join(base_functions, lambda_config.locations_name),
                                                        layers=[lib_layer,
                                                                lmbd_python.PythonLayerVersion(self,
                                                                                               compatible_runtimes=[
                                                                                                   lmbd.Runtime.PYTHON_3_9],
                                                                                               id=lambda_config.locations_layer,
                                                                                               entry=path.join(
                                                                                                   base_functions,
                                                                                                   lambda_config.locations_name),
                                                                                               )])
        db_cluster.grant_data_api_access(locations_function)
        locations_queue = sqs.Queue(self, lambda_config.locations_queue)
        locations_queue.grant_send_messages(locations_function)

        alerts_function = lmbd_python.PythonFunction(self, lambda_config.alerts_name,
                                                     runtime=lmbd.Runtime.PYTHON_3_9,
                                                     timeout=Duration.minutes(1),
                                                     entry=path.join(base_functions, lambda_config.alerts_name),
                                                     layers=[lib_layer,
                                                             lmbd_python.PythonLayerVersion(self,
                                                                                            id=lambda_config.alerts_layer,
                                                                                            compatible_runtimes=[
                                                                                                lmbd.Runtime.PYTHON_3_9],
                                                                                            entry=path.join(
                                                                                                base_functions,
                                                                                                lambda_config.alerts_name),
                                                                                            )])

        db_cluster.grant_data_api_access(alerts_function)
        alerts_queue = sqs.Queue(self, lambda_config.alerts_queue)
        alerts_queue.grant_send_messages(alerts_function)

        http_api = api_gtw.HttpApi(self, lambda_config.api_name)

        issuer = f'https://cognito-idp.{kwargs.get("env").region}.amazonaws.com/{user_pool.user_pool_id}'

        http_authorizer = auth.HttpJwtAuthorizer(id=lambda_config.authorizewr_name,
                                                 identity_source=['$request.header.Authorization'],

                                                 authorizer_name=user_pool_client.user_pool_client_name,
                                                 jwt_audience=[user_pool_client.user_pool_client_id],
                                                 jwt_issuer=issuer,
                                                 )

        http_api.add_routes(
            path=f'/{lambda_config.locations_name}',
            authorizer=http_authorizer,
            methods=[api_gtw.HttpMethod.GET, api_gtw.HttpMethod.POST, api_gtw.HttpMethod.PATCH,
                     api_gtw.HttpMethod.DELETE],
            integration=intgr.HttpLambdaIntegration('locations_integration', locations_function)
        )

        http_api.add_routes(
            path=f'/{lambda_config.alerts_name}',
            authorizer=http_authorizer,
            methods=[api_gtw.HttpMethod.GET, api_gtw.HttpMethod.POST, api_gtw.HttpMethod.PATCH,
                     api_gtw.HttpMethod.DELETE],
            integration=intgr.HttpLambdaIntegration('alerts_integration', alerts_function)
        )
