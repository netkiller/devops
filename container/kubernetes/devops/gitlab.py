import sys
import os
sys.path.insert(0, '/Users/neo/workspace/devops')

from netkiller.kubernetes import *



namespace = 'default'

# config = ConfigMap('gitlab')
# config.apiVersion('v1')
# config.metadata().name('gitlab').namespace(namespace)
# # config.from_file('gitlab.conf', 'gitlab.conf')
# config.data({
#     'gitlab.conf':
#     pss('''\

# ''')
# })

# config.debug()

service = Service()
service.metadata().name('gitlab')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'gitlab'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'http',
    'protocol': 'TCP',
    'port': 80,
    'targetPort': 80
}, {
    'name': 'https',
    'protocol': 'TCP',
    'port': 443,
    'targetPort': 443
}, {
    'name': 'ssh',
    'protocol': 'TCP',
    'port': 22,
    'targetPort': 22
}])
# service.debug()

persistentVolumeClaim = PersistentVolumeClaim()
persistentVolumeClaim.metadata().name('gitlab')
persistentVolumeClaim.metadata().namespace(namespace)
persistentVolumeClaim.metadata().labels({'app': 'gitlab', 'type': 'longhorn'})
persistentVolumeClaim.spec().storageClassName('longhorn')
persistentVolumeClaim.spec().accessModes(['ReadWriteOnce'])
# persistentVolumeClaim.spec().accessModes(['ReadWriteMany'])
persistentVolumeClaim.spec().resources({'requests': {'storage': '2Gi'}})

statefulSet = StatefulSet()
statefulSet.metadata().namespace(namespace)
statefulSet.metadata().name('gitlab').labels({'app': 'gitlab'})
statefulSet.spec().replicas(1)
statefulSet.spec().serviceName('gitlab')
statefulSet.spec().selector({'matchLabels': {'app': 'gitlab'}})
statefulSet.spec().template().metadata().labels({'app': 'gitlab'})
statefulSet.spec().revisionHistoryLimit(10)
statefulSet.spec().selector({'matchLabels': {'app': 'gitlab'}})
# statefulSet.spec().strategy().type('RollingUpdate').rollingUpdate(1, 0)

# statefulSet.spec().template().spec().nodeName('master')

statefulSet.spec().template().spec().containers(
).name('gitlab').image('gitlab/gitlab-ce:latest').ports([
    {
    'name':'http',
    'containerPort': 80
    },{
    'name':'https',
    'containerPort': 443
    },{
    'name':'ssh',
    'containerPort': 22
    },
]).env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'POSTGRES_USER', 'value': 'sonar'},
        {'name': 'POSTGRES_PASSWORD', 'value': 'sonar'}
        ]).volumeMounts([
            {
                'name': 'gitlab',
                'mountPath': '/var/opt/gitlab',
                # 'subPath': 'gitlab'
            },
            # {
            #     'name': 'gitlab',
            #     'mountPath': '/var/log/gitlab',
            #     'subPath': 'gitlab'
            # }, {
            #     'name': 'gitlab',
            #     'mountPath': '/etc/gitlab',
            #     'subPath': 'gitlab'
            # },
        ]).imagePullPolicy(Define.containers.imagePullPolicy.IfNotPresent)
        # .securityContext({'privileged': True})
statefulSet.spec().template().spec().nodeName('agent-3')
statefulSet.spec().template().spec().volumes([
    {
        'name': 'gitlab',
        'persistentVolumeClaim': {
            'claimName': 'gitlab'
        }
    }
])
statefulSet.spec().volumeClaimTemplates([{
    'metadata': {'name': 'gitlab'},
    'spec': {
        'accessModes': ["ReadWriteOnce"],
        # 'storageClassName': "local-path",
        'storageClassName': "longhorn",
        # 'storageClassName': "longhorn-storage",
        'resources':{'requests': {'storage': '1Gi'}}
    }
}
])

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('gitlab')
ingress.metadata().namespace(namespace)
ingress.spec().rules([
    {
        'host': 'gitlab.netkiller.cn',
        'http': {
            'paths': [{
                'pathType': Define.Ingress.pathType.Prefix,
                'path': '/',
                'backend': {
                    'service': {
                        'name': 'gitlab',
                        'port': {'number': 80}
                    }
                }}]}
    }
])

compose = Compose('development')

compose.add(service)
# compose.add(persistentVolumeClaim)
compose.add(statefulSet)
compose.add(ingress)
# compose.debug()

# kubeconfig = '/Users/neo/workspace/kubernetes/office.yaml'
kubeconfig = os.path.expanduser('~/workspace/Neo/ops/k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()
