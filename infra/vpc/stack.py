from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

from config import vpc_config


class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        print(vpc_config.public_subnet_name)
        self.vpc = ec2.Vpc(
            self, vpc_config.name, cidr=vpc_config.cidr, nat_gateways=0, subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=vpc_config.public_subnet_name,
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name=vpc_config.private_subnet_name,
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                )
            ], enable_dns_support=True,
            enable_dns_hostnames=True,
        )
