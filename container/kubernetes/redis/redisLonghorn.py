import sys, os

sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

namespace = 'default'

config = ConfigMap('redis')
config.apiVersion('v1')
config.metadata().name('redis').namespace(namespace)
# config.from_file('redis.conf', 'redis.conf')
config.data({
    'redis.conf':
    pss('''\
    pidfile /var/lib/redis/redis.pid
    dir /data
    port 6379
    bind 0.0.0.0
    appendonly yes
    protected-mode yes
    requirepass passw0rd
    maxmemory 2mb
    maxmemory-policy allkeys-lru  
''')
})

# config.debug()

persistentVolumeClaim = PersistentVolumeClaim()
persistentVolumeClaim.metadata().name('redis')
persistentVolumeClaim.metadata().labels({'app': 'redis', 'type': 'longhorn'})
persistentVolumeClaim.spec().storageClassName('longhorn')
# persistentVolumeClaim.spec().storageClassName('local-path')
persistentVolumeClaim.spec().accessModes(['ReadWriteOnce'])
persistentVolumeClaim.spec().resources({'requests': {'storage': '2Gi'}})

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
readinessProbe = {
    'tcpSocket': {
        'port': 6379
    },
    'initialDelaySeconds': 5,
    'failureThreshold': 3,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}

statefulSet = StatefulSet()
statefulSet.metadata().name('redis').labels({'app': 'redis'})
statefulSet.spec().replicas(1)
statefulSet.spec().serviceName('redis')
statefulSet.spec().selector({'matchLabels': {'app': 'redis'}})
statefulSet.spec().template().metadata().labels({'app': 'redis'})
# statefulSet.spec().template().spec().nodeName('master')
statefulSet.spec().template().spec().containers(
).name('redis').image('redis:latest').ports([{
    'containerPort': 6379
}]).volumeMounts([
    {
        'name': 'data',
        'mountPath': '/data'
    },
    {
        'name': 'config',
        'mountPath': '/etc/redis.conf',
        'subPath': 'redis.conf'
    },
]).resources(None).livenessProbe(livenessProbe).readinessProbe(readinessProbe).args(['--appendonly yes','--requirepass Redispass2021'])
# .command(["sh -c redis-server /usr/local/etc/redis.conf"])
statefulSet.spec().template().spec().volumes([{
    'name': 'data',
    'persistentVolumeClaim': {
        'claimName': 'redis'
    }
}, {
    'name': 'config',
    'configMap': {
        'name': 'redis'
    }
}])
# statefulSet.spec().volumeClaimTemplates([{
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
compose.add(config)
compose.add(persistentVolumeClaim)
compose.add(statefulSet)
compose.add(service)
# compose.debug()

# kubeconfig = '/Volumes/Data/kubernetes/test'
kubeconfig = os.path.expanduser('~/workspace/ops/k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()