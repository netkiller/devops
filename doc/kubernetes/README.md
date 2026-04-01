# Kubernetes 编排工具

## 安装 Python 编排工具

    pip3 install -i https://pypi.org/project netkiller-devops

    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple netkiller-devops

## 演示例子 Gitlab

```python



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

```

## 演示例子 Elasticsearch

```python
from doctest import master
import sys, os

sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

# https://blog.csdn.net/weihua831/article/details/126172591
# https://www.jianshu.com/p/05c93cf45971

namespace = 'default'
# image = 'docker.elastic.co/elasticsearch/elasticsearch:8.4.1'
image = 'elasticsearch:8.4.1'

compose = Compose('development')

config = ConfigMap('elasticsearch')
config.apiVersion('v1')
config.metadata().name('elasticsearch').namespace(namespace).labels({
    'app':
    'elasticsearch',
    'role':
    'master'
})
# config.from_file('redis.conf', 'redis.conf')
config.data({
    'elasticsearch.yml':
    pss('''\
cluster.name: kubernetes-cluster
node.name: ${HOSTNAME}
discovery.seed_hosts: 
  - elasticsearch-master-0
cluster.initial_master_nodes: 
  - elasticsearch-master-0.elasticsearch.default.svc.cluster.local
  - elasticsearch-data-0.elasticsearch-data.default.svc.cluster.local
  - elasticsearch-data-1.elasticsearch-data.default.svc.cluster.local
  - elasticsearch-data-2.elasticsearch-data.default.svc.cluster.local

network.host: 0.0.0.0
transport.profiles.default.port: 9300

xpack.security.enabled: false
xpack.monitoring.collection.enabled: true
''')
})
config.debug()
compose.add(config)

service = Service()
service.metadata().name('elasticsearch')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'elasticsearch', 'role': 'master'})
# service.spec().type('NodePort')
service.spec().ports([{
    'name': 'restful',
    'protocol': 'TCP',
    'port': 9200,
    'targetPort': 9200
}, {
    'name': 'transport',
    'protocol': 'TCP',
    'port': 9300,
    'targetPort': 9300
}])
# service.debug()
compose.add(service)

service = Service()
service.metadata().name('elasticsearch-data').labels({
    'app': 'elasticsearch',
    'role': 'data'
})
service.metadata().namespace(namespace)
service.spec().selector({'app': 'elasticsearch', 'role': 'data'})
# service.spec().type('NodePort')
service.spec().ports([
    # {'name': 'restful', 'protocol': 'TCP', 'port': 9200, 'targetPort': 9200},
    {
        'name': 'transport',
        'protocol': 'TCP',
        'port': 9300,
        'targetPort': 9300
    }
])
# service.debug()
compose.add(service)

limits = {
    'limits': {
        # 'cpu': '500m',
        'memory': '1Gi'
    },
    'requests': {
        # 'cpu': '500m',
        'memory': '1Gi'
    }
}

env = [
    {
        'name': 'TZ',
        'value': 'Asia/Shanghai'
    },
    {
        'name': 'LANG',
        'value': 'en_US.UTF-8'
    },
    {
        'name': 'cluster.name',
        'value': 'kubernetes-cluster'
    },
    {
        'name': 'node.name',
        'valueFrom': {
            'fieldRef': {
                'fieldPath': 'metadata.name'
            }
        }
    },
    {
        'name': 'cluster.initial_master_nodes',
        'value': 'elasticsearch-master-0,elasticsearch-master-1'
    },
    {
        'name':
        'discovery.seed_hosts',
        'value':
        'elasticsearch-master-0.elasticsearch.default.svc.cluster.local,elasticsearch-master-1.elasticsearch.default.svc.cluster.local,elasticsearch-data-0.elasticsearch-data.default.svc.cluster.local,elasticsearch-data-1.elasticsearch-data.default.svc.cluster.local,elasticsearch-data-2.elasticsearch-data.default.svc.cluster.local'
    },
    {
        'name': 'xpack.security.enabled',
        'value': 'false'
    },
    {
        'name': 'ES_JAVA_OPTS',
        'value': '-Xms2048m -Xmx2048m'
    },
    {
        'name': 'RLIMIT_MEMLOCK',
        'value': 'unlimited'
    },
]

deployment = StatefulSet()
deployment.metadata().name('elasticsearch-master').labels({
    'app': 'elasticsearch',
    'role': 'master'
}).annotations({
    # 'security.kubernetes.io/sysctls': 'vm.swappiness=0',
    'security.kubernetes.io/sysctls': 'vm.max_map_count=262144',
    # 'security.kubernetes.io/sysctls': 'vm.overcommit_memory=1'
})
deployment.spec().replicas(2).revisionHistoryLimit(10)
deployment.spec().serviceName('elasticsearch')
deployment.spec().selector(
    {'matchLabels': {
        'app': 'elasticsearch',
        'role': 'master'
    }})
deployment.spec().template().metadata().labels({
    'app': 'elasticsearch',
    'role': 'master'
})
deployment.spec().template().spec().initContainers(
).name('sysctl').image(image).imagePullPolicy('IfNotPresent').securityContext({
    'privileged':
    True,
    'runAsUser':
    0
}).command([
    "/bin/bash",
    "-c",
    "sysctl -w vm.max_map_count=262144 -w vm.swappiness=0 -w vm.overcommit_memory=1",
])
deployment.spec().template().spec().containers(
).name('elasticsearch-master').image(image).resources(None).ports([
    {
        'name': 'restful',
        'protocol': 'TCP',
        'containerPort': 9200
    },
    {
        'name': 'transport',
        'protocol': 'TCP',
        'containerPort': 9300
    },
]).volumeMounts([
    #     {
    #     'name': 'config',
    #     'mountPath': '/usr/share/elasticsearch/config/elasticsearch.yml',
    #     'subPath': 'elasticsearch.yml'
    # },
    {
        'name': 'elasticsearch',
        'mountPath': '/usr/share/elasticsearch/data'
    }
]).env(env).securityContext({'privileged': True})
deployment.spec().template().spec().volumes([{
    'name': 'config',
    'configMap': {
        'name': 'elasticsearch'
    }
}, {
    'name': 'elasticsearch',
    'emptyDir': {}
}])
# deployment.debug()
compose.add(deployment)

livenessProbe = {
    'tcpSocket': {
        'port': 9300
    },
    'initialDelaySeconds': 60,
    'failureThreshold': 3,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}
readinessProbe = {
    'tcpSocket': {
        'port': 9300
    },
    'initialDelaySeconds': 5,
    'failureThreshold': 3,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}

statefulSet = StatefulSet()
statefulSet.metadata().name('elasticsearch-data').labels({
    'app': 'elasticsearch',
    'role': 'data'
}).annotations({
    # 'security.kubernetes.io/sysctls': 'vm.swappiness=0',
    'security.kubernetes.io/sysctls': 'vm.max_map_count=262144',
    # 'security.kubernetes.io/sysctls': 'vm.overcommit_memory=1'
})
statefulSet.spec().replicas(3).revisionHistoryLimit(10)
statefulSet.spec().serviceName('elasticsearch-data')
statefulSet.spec().selector(
    {'matchLabels': {
        'app': 'elasticsearch',
        'role': 'data'
    }})
statefulSet.spec().template().metadata().labels({
    'app': 'elasticsearch',
    'role': 'data'
})
statefulSet.spec().template().spec().initContainers(
).name('sysctl').image(image).imagePullPolicy('IfNotPresent').securityContext({
    'privileged':
    True,
    'runAsUser':
    0
}).command([
    "/bin/bash",
    "-c",
    "sysctl -w vm.max_map_count=262144 -w vm.swappiness=0 -w vm.overcommit_memory=1",
])
statefulSet.spec().template().spec().containers(
).name('elasticsearch-data').image(image).ports([
    # {'name': 'restful', 'protocol': 'TCP', 'containerPort': 9200},
    {
        'name': 'transport',
        'protocol': 'TCP',
        'containerPort': 9300
    }
]).volumeMounts([
#     {
#     'name': 'config',
#     'mountPath': '/usr/share/elasticsearch/config/elasticsearch.yml',
#     'subPath': 'elasticsearch.yml'
# }, 
{
    'name': 'elasticsearch',
    'mountPath': '/usr/share/elasticsearch/data'
}]).env(env).securityContext({
    'privileged': True
}).resources(None).livenessProbe(livenessProbe).readinessProbe(readinessProbe)
statefulSet.spec().template().spec().volumes([
    {
        'name': 'config',
        'configMap': {
            'name': 'elasticsearch'
        }
    }
])
# statefulSet.spec().volumeClaimTemplates('a').metadata().name('elasticsearch')
# statefulSet.spec().volumeClaimTemplates('a').spec().resources({'requests':{'storage': '1Gi'}}).accessModes(['ReadWriteOnce']).storageClassName('local-path')
statefulSet.spec().volumeClaimTemplates([{
    'metadata': {
        'name': 'elasticsearch'
    },
    'spec': {
        'accessModes': ["ReadWriteOnce"],
        #   'storageClassName': "longhorn-storage",
        'storageClassName': "local-path",
        'resources': {
            'requests': {
                'storage': '100Gi'
            }
        }
    }
}])
# statefulSet.debug()
compose.add(statefulSet)

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('elasticsearch').labels({
    'app': 'elasticsearch',
    'role': 'master'
})
ingress.metadata().namespace(namespace)
# ingress.metadata().annotations({'kubernetes.io/ingress.class': 'nginx'})
ingress.spec().rules([{
    'host': 'es.netkiller.cn',
    'http': {
        'paths': [{
            'pathType': Define.Ingress.pathType.Prefix,
            'path': '/',
            'backend': {
                'service': {
                    'name': 'elasticsearch',
                    'port': {
                        'number': 9200
                    }
                }
            }
        }]
    }
}])
# ingress.debug()
compose.add(ingress)
# compose.debug()

# kubeconfig = '/Volumes/Data/kubernetes/test'
# kubeconfig =  os.path.expanduser('~/workspace/ops/ensd/k3d-test.yaml')
kubeconfig = os.path.expanduser('~/workspace/ops/ensd/k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()
```

Kibana

```python
import sys, os

sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

namespace = 'default'

config = ConfigMap('kibana')
config.apiVersion('v1')
config.metadata().name('kibana').namespace(namespace)
# config.from_file('redis.conf', 'redis.conf')
config.data({
    'kibana.yml':
    pss('''\
server.name: kibana
server.host: "0"
server.basePath: "/kibana"
monitoring.ui.container.elasticsearch.enabled: true
xpack.security.enabled: true
elasticsearch.hosts: [ "http://elasticsearch:9200" ]
elasticsearch.username: elastic
elasticsearch.password: I3KEj0MhUmGxKyd510MhUmGxKydSt
''')
})

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

deployment = Deployment()
deployment.metadata().name('kibana').labels({
    'app': 'kibana'
}).namespace(namespace)
deployment.spec().replicas(1)
deployment.spec().revisionHistoryLimit(10)
# deployment.spec().serviceName('redis')
deployment.spec().selector({'matchLabels': {'app': 'kibana'}})
deployment.spec().strategy().type('RollingUpdate').rollingUpdate('25%','25%')
deployment.spec().template().metadata().labels({'app': 'kibana'})
deployment.spec().template().spec().containers().name('kibana').image(
    'kibana:8.4.1').ports([{
        'name': 'http',
        'containerPort': 5601,
        'protocol': 'TCP'
    }]).env([
        {
            'name': 'TZ',
            'value': 'Asia/Shanghai'
        },
        {
            'name': 'ELASTICSEARCH_HOSTS',
            'value': 'http://elasticsearch.default.svc.cluster.local:9200'
        },
    ])
deployment.spec().template().spec().tolerations([{
    'key': 'node-role.kubernetes.io/master',
    'effect': 'NoSchedule'
}])
# .volumeMounts([
    # {
    #     'name': 'config',
    #     'mountPath': '/usr/share/kibana/config/kibana.yml',
    #     'subPath': 'kibana.yml'
    # },
# ])
# .resources(None).livenessProbe(livenessProbe).readinessProbe(readinessProbe)

# deployment.spec().template().spec().volumes([{
#     'name': 'config',
#     'configMap': {
#         'name': 'kibana'
#     }
# }])

service = Service()
service.metadata().name('kibana')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'kibana'})
service.spec().type('ClusterIP')
service.spec().ports([{
    'name': 'http',
    'protocol': 'TCP',
    'port': 80,
    'targetPort': 5601
}])
# service.debug()

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('kibana').labels({
    'app': 'kibana',
})
ingress.metadata().namespace(namespace)
# ingress.metadata().annotations({'kubernetes.io/ingress.class': 'nginx'})
ingress.spec().rules([
    {
        'host': 'kibana.netkiller.cn',
        'http': {
            'paths': [{
                'pathType': Define.Ingress.pathType.Prefix,
                'path': '/',
                'backend': {
                    'service': {
                        'name': 'kibana',
                        'port': {
                            'number': 80
                        }
                    }
                }
            }]
        }
    }
])

compose = Compose('development')
compose.add(config)
compose.add(deployment)
compose.add(service)
compose.add(ingress)
# compose.debug()

# kubeconfig = '/Volumes/Data/kubernetes/test'
kubeconfig = os.path.expanduser('~/workspace/ops/ensd/k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()
```

## 演示例子 Mongo

```python
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *
namespace = 'default'

config = ConfigMap('mongo')
config.metadata().name('mongo').namespace(namespace).labels({'app': 'mongo'})
config.data({'mongod.cnf': pss('''\
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
#  engine:
#  wiredTiger:

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0


# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

security:
  authorization: enabled

#operationProfiling:

#replication:

#sharding:

## Enterprise-Only Options:

#auditLog:

#snmp:
''')})
config.data({'mongo_ROOT_PASSWORD': '123456', 'mongo_DATABASE': 'test',
            'mongo_USER': 'test', 'mongo_PASSWORD': 'test'})
# config.debug()


storageClassName = 'manual'
persistentVolume = PersistentVolume('mongo-pv')
persistentVolume.metadata().name(
    'mongo-pv').labels({'type': 'local'})
persistentVolume.spec().storageClassName(storageClassName)
persistentVolume.spec().capacity({'storage': '2Gi'}).accessModes(
    ['ReadWriteOnce']).hostPath({'path': "/var/lib/mongodb"})
persistentVolume.debug()

persistentVolumeClaim = PersistentVolumeClaim('mongo-pvc')
persistentVolumeClaim.metadata().name('mongo-pvc')
persistentVolumeClaim.spec().storageClassName(storageClassName)
persistentVolumeClaim.spec().resources({'requests': {'storage':'2Gi'}})
persistentVolumeClaim.spec().accessModes(
    ['ReadWriteOnce'])
persistentVolumeClaim.debug()
# exit()


statefulSet = StatefulSet()
statefulSet.metadata().name('mongo')
statefulSet.spec().replicas(1)
statefulSet.spec().serviceName('mongo')
statefulSet.spec().selector({'matchLabels': {'app': 'mongo'}})
statefulSet.spec().template().metadata().labels({'app': 'mongo'})
# statefulSet.spec().replicas(1)
# statefulSet.spec().template().spec().securityContext({'sysctls':[{'name':'fs.inotify.max_user_instances', 'value':'4096'}]})
# statefulSet.spec().template().spec().initContainers().name('busybox').image('busybox').command(['sh','-c','mkdir -p /var/lib/mongo && echo 2048 > /proc/sys/net/core/somaxconn && echo never > /sys/kernel/mm/transparent_hugepage/enabled']).volumeMounts([
#         {'name': 'data', 'mountPath': '/var/lib/mongo'}])
statefulSet.spec().template().spec().containers().name('mongo').image(
    'mongo:latest').ports([{
        'name': 'mongo',
        'protocol': 'TCP',
        'containerPort': 27017
    }]).env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'MONGO_INITDB_DATABASE', 'value': 'admin'},
        {'name': 'MONGO_INITDB_ROOT_USERNAME', 'value': 'admin'},
        {'name': 'MONGO_INITDB_ROOT_PASSWORD', 'value': 'A8nWiX7vitsqOsqoWVnTtv4BDG6uMbexYX9s'}
    ]).volumeMounts([
        {'name': 'config', 'mountPath': '/etc/mongod.conf',
            'subPath': 'mongo.cnf'},
        {'name': 'data', 'mountPath': '/var/lib/mongodb'}
    ]).imagePullPolicy('IfNotPresent')
statefulSet.spec().template().spec().volumes().name(
    'config').configMap({'name': 'mongo'})
statefulSet.spec().template().spec().volumes().name(
    'data').persistentVolumeClaim('mongo-pvc')
# statefulSet.debug()
# exit()

service = Service()
service.metadata().name('mongo')
service.metadata().namespace(namespace).labels({'app': 'mongo'})
service.spec().selector({'app': 'mongo'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'mongo',
    'protocol': 'TCP',
    'port': 27017,
    'targetPort': 27017
}])

ingress = IngressRouteTCP()
ingress.metadata().name('mongo')
ingress.metadata().namespace(namespace)
ingress.spec().entryPoints(['mongo'])
ingress.spec().routes([{
    'match': 'HostSNI(`*`)',
    'services': [{
        'name': 'mongo',
        'port': 27017,
    }]
}])
# ingress.debug()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
compose.add(config)
compose.add(persistentVolume)
compose.add(persistentVolumeClaim)
compose.add(statefulSet)
compose.add(service)
compose.add(ingress)
compose.debug()
# compose.save()
compose.delete()
compose.create()

```

## 演示例子 MySQL

```python
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *
namespace = 'default'

config = ConfigMap('mysql')
config.metadata().name('mysql').namespace(namespace).labels({'app': 'mysql'})
config.data({'mysql.cnf': pss('''\
[mysqld]
max_connections=2048
max_execution_time=120
connect_timeout=120
max_allowed_packet=32M
net_read_timeout=120
net_write_timeout=120
# --wait_timeout=60
# --interactive_timeout=60

sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
character-set-server=utf8mb4
collation-server=utf8mb4_general_ci
explicit_defaults_for_timestamp=true
max_execution_time=0
''')})
config.data({'MYSQL_ROOT_PASSWORD': '123456', 'MYSQL_DATABASE': 'test',
            'MYSQL_USER': 'test', 'MYSQL_PASSWORD': 'test'})
# config.debug()


storageClassName = 'manual'
persistentVolume = PersistentVolume('mysql-pv')
persistentVolume.metadata().name(
    'mysql-pv').labels({'type': 'local'})
persistentVolume.spec().storageClassName(storageClassName)
persistentVolume.spec().capacity({'storage': '2Gi'}).accessModes(
    ['ReadWriteOnce']).hostPath({'path': "/var/lib/mysql"})
persistentVolume.debug()

persistentVolumeClaim = PersistentVolumeClaim('mysql-pvc')
persistentVolumeClaim.metadata().name('mysql-pvc')
persistentVolumeClaim.spec().storageClassName(storageClassName)
persistentVolumeClaim.spec().resources({'requests': {'storage':'2Gi'}})
persistentVolumeClaim.spec().accessModes(
    ['ReadWriteOnce'])
persistentVolumeClaim.debug()
# exit()


statefulSet = StatefulSet()
statefulSet.metadata().name('mysql')
statefulSet.spec().replicas(1)
statefulSet.spec().serviceName('mysql')
statefulSet.spec().selector({'matchLabels': {'app': 'mysql'}})
statefulSet.spec().template().metadata().labels({'app': 'mysql'})
# statefulSet.spec().replicas(1)
# statefulSet.spec().template().spec().securityContext({'sysctls':[{'name':'fs.inotify.max_user_instances', 'value':'4096'}]})
statefulSet.spec().template().spec().initContainers().name('busybox').image('busybox').command(['sh','-c','rm -rf /var/lib/mysql/* && mkdir -p /var/lib/mysql']).volumeMounts([
        {'name': 'data', 'mountPath': '/var/lib/mysql'}])
statefulSet.spec().template().spec().containers().name('mysql').image(
    'mysql:latest'
    # 'mysql:5.7'
    ).ports([{
        'name': 'mysql',
        'protocol': 'TCP',
        'containerPort': 3306
    }]).env([
        {'name': 'MYSQL_ROOT_PASSWORD', 'value': '123456'},
        {'name': 'MYSQL_DATABASE', 'value': 'nacos'},
        {'name': 'MYSQL_USER', 'value': 'nacos'},
        {'name': 'MYSQL_PASSWORD', 'value': 'nacos'}
    ]).volumeMounts([
        {'name': 'config', 'mountPath': '/etc/mysql/conf.d/mysql.cnf',
            'subPath': 'mysql.cnf'},
        {'name': 'data', 'mountPath': '/var/lib/mysql'}
    ]).imagePullPolicy('IfNotPresent')
statefulSet.spec().template().spec().volumes().name(
    'config').configMap({'name': 'mysql'})
statefulSet.spec().template().spec().volumes().name(
    'data').persistentVolumeClaim('mysql-pvc')
# statefulSet.debug()
# exit()

service = Service()
service.metadata().name('mysql')
service.metadata().namespace(namespace).labels({'app': 'mysql'})
service.spec().selector({'app': 'mysql'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'mysql',
    'protocol': 'TCP',
    'port': 3306,
    'targetPort': 3306,
    # 'nodePort': 33306
}])

ingress = IngressRouteTCP()
ingress.metadata().name('mysql')
ingress.metadata().namespace(namespace)
ingress.spec().entryPoints(['mysql'])
ingress.spec().routes([{
    'match': 'HostSNI(`*`)',
    'services': [{
        'name': 'mysql',
        'port': 3306
    }]
}])
# ingress.debug()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
compose.add(config)
compose.add(persistentVolume)
compose.add(persistentVolumeClaim)
compose.add(statefulSet)
compose.add(service)
# compose.add(ingress)
compose.debug()
# compose.save()
compose.delete()
compose.create()

```

## 演示例子 Java Springboot 框架

```python
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
```

## 演示例子 Sonar Qube

```python
import sys, os

sys.path.insert(0, '/Users/neo/workspace/GitHub/devops')
from netkiller.kubernetes import *

namespace = 'default'

# config = ConfigMap('sonarqube')
# config.apiVersion('v1')
# config.metadata().name('sonarqube').namespace(namespace)
# # config.from_file('sonarqube.conf', 'sonarqube.conf')
# config.data({
#     'sonarqube.conf':
#     pss('''\

# ''')
# })

# config.debug()

service = Service()
service.metadata().name('sonarqube')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'sonarqube'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'sonarqube',
    'protocol': 'TCP',
    'port': 80,
    'targetPort': 9000
}])
# service.debug()

# persistentVolumeClaim = PersistentVolumeClaim()
# persistentVolumeClaim.metadata().name('sonarqube')
# persistentVolumeClaim.metadata().namespace(namespace)
# persistentVolumeClaim.metadata().labels({'app': 'sonarqube', 'type': 'longhorn'})
# persistentVolumeClaim.spec().storageClassName('longhorn')
# persistentVolumeClaim.spec().accessModes(['ReadWriteOnce'])
# persistentVolumeClaim.spec().resources({'requests': {'storage': '2Gi'}})

statefulSet = StatefulSet()
statefulSet.metadata().namespace(namespace)
statefulSet.metadata().name('sonarqube').labels({'app': 'sonarqube'})
statefulSet.spec().replicas(1)
statefulSet.spec().serviceName('sonarqube')
statefulSet.spec().selector({'matchLabels': {'app': 'sonarqube'}})
statefulSet.spec().template().metadata().labels({'app': 'sonarqube'})
# statefulSet.spec().template().spec().nodeName('master')

statefulSet.spec().template().spec().containers(
).name('postgresql').image('postgres:latest').ports([{
    'containerPort': 5432
}]).env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'POSTGRES_USER', 'value': 'sonar'},
        {'name': 'POSTGRES_PASSWORD', 'value': 'sonar'}
]).volumeMounts([
    {
        'name': 'postgresql',
        'mountPath': '/var/lib/postgresql'
    },
    {
        'name': 'postgresql',
        'mountPath': '/var/lib/postgresql/data',
        'subPath' : 'data'
    },
])

statefulSet.spec().template().spec().containers(
).name('sonarqube').image('sonarqube:community').ports([{
    'containerPort': 9000
}]).env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'SONAR_JDBC_URL', 'value': 'jdbc:postgresql://localhost:5432/sonar'},
        {'name': 'SONAR_JDBC_USERNAME', 'value': 'sonar'},
        {'name': 'SONAR_JDBC_PASSWORD', 'value': 'sonar'}
]).resources(
#     {
#     'limits': {
#         'cpu': '500m',
#         'memory': '2Gi'
#     },
#     'requests': {
#         'cpu': '500m',
#         'memory': '2Gi'
#     }
# }
).livenessProbe(
#     {
#     'httpGet': {
#         'port': 9000,
#         'path': '/'
#     },
#     'initialDelaySeconds': 30,
#     'failureThreshold': 3,
#     'periodSeconds': 10,
#     'successThreshold': 1,
#     'timeoutSeconds': 5
# }
).readinessProbe(
#     {
#     'httpGet': {
#         'port': 9000,
#         'path': '/'
#     },
#     'initialDelaySeconds': 5,
#     'failureThreshold': 3,
#     'periodSeconds': 10,
#     'successThreshold': 1,
#     'timeoutSeconds': 5
# }
).volumeMounts([
    {
        'name': 'sonarqube',
        'mountPath': '/opt/sonarqube/data',
        'subPath' : 'data'
    },
    {
        'name': 'sonarqube',
        'mountPath': '/opt/sonarqube/extensions',
        'subPath' : 'extensions'
    },
]).securityContext({'privileged': True})

statefulSet.spec().template().spec().volumes([
    {
    'name': 'sonarqube',
    'persistentVolumeClaim': {
        'claimName': 'sonarqube'
    }
},
 {
    'name': 'postgresql',
    'persistentVolumeClaim': {
        'claimName': 'postgresql'
    }
}
])
statefulSet.spec().volumeClaimTemplates([{
	'metadata':{'name': 'sonarqube'},
    'spec':{
      'accessModes': [ "ReadWriteOnce" ],
    #   'storageClassName': "local-path",
      'storageClassName': "longhorn",
      'resources':{'requests':{'storage': '2Gi'}}
	}
},{
	'metadata':{'name': 'postgresql'},
    'spec':{
      'accessModes': [ "ReadWriteOnce" ],
    #   'storageClassName': "local-path",
      'storageClassName': "longhorn-storage",
      'resources':{'requests':{'storage': '2Gi'}}
	}
}
])

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('sonarqube')
ingress.metadata().namespace(namespace)
ingress.spec().rules([
{
    'host': 'sonarqube.netkiller.cn',
    'http':{
        'paths': [{
            'pathType': Define.Ingress.pathType.Prefix,
            'path': '/', 
            'backend':{
                'service':{
                    'name':'sonarqube', 
                    'port':{'number': 80}
                }
            }}]}
}
])

compose = Compose('development')

compose.add(service)
compose.add(statefulSet)
compose.add(ingress)
# compose.debug()

kubeconfig = '/Users/neo/workspace/kubernetes/office.yaml'
# kubeconfig = os.path.expanduser('~/workspace/ops/k3s.yaml')

kubernetes = Kubernetes(kubeconfig)
kubernetes.compose(compose)
kubernetes.main()
```

## 演示例子 Nacos 

单机版

```python
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

namespace = 'default'

# namespace = Namespace()
# namespace.metadata().name(namespace)
# namespace.metadata().namespace(namespace)
# namespace.debug()

config = ConfigMap('nacos')
config.apiVersion('v1')
config.metadata().name('nacos').namespace(namespace)
# config.from_file('custom.properties', 'nacos/init.d/custom.properties')
config.data({'application.properties':pss('''\
    # spring
    server.servlet.contextPath=/nacos
    server.contextPath=/nacos
    server.port=8848
    spring.datasource.platform=mysql
    # nacos.cmdb.dumpTaskInterval=3600
    # nacos.cmdb.eventTaskInterval=10
    # nacos.cmdb.labelTaskInterval=300
    # nacos.cmdb.loadDataAtStart=false
    db.num=1
    # db.url.0=jdbc:mysql://mysql-0.mysql:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    # db.url.1=jdbc:mysql://mysql-0.mysql:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    db.url.0=jdbc:mysql://192.168.30.12:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    db.url.1=jdbc:mysql://192.168.30.12:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    # db.url.1=jdbc:mysql://mysql-0.mysql.default.svc.cluster.local:3306/nacos?characterEncoding=utf8&connectTimeout=3000&socketTimeout=3000&autoReconnect=true&useSSL=false&serverTimezone=Asia/Shanghai
    db.user=nacos
    db.password=nacos
    ### The auth system to use, currently only 'nacos' is supported:
    nacos.core.auth.system.type=nacos


    ### The token expiration in seconds:
    nacos.core.auth.default.token.expire.seconds=${NACOS_AUTH_TOKEN_EXPIRE_SECONDS:18000}

    ### The default token:
    nacos.core.auth.default.token.secret.key=${NACOS_AUTH_TOKEN:SecretKey012345678901234567890123456789012345678901234567890123456789}

    ### Turn on/off caching of auth information. By turning on this switch, the update of auth information would have a 15 seconds delay.
    nacos.core.auth.caching.enabled=${NACOS_AUTH_CACHE_ENABLE:false}
    nacos.core.auth.enable.userAgentAuthWhite=${NACOS_AUTH_USER_AGENT_AUTH_WHITE_ENABLE:false}
    nacos.core.auth.server.identity.key=${NACOS_AUTH_IDENTITY_KEY:serverIdentity}
    nacos.core.auth.server.identity.value=${NACOS_AUTH_IDENTITY_VALUE:security}
    server.tomcat.accesslog.enabled=${TOMCAT_ACCESSLOG_ENABLED:false}
    server.tomcat.accesslog.pattern=%h %l %u %t "%r" %s %b %D
    # default current work dir
    server.tomcat.basedir=
    ## spring security config
    ### turn off security
    nacos.security.ignore.urls=${NACOS_SECURITY_IGNORE_URLS:/,/error,/**/*.css,/**/*.js,/**/*.html,/**/*.map,/**/*.svg,/**/*.png,/**/*.ico,/console-fe/public/**,/v1/auth/**,/v1/console/health/**,/actuator/**,/v1/console/server/**}
    # metrics for elastic search
    management.metrics.export.elastic.enabled=false
    management.metrics.export.influx.enabled=false

    nacos.naming.distro.taskDispatchThreadCount=10
    nacos.naming.distro.taskDispatchPeriod=200
    nacos.naming.distro.batchSyncKeyCount=1000
    nacos.naming.distro.initDataRatio=0.9
    nacos.naming.distro.syncRetryDelay=5000
    nacos.naming.data.warmup=true    
'''    
)})
# config.save()
# config.debug()

statefulSet = StatefulSet()
statefulSet.apiVersion('apps/v1')
statefulSet.metadata().name('nacos').labels(
    {'app': 'nacos'}).namespace(namespace)
statefulSet.spec().replicas(3)
statefulSet.spec().serviceName('nacos')
statefulSet.spec().selector({'matchLabels': {'app': 'nacos'}})
statefulSet.spec().template().metadata().labels({'app': 'nacos'})
statefulSet.spec().template().spec().containers().name('nacos').image(
    'nacos/nacos-server:latest').env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'PREFER_HOST_MODE', 'value': 'hostname'},
        # {'name': 'MODE', 'value': 'standalone'},
        
        {'name': 'MODE', 'value': 'cluster'},
        {'name': 'NACOS_REPLICAS', 'value': '3'},
        {'name': 'NACOS_SERVERS', 'value': 'nacos-0.nacos.default.svc.cluster.local:8848 nacos-1.nacos.default.svc.cluster.local:8848 nacos-2.nacos.default.svc.cluster.local:8848'},


        {'name': 'SPRING_DATASOURCE_PLATFORM', 'value': 'mysql'},
        # {'name': 'MYSQL_SERVICE_HOST', 'value': 'mysql-0.mysql.default.svc.cluster.local'},
        {'name': 'MYSQL_SERVICE_HOST', 'value': '192.168.30.12'},
        {'name': 'MYSQL_SERVICE_PORT', 'value': '3306'},
        {'name': 'MYSQL_SERVICE_DB_NAME', 'value': 'nacos'},
        {'name': 'MYSQL_SERVICE_USER', 'value': 'nacos'},
        {'name': 'MYSQL_SERVICE_PASSWORD', 'value': 'nacos'},

        # {'name': 'MYSQL_SERVICE_USER', 'value': 'root'},
        # {'name': 'MYSQL_SERVICE_PASSWORD', 'value': 'passw0rd'},
        {'name': 'MYSQL_SERVICE_DB_PARAM', 'value': 'characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8'},
        {'name': 'JVM_XMX', 'value': '4g'},
        {'name': 'NACOS_DEBUG', 'value': 'true'},
        {'name': 'TOMCAT_ACCESSLOG_ENABLED', 'value': 'true'},
    ]).ports([
        {'containerPort': 8848},
        {'containerPort': 9848},
        {'containerPort': 9555}
    ]).volumeMounts([
        {'name': 'config', 'mountPath': '/home/nacos/conf/custom.properties', 'subPath': 'custom.properties'},
        # {'name': 'config', 'mountPath': '/home/nacos/conf/application.properties', 'subPath': 'application.properties'}
]).resources({'limits':{'memory': "4Gi"}, 'requests': {'memory': "2Gi"}})
# statefulSet.spec().template().spec().securityContext({'sysctls':[{'name': 'fs.file-max', 'value': '60000'}]})
statefulSet.spec().template().spec().volumes().name('config').configMap({'name': 'nacos'})
statefulSet.debug()
# statefulSet.json()

service = Service()
service.metadata().name('nacos')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'nacos'})
service.spec().type('ClusterIP')
service.spec().ports([
    {'name': 'http', 'protocol': 'TCP', 'port': 8848, 'targetPort': 8848},
    {'name': 'rpc', 'protocol': 'TCP', 'port': 9848, 'targetPort': 9848},
    # {'name': 'http', 'protocol': 'TCP', 'port': 9555, 'targetPort': 9555}
])

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
compose.add(config)
compose.add(statefulSet)
compose.add(service)
compose.debug()
# compose.save()
# compose.delete()
# compose.create()

print("=" * 40, "Busybox", "=" * 40)
# os.system("sleep 5")
# for cmd in ['kubectl get secret tls', 'kubectl get configmap', 'kubectl get pods', 'kubectl get service', 'kubectl get statefulset', 'kubectl get ingress']:
#     os.system(cmd)
#     print("-" * 50)

```

集群版

```python
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *
namespace = 'default'

config = ConfigMap('nacos')
config.apiVersion('v1')
config.metadata().name('nacos').namespace(namespace)
# config.data({
#     'mysql.host': "rm-bp1gna9an26441wsb.mysql.rds.aliyuncs.com",
#     'mysql.port': "3306",
#     'mysql.dbname': "nacos",
#     'mysql.user': "grey",
#     'mysql.password': "A6Diyai1"
# })
config.data({
    'mysql.host': "172.18.200.5",
    'mysql.port': "3306",
    'mysql.dbname': "nacos",
    'mysql.user': "nacos",
    'mysql.password': "nacos"
})
# config.debug()

statefulSet = StatefulSet()
statefulSet = StatefulSet()
statefulSet.apiVersion('apps/v1')
statefulSet.metadata().name('nacos').labels(
    {'app': 'nacos'}).namespace(namespace)
statefulSet.spec().replicas(3)
statefulSet.spec().serviceName('nacos')
statefulSet.spec().selector({'matchLabels': {'app': 'nacos'}})
statefulSet.spec().template().metadata().labels({'app': 'nacos'})
statefulSet.spec().template().metadata().annotations(
    {'pod.alpha.kubernetes.io/initialized': "true"})
# statefulSet.spec().template().spec().affinity().nodeAffinity({
#     'requiredDuringSchedulingIgnoredDuringExecution': [
#         {'labelSelector': {
#             'matchExpressions': [
#                 {'key': 'app',
#                  'operator': 'In',
#                  'values': ['nacos']
#                  }]
#             },
#         'topologyKey': "kubernetes.io/hostname"
#         }
#     ]
# })
statefulSet.spec().template().spec().containers().name('nacos').imagePullPolicy(Define.containers.imagePullPolicy.IfNotPresent).image(
    'nacos/nacos-server:latest').resources(
        # {'requests': {
        # # 'cpu':'200m',
        # 'memory': "2Gi"}}
        ).ports([
        {'name':'client','containerPort': 8848},
        {'name':'client-rpc','containerPort': 9848},
        {'name':'raft-rpc','containerPort': 9849}
    ]).env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'NACOS_REPLICAS', 'value': '1'},
        {'name': 'NACOS_AUTH_ENABLE', 'value': 'true'},
        # {'name': 'SPRING_DATASOURCE_PLATFORM', 'value': 'mysql'},
        
        {'name': 'MYSQL_SERVICE_HOST', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.host'}}},
        {'name': 'MYSQL_SERVICE_PORT', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.port'}}},
        {'name': 'MYSQL_SERVICE_DB_NAME', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.dbname'}}},
        {'name': 'MYSQL_SERVICE_USER', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.user'}}},
        {'name': 'MYSQL_SERVICE_PASSWORD', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.password'}}},
        # {'name': 'MYSQL_SERVICE_DB_PARAM', 'value': 'characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8'},
        
        {'name': 'NACOS_SERVER_PORT', 'value': '8848'},
        {'name': 'NACOS_APPLICATION_PORT', 'value': '8848'},
        {'name': 'PREFER_HOST_MODE', 'value': 'hostname'},
        {'name': 'NACOS_SERVERS', 'value': 'nacos-0.nacos.default.svc.cluster.local:8848 nacos-1.nacos.default.svc.cluster.local:8848 nacos-2.nacos.default.svc.cluster.local:8848'},

        # {'name': 'JVM_XMX', 'value': '4g'},
        # {'name': 'NACOS_DEBUG', 'value': 'true'},
        # {'name': 'TOMCAT_ACCESSLOG_ENABLED', 'value': 'true'},
    ])

# statefulSet.debug()

service = Service()
service.metadata().name('nacos')
service.metadata().namespace(namespace)
service.metadata().labels({'app':'nacos'})
service.spec().selector({'app': 'nacos'})
service.spec().type('ClusterIP')
service.spec().ports([
    {'name': 'server', 'protocol': 'TCP', 'port': 8848, 'targetPort': 8848},
    {'name': 'client-rpc', 'protocol': 'TCP', 'port': 9848, 'targetPort': 9848},
    {'name': 'raft-rpc', 'protocol': 'TCP', 'port': 9555, 'targetPort': 9555}
])

# service.debug()

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('nacos')
ingress.metadata().namespace(namespace)
# ingress.metadata().annotations({'kubernetes.io/ingress.class': 'nginx'})
ingress.spec().rules([
{
    'host': 'nacos.netkiller.cn',
    'http':{
        'paths': [{
            'pathType': Define.Ingress.pathType.Prefix,
            'path': '/nacos', 
            'backend':{
                'service':{
                    'name':'nacos', 
                    'port':{'number': 8848}
                }
            }}]}
}
])
# ingress.debug()

kubeconfig =  os.path.expanduser('~/workspace/ops/ensd/k3s.yaml')
# kubeconfig =  os.path.expanduser('~/tmp/ops/ensd/k3d-test.yaml')
# kubeconfig = '/Volumes/Data/kubeconfig'
kubernetes = Kubernetes(kubeconfig)
compose = Compose('nacos')
compose.add(config)
compose.add(statefulSet)
compose.add(service)
compose.add(ingress)
kubernetes.compose(compose)
kubernetes.main()

```