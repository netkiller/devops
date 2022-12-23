import sys, os

sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

namespace = 'default'

deployment = Deployment()
deployment.metadata().name('bottleneck').labels({
    'app': 'bottleneck'
}).namespace(namespace)
deployment.spec().replicas(6)
deployment.spec().revisionHistoryLimit(10)
# deployment.spec().serviceName('redis')
deployment.spec().selector({'matchLabels': {'app': 'bottleneck'}})
deployment.spec().strategy().type('RollingUpdate').rollingUpdate('25%', '25%')
deployment.spec().template().metadata().labels({'app': 'bottleneck'})
deployment.spec().template().spec().containers().name('bottleneck').image(
    'netkiller/bottleneck:undertow').ports([{
        'name': 'http',
        'containerPort': 8080,
        'protocol': 'TCP'
    }]).env([
        {
            'name': 'TZ',
            'value': 'Asia/Shanghai'
        },
        {
            'name': 'JAVA_OPTS',
            'value': '-Xms2048m -Xmx4096m'
        },
        {
            'name': 'SPRING_OPTS',
            'value': '--spring.profiles.active=dev --server.undertow.worker-threads=5000'
            # --server.tomcat.max-connections=20000 --server.tomcat.max-threads=5000'
        },
    ]).imagePullPolicy(Define.containers.imagePullPolicy.Always)
# deployment.spec().template().spec().tolerations([{
#     'key': 'node-role.kubernetes.io/master',
#     'effect': 'NoSchedule'
# }])

service = Service()
service.metadata().name('bottleneck')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'bottleneck'})
service.spec().type('ClusterIP')
service.spec().ports([{
    'name': 'http',
    'protocol': 'TCP',
    'port': 80,
    'targetPort': 8080
}])

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('bottleneck').labels({
    'app': 'bottleneck',
})
ingress.metadata().namespace(namespace)
# ingress.metadata().annotations({'kubernetes.io/ingress.class': 'nginx'})
ingress.spec().rules([{
    'host': 'bottleneck.netkiller.cn',
    'http': {
        'paths': [{
            'pathType': Define.Ingress.pathType.Prefix,
            'path': '/',
            'backend': {
                'service': {
                    'name': 'bottleneck',
                    'port': {
                        'number': 80
                    }
                }
            }
        }]
    }
}])

compose = Compose('development')
compose.add(deployment)
compose.add(service)
compose.add(ingress)
# compose.debug()

# kubeconfig = '/Volumes/Data/kubernetes/test'
# kubeconfig = os.path.expanduser('~/workspace/ops/ensd/abgrey.yaml')
kubeconfig = os.path.expanduser('~/workspace/ops/ensd/k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()