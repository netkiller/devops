import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,module)

from netkiller.kubernetes import *

print("=" * 40, "Namespace", "=" * 40)
test = Namespace()
# meta = test.metadata()
# meta.namespace('test')
# test.metadata().name('test').namespace('test')
test.metadata.namespace('test')
# print(test.metadata.metadata())
# namespace.test('hello')
# test.debug()

# exit()

namespace = Namespace()
namespace.metadata.name('production').namespace('production')
# namespace.metadata().namespace('production')
# namespace.test('hello')
# namespace.debug()

# exit()

staging = Namespace()
staging.metadata.name('staging')
staging.metadata.namespace('staging')
# staging.test('world')
# staging.debug()


# exit()

testing = Namespace()
testing.metadata.name('testing')
testing.metadata.namespace('testing')
# testing.debug()

# namespace.debug()

# exit()

print("=" * 40, "ServiceAccount", "=" * 40)
account = ServiceAccount()
account.metadata.name('search').namespace('testing').labels({'app':'elasticsearch'})
# account.debug()

print("=" * 40, "Pod", "=" * 40)
pod = Pod()
pod.apiVersion()
pod.metadata.name('counter')
# pod.metadata.namespace('development')
pod.spec().containers().name('count')
pod.spec().containers().image('busybox:latest')
pod.spec().containers().args(["echo 'Helloworld!!!'"])
# spec = container = pod.spec()
# spec.restartPolicy('Always')
# spec.hostAliases([{'ip':'127.0.0.1','hostname':['www.netkiller.cn','db.netkiller.cn']}])
# spec.securityContext({'sysctls': ['name: net.core.somaxconn','value: "1024"'], 'privileged': 'true'})
# pod.spec().env([{'name':'HOST','valueFrom':{'configMapKeyRef':{'name': 'db-config','key': 'db.host'}}}])
# container = pod.spec().containers()
# container.name('count')
# container.image('busybox:latest')
# .volumeMounts([
# 	{'name': 'config-volume','mountPath': '/etc/config'},
# 	{'name': 'config','mountPath': '/usr/local/etc/redis/redis.conf','subPath': 'redis.conf'}])
# container.command(['nginx -c /etc/nginx/nginx.conf'])
# pod.spec().containers().ports([{'containerPort':'6379'}])
# pod.spec().volumes().name('config-volume').configMap({'name':'special-config', 'items':[{'key':'cache','path':'/mnt/cache'}]})

pod.debug()

# apiVersion: v1
# kind: Pod
# metadata:
#   name: counter
# spec:
#   containers:
#   - name: count
#     image: busybox
#     args: [/bin/sh, -c, 'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']

# exit()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
# compose.add(staging)
# compose.add(testing)
# compose.add(account)
compose.add(pod)
compose.debug()
compose.yaml()
compose.save('/tmp/test.yaml')

print("=" * 40, "Kubernetes", "=" * 40)

kubernetes = Kubernetes()
kubernetes.compose(compose)
# kubernetes.debug()
# print(kubernetes.dump())
kubernetes.main()