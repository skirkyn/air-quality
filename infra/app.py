#!/usr/bin/env python3

import aws_cdk as cdk

from bastion.stack import BastionStack
from config import aws_account, aws_region
from db.stack import DBStack
from eks.stack import EKSStack
from vpc.stack import VPCStack
from cognito.stack import CognitoStack
from lmbd.stack import LambdaStack

app = cdk.App()

env = cdk.Environment(account=aws_account, region=aws_region)

vpc_stack = VPCStack(app, 'AqVpcStack', env=env)
db_stack = DBStack(app, 'AqDbStack', env=env, vpc=vpc_stack.vpc)
cognito_stack = CognitoStack(app, 'AqCognitoStack',  env=env)
lambda_stack = LambdaStack(app, 'AqLambdaStack', user_pool=cognito_stack.cognito_user_pool,
                           user_pool_client=cognito_stack.app_client,  env=env)
eks_stack = EKSStack(app, 'AqEksStack', env=env, db_cluster=db_stack.cluster, vpc=vpc_stack.vpc)
bastion_stack = BastionStack(app, 'AQBastionStack', env=env, vpc=vpc_stack.vpc, eks_role=eks_stack.role)

app.synth()
