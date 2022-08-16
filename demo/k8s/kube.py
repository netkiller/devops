import os,sys

# module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(module)
# sys.path.insert(0,module)
sys.path.insert(0,'/Users/neo/workspace/devops')

from netkiller.kubernetes import *

print("=" * 40, "Namespace", "=" * 40)
test = Namespace()
# meta = test.metadata()
# meta.namespace('test')
# test.metadata().name('test').namespace('test')
test.metadata().namespace('test')
# print(test.metadata.metadata())
# namespace.test('hello')
# test.debug()

# exit()

namespace = Namespace()
namespace.metadata().name('production').namespace('production')
# namespace.metadata().namespace('production')
# namespace.test('hello')
# namespace.debug()

# exit()

staging = Namespace()
staging.metadata().name('staging')
staging.metadata().namespace('staging')
# staging.test('world')
# staging.debug()


# exit()

testing = Namespace()
testing.metadata().name('testing')
testing.metadata().namespace('testing')
# testing.debug()

# namespace.debug()

# exit()

print("=" * 40, "ServiceAccount", "=" * 40)
account = ServiceAccount()
account.metadata().name('search').namespace('testing').labels({'app':'elasticsearch'})
# account.debug()

print("=" * 40, "ConfigMap", "=" * 40)
config = ConfigMap()
config.apiVersion('v1')
config.metadata().name('test')
# .namespace('test')
config.data({'db.host':'localhost','db.port':'3306','db.user':'root','db.pass':'123456'})
# config.data({'db.host':'localhost'})
# config.debug()

print("=" * 40, "Pod", "=" * 40)
pod = Pod()
pod.apiVersion()
# pod.metadata().name('counter')
# pod.metadata.namespace('development')
# pod.spec.restartPolicy('Always')
# pod.spec.hostAliases([{'ip1':'127.0.0.1','hostname1':['www.netkiller.cn','db.netkiller.cn']}])
# pod.spec.securityContext({'sysctls': ['name: net.core.somaxconn','value: "1024"'], 'privileged': 'true'})
# pod.spec.env([{'name':'HOST','valueFrom':{'configMapKeyRef':{'name': 'db-config','key': 'db.host'}}}])

# pod.spec().containers.name('count')
# pod.spec().containers.image('busybox:latest')
# pod.spec().containers.args(["echo 'Helloworld!!!'"])

# pod.spec.containers.name('count').image('busybox:alpine').args(["echo 'Helloworld!!!'"])
# pod.spec.containers.name('nginx').image('nginx:latest')
# spec = container = pod.spec()

# spec.hostAliases([{'ip':'127.0.0.1','hostname':['www.netkiller.cn','db.netkiller.cn']}, {'ip1':'127.0.0.1','hostname1':['www.netkiller.cn','db.netkiller.cn']}])
# container = 

# .volumeMounts([
# 	{'name': 'config-volume','mountPath': '/etc/config'},
# 	{'name': 'config','mountPath': '/usr/local/etc/redis/redis.conf','subPath': 'redis.conf'}])
# container.command(['nginx -c /etc/nginx/nginx.conf'])
# pod.spec().containers().ports([{'containerPort':'6379'}])
# pod.spec().volumes().name('config-volume').configMap({'name':'special-config', 'items':[{'key':'cache','path':'/mnt/cache'}]})

# pod.debug()
# exit()

print("=" * 40, "Service", "=" * 40)
service = Service()
service.metadata().name('nginx')
# service.metadata().namespace('stage')
service.spec().selector({'app': 'nginx'})
service.spec().type('NodePort')
# service.spec().type('ClusterIP')
service.spec().ports([{'name':'http','protocol':'TCP','port':80,'targetPort':80, 'nodePort': 31000}])
# service.spec().ports([{'port':80,'targetPort':80, 'nodePort': 31000}])
# service.spec().externalIPs(['172.16.0.250'])
# service.spec().clusterIP('172.168.0.254')
# service.debug()
# exit()

print("=" * 40, "Deployment", "=" * 40)
deployment = Deployment()
deployment.metadata().name('nginx').labels({'app':'nginx'})
deployment.spec().replicas(2)
deployment.spec().selector({'matchLabels':{'app':'nginx'}})
deployment.spec().template().metadata().labels({'app':'nginx'})
deployment.spec().template().spec().containers().name('nginx').image('nginx:latest').ports([{'containerPort':80}])
# deployment.debug()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
# compose.add(staging)
# compose.add(testing)
# compose.add(account)
# compose.add(config)
# compose.add(pod)
compose.add(service)
compose.add(deployment)
# compose.debug()
compose.yaml()
# compose.save('/tmp/test.yaml')



print("=" * 40, "Kubernetes", "=" * 40)

kubernetes = Kubernetes('/Volumes/Data/kubeconfig')
kubernetes.compose(compose)
kubernetes.compose(Compose('testing'))
kubernetes.compose(Compose('production'))
# kubernetes.debug()
# print(kubernetes.dump())
kubernetes.main()