import sys, os

sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

namespace = 'default'

limits = {
    'limits': {
        'cpu': '200m',
        'memory': '2Gi'
    },
    'requests': {
        'cpu': '200m',
        'memory': '1Gi'
    }
}
readinessProbe = {
    'tcpSocket': {
        'port': 6379
    },
    'initialDelaySeconds': 10,
    'failureThreshold': 5,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}

livenessProbe = {
    'tcpSocket': {
        'port': 6379
    },
    'initialDelaySeconds': 30,
    'failureThreshold': 3,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}


daemonSet = DaemonSet()
daemonSet.metadata().name('redis').labels({'app': 'redis'})
# daemonSet.spec().replicas(1)
daemonSet.spec().revisionHistoryLimit(10)
# daemonSet.spec().serviceName('redis')
daemonSet.spec().selector({'matchLabels': {'app': 'redis'}})
daemonSet.spec().template().metadata().labels({'app': 'redis'})
# daemonSet.spec().template().spec().nodeName('master')
daemonSet.spec().template().spec().containers(
).name('redis').image('redis:latest').imagePullPolicy(Define.containers.imagePullPolicy.IfNotPresent).ports([{
    'containerPort': 6379, 'name':'redis', 'protocol':'TCP'
}]).volumeMounts([
    {
        'name': 'data',
        'mountPath': '/data'
    },
    # {
    #     'name': 'config',
    #     'mountPath': '/etc/redis.conf',
    #     'subPath': 'redis.conf'
    # },
]).resources(limits).livenessProbe(livenessProbe).readinessProbe(readinessProbe).args(['--appendonly yes','--requirepass Redispass2021'])
# .command(["sh -c redis-server /usr/local/etc/redis.conf"])
daemonSet.spec().template().spec().volumes([{
    'name': 'data',
    'hostPath':{
          'path': '/var/lib/redis', 
          'type': ""
    }
}])
# daemonSet.spec().volumeClaimTemplates([{
# 	'metadata':{'name': 'data'},
#     'spec':{
#       'accessModes': [ "ReadWriteOnce" ],
#       'storageClassName': "local-path",
#       'resources':{'requests':{'storage': '2Gi'}}
# 	}
# }])

service = Service()
service.metadata().name('redis')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'redis'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'redis',
    'protocol': 'TCP',
    'port': 6379,
    'targetPort': 6379
}])
# service.debug()

compose = Compose('development')
compose.add(daemonSet)
# compose.add(service)
# compose.debug()

# kubeconfig = '/Volumes/Data/kubernetes/test'
kubeconfig = os.path.expanduser('k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()