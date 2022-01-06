import os, sys

module = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(module)
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
# service.spec().externalIPs(['172.16.0.250'])
# service.spec().clusterIP('172.168.0.254')
# service.status().loadBalancer({
#     'ingress': [{'ip': '127.18.10.12'}]
#     })
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
# deployment.debug()
# # deployment.json()

# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: nginx
#   labels:
#     app: nginx
# spec:
#   replicas: 3
#   selector:
#     matchLabels:
#       app: nginx
#   template:
#     metadata:
#       labels:
#         app: nginx
#     spec:
#       containers:
#       - name: nginx
#         image: nginx:latest
#         ports:
#         - containerPort: 80

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('nginx')
ingress.metadata().namespace('development')
ingress.metadata().annotations({'ingress.kubernetes.io/ssl-redirect': "false"})
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
# ingress.debug()

# apiVersion: networking.k8s.io/v1
# kind: Ingress
# metadata:
#   name: nginx
#   annotations:
#     kubernetes.io/ingress.class: nginx
# spec:
#   # defaultBackend:
#   #   service:
#   #     name: nginx
#   #     port:
#   #       number: 80
#   rules:
#   - host: foo.bar.com
#     http:
#       paths:
#       - pathType: Prefix
#         path: "/"
#         backend:
#           # serviceName: nginx
#           # servicePort: 80
#           service:
#             name: nginx
#             port:
#               number: 80

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
compose.add(namespace)
# compose.add(staging)
# compose.add(testing)
# compose.add(account)
# compose.add(config)

compose.add(service)
compose.add(deployment)
compose.add(ingress)
# compose.debug()
# compose.yaml()
# compose.save('/tmp/test.yaml')

print("=" * 40, "Kubernetes", "=" * 40)

kubernetes = Kubernetes()
kubernetes.compose(compose)
# kubernetes.debug()
# print(kubernetes.dump())
kubernetes.main()