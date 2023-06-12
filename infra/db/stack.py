from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
)
from constructs import Construct

from config import db_config
from config import vpc_config


class DBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        secret = rds.DatabaseSecret(self, db_config.secret_name,
                                    username=db_config.name
                                    )
        credentials = rds.Credentials.from_secret(secret)

        db_sec_group = ec2.SecurityGroup(self, vpc=vpc, id=db_config.security_group)
        db_sec_group.add_ingress_rule(ec2.Peer.ipv4(vpc_config.cidr), ec2.Port.tcp(3306))

        self.cluster = rds.ServerlessCluster(self, db_config.name,
                                             engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
                                             vpc=vpc,
                                             vpc_subnets=ec2.SubnetSelection(
                                                 subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                                             enable_data_api=True,
                                             default_database_name=db_config.name,
                                             credentials=credentials,
                                             security_groups=[db_sec_group])
