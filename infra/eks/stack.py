from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_eks as eks,
)
from constructs import Construct

from config import eks_config, vpc_config


class EKSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, db_cluster: rds.ServerlessCluster, vpc: ec2.Vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.role = iam.Role(self, eks_config.admin_user, assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
                             role_name=eks_config.admin_role_name, managed_policies=
                             [iam.ManagedPolicy.from_aws_managed_policy_name(
                                 managed_policy_name=eks_config.managed_policy)])

        db_cluster.grant_data_api_access(self.role)

        self.cluster = eks.Cluster(self, eks_config.cluster_id,
                                                           cluster_name=eks_config.cluster_name,
                                                           version=eks.KubernetesVersion.V1_26,
                                                           vpc=vpc,
                                                           vpc_subnets=[
                                                               ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                               ec2.SubnetSelection(
                                                                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)],
                                                           default_capacity=0,

                                                           masters_role=self.role)

        self.cluster.add_nodegroup_capacity(eks_config.private_nodes_name,
                                            instance_types=[
                                                ec2.InstanceType.of(ec2.InstanceClass.T2,
                                                                    ec2.InstanceSize.MEDIUM)],
                                            disk_size=eks_config.private_nodes_disk_size,
                                            min_size=eks_config.private_nodes_min_size,
                                            max_size=eks_config.private_nodes_max_size,
                                            desired_size=eks_config.private_nodes_desired_size,
                                            subnets=ec2.SubnetSelection(
                                                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                                            remote_access=eks.NodegroupRemoteAccess(
                                                ssh_key_name=vpc_config.ssh_key_name),
                                            capacity_type=eks.CapacityType.ON_DEMAND)

        self.cluster.add_nodegroup_capacity(eks_config.public_nodes_name,
                                            instance_types=[
                                                ec2.InstanceType.of(ec2.InstanceClass.T2,
                                                                    ec2.InstanceSize.SMALL)],
                                            disk_size=eks_config.public_nodes_disk_size,
                                            min_size=eks_config.public_nodes_min_size,
                                            max_size=eks_config.public_nodes_max_size,
                                            desired_size=eks_config.public_nodes_desired_size,
                                            subnets=ec2.SubnetSelection(
                                                subnet_type=ec2.SubnetType.PUBLIC),
                                            remote_access=eks.NodegroupRemoteAccess(
                                                ssh_key_name=vpc_config.ssh_key_name),
                                            capacity_type=eks.CapacityType.ON_DEMAND)
