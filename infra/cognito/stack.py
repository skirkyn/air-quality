from aws_cdk import (
    Stack,
    aws_cognito as cognito, RemovalPolicy,
)
from constructs import Construct

from config import cognito_config


class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cognito_user_pool = cognito.UserPool(self, cognito_config.pool_name,
                                                  user_pool_name=cognito_config.pool_name,
                                                  sign_in_aliases=cognito.SignInAliases(
                                                      email=True
                                                  ),
                                                  self_sign_up_enabled=True,
                                                  auto_verify=cognito.AutoVerifiedAttrs(
                                                      email=True
                                                  ),
                                                  user_verification=cognito.UserVerificationConfig(
                                                      email_subject=cognito_config.email_subject,
                                                      email_body=cognito_config.email_body,
                                                      email_style=cognito.VerificationEmailStyle.CODE
                                                  ),
                                                  password_policy=cognito.PasswordPolicy(
                                                      min_length=8,
                                                      require_lowercase=True,
                                                      require_uppercase=True,
                                                      require_digits=True,
                                                      require_symbols=True
                                                  ),
                                                  account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
                                                  removal_policy=RemovalPolicy.DESTROY
                                                  )

        self.app_client = self.cognito_user_pool.add_client(
            cognito_config.client_name,
            user_pool_client_name=cognito_config.client_name,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                admin_user_password=True
            ),
            o_auth=cognito.OAuthSettings(flows=cognito.OAuthFlows(implicit_code_grant=True))
        )

        self.cognito_user_pool.add_domain(cognito_config.domain_name, cognito_domain=cognito.CognitoDomainOptions(
            domain_prefix=cognito_config.pool_name))
