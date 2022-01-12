import os, sys

module = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(module)
sys.path.insert(0, module)
from netkiller.kubernetes import *

namespace = Namespace()
namespace.metadata.name('development')
namespace.metadata.namespace('development')
# namespace.debug()

service = Service()
service.metadata().name('nginx')
service.metadata().namespace('development')
service.spec().selector({'app': 'nginx'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'http',
    'protocol': 'TCP',
    'port': 80,
    'targetPort': 80
}])
# service.debug()

deployment = Deployment()
deployment.apiVersion('apiVersion: apps/v1')
deployment.metadata().name('nginx').labels({'app': 'nginx'}).namespace('development')
deployment.spec().replicas(2)
deployment.spec().selector({'matchLabels': {'app': 'nginx'}})
deployment.spec().template().metadata().labels({'app': 'nginx'})
deployment.spec().template().spec().containers().name('nginx').image(
    'nginx:latest').ports([{
        'containerPort': 80
    }])

secret = Secret()
secret.metadata().name('tls').namespace('development')
secret.data({'tls.crt':' ','tls.key':' '})
secret.type('kubernetes.io/tls')
secret.debug()

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('nginx').namespace('development')
ingress.metadata().annotations({'ingress.kubernetes.io/ssl-redirect': "true"})
ingress.spec().tls([{'hosts':['www.netkiller.cn'],'secretName':'tls'}])
ingress.spec().rules([{
    # 'host': 'www.netkiller.cn',
    'http': {
        'paths': [{
            'path': '/',
            'pathType': 'Prefix',
            'backend': {
                'service': {
                    'name': 'nginx',
                    'port': {
                        'number': 80
                    }
                }
            }
        }]
    }
}])
# ingress.spec().rules([{'host':'article.netkiller.cn','http':{'paths': [{'path':'/($/.*)','backend':{'serviceName':'article', 'servicePort':80}}] }}])
ingress.debug()

compose = Compose('development')
compose.add(namespace)
compose.add(service)
compose.add(deployment)
compose.add(ingress)

kubernetes = Kubernetes()
kubernetes.compose(compose)
kubernetes.main()
