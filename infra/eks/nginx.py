from constructs import Construct
import cdk8s
import cdk8s_plus_26 as kplus
from config import eks_config


class Nginx(cdk8s.Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.deployment = kplus.Deployment(self, 'api-deployment',
                                      containers=[
                                          {
                                              'image': 'nginx',
                                              'imagePullPolicy': kplus.ImagePullPolicy.ALWAYS,
                                              'name': 'nginx',
                                              'port': 80

                                          }
                                      ],
                                      metadata={
                                          'name': 'api-deployment',
                                          'namespace': eks_config.namespace
                                      },
                                      )
        deployment.pod_metadata.add_label('app', 'nginx')
        deployment.select(kplus.LabelSelector.of({'labels': {'app': 'nginx'}}))
        self.service = kplus.Service(self, 'api-service',
                                metadata={
                                    'namespace': eks_config.namespace,
                                    'name': 'api-service',
                                    'labels': {
                                        'app': 'nginx'
                                    },
                                    'annotations': {
                                        'alb.ingress.kubernetes.io/target-type': 'ip'
                                    }
                                    ,
                                    'type': kplus.ServiceType.NODE_PORT,
                                    'ports': [{'port': 80}]
                                })

        self.ingress = kplus.Ingress(self, eks_config.ingress_name,
                                metadata={
                                    'name': eks_config.ingress_name,
                                    'namespace': eks_config.namespace,
                                    'annotations': {
                                        'kubernetes.io/ingress.class': 'alb',
                                        'alb.ingress.kubernetes.io/scheme': 'internal',
                                        'alb.ingress.kubernetes.io/target-type': 'ip'
                                    },
                                    'labels': {'app': 'nginx'}
                                },
                                rules=[
                                    {
                                        'backend': kplus.IngressBackend.from_service(service)
                                    }
                                ]
                                )
