import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))

aws_account = os.getenv('aws_account')
aws_region = os.getenv('aws_region')


class vpc_config:
    name = os.getenv('vpc_name')
    public_subnet_name = os.getenv('public_subnet_name')
    private_subnet_name = os.getenv('private_subnet_name')
    cidr = os.getenv('cidr')
    cidr_mask = os.getenv('cidr_mask')
    ssh_key_name = os.getenv('ssh_key_name')


class db_config:
    name = os.getenv('db_name')
    secret_name = os.getenv('db_secret_name')
    user = os.getenv('db_user')
    security_group = os.getenv('db_security_group')


class eks_config:
    admin_user = os.getenv('eks_admin_user')
    admin_role_name = os.getenv('eks_admin_role_name')
    managed_policy = os.getenv('eks_managed_policy')
    cluster_name = os.getenv('eks_cluster_name')
    cluster_id = os.getenv('eks_cluster_id')

    private_nodes_name = os.getenv('eks_private_nodes_name')
    private_nodes_disk_size = int(os.getenv('eks_private_disk_size'))
    private_nodes_min_size = int(os.getenv('eks_private_nodes_min_size'))
    private_nodes_max_size = int(os.getenv('eks_private_nodes_max_size'))
    private_nodes_desired_size = int(os.getenv('eks_private_nodes_desired_size'))

    public_nodes_name = os.getenv('eks_public_nodes_name')
    public_nodes_disk_size = int(os.getenv('eks_public_disk_size'))
    public_nodes_min_size = int(os.getenv('eks_public_nodes_min_size'))
    public_nodes_max_size = int(os.getenv('eks_public_nodes_max_size'))
    public_nodes_desired_size = int(os.getenv('eks_public_nodes_desired_size'))

    alb_controller_name = os.getenv('eks_alb_controller_name')

    namespace = os.getenv('eks_namespace') #
    ingress_name = os.getenv('eks_ingress_name')


class cognito_config:
    pool_name = os.getenv('cognito_pool_name')
    client_name = os.getenv('cognito_client_name')
    email_subject = os.getenv('cognito_email_subject')
    email_body = os.getenv('cognito_email_body')
    domain_name = os.getenv('cognito_domain_name')


class bastion_config:
    profile_name = os.getenv('bastion_profile_name')
    admin_role_name = os.getenv('eks_admin_role_name')
    security_group = os.getenv('bastion_security_group')
    name = os.getenv('bastion_name')
    machine_image = os.getenv('bastion_machine_image')

class lambda_config:
    functions_dir = os.getenv('lambda_functions_dir') # '../../code/functions'
    api_name = os.getenv('lambda_api_name') # 'aq_api'
    lib_name = os.getenv('lambda_lib_name')  # lib
    locations_name = os.getenv('lambda_locations_name') # locations
    alerts_name = os.getenv('lambda_alerts_name')  # alerts
    authorizewr_name = os.getenv('lambda_authorizer_name') #'aq_authorizer'
    lib_layer = os.getenv('lambda_lib_layer_name') # lib
    alerts_layer = os.getenv('lambda_alerts_layer_name') # alerts
    locations_layer = os.getenv('lambda_locations_layer_name') # locations
    locations_integration_name = os.getenv('lambda_locations_int_name') #locations_integration
    alerts_integration_name = os.getenv('lambda_alerts_int_name')  # alerts_integration
    alerts_queue = os.getenv('lambda_alerts_queue')
    locations_queue = os.getenv('lambda_locations_queue')

