from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

from config import bastion_config
from config import eks_config
from config import vpc_config


class BastionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, eks_role: iam.Role, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aq_bastion_profile = iam.CfnInstanceProfile(self, bastion_config.profile_name,
                                                    roles=[eks_role.role_name],
                                                    instance_profile_name=eks_config.admin_role_name)
        eks_role.add_managed_policy(aq_bastion_profile)

        db_conn_sec_group = ec2.SecurityGroup(self, id=bastion_config.security_group, vpc=vpc)
        db_conn_sec_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))

        self.instance = ec2.Instance(self, bastion_config.name,
                                     vpc=vpc,
                                     instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
                                     machine_image=ec2.MachineImage.lookup(name=bastion_config.machine_image),
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                     security_group=db_conn_sec_group,
                                     key_name=vpc_config.ssh_key_name,
                                     role=eks_role)
