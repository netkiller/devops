import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(module)
sys.path.insert(0,module)

from netkiller.kubernetes import *

print("=" * 40, "Namespace", "=" * 40)
namespace = Namespace()
namespace.metadata().namespace('production')
namespace.debug()

# exit()

print("=" * 40, "ConfigMap", "=" * 40)
config = ConfigMap()
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.data({'host':'localhost','port':3306,'user':'root','pass':'123456'})
# config.data({'redis.conf':'''|-
#     pidfile /var/lib/redis/redis.pid
#     dir /var/lib/redis
#     port 6379
#     bind 0.0.0.0
#     appendonly yes
#     protected-mode no
#     requirepass 123456
# '''})
config.dump()
config.debug()

print("=" * 40, "Pod", "=" * 40)

pod = Pod()
pod.apiVersion()
pod.metadata().name('counter').annotations(['security.alpha.kubernetes.io/sysctls: kernel.shm_rmid_forced=1'])
pod.metadata().namespace('development')
spec = container = pod.spec()
spec.restartPolicy('Always')
spec.hostAliases([{'ip':'127.0.0.1','hostname':['www.netkiller.cn','db.netkiller.cn']}])
spec.securityContext({'sysctls': ['name: net.core.somaxconn','value: "1024"'], 'privileged': 'true'})
pod.spec().env([{'name':'HOST','valueFrom':{'configMapKeyRef':{'name': 'db-config','key': 'db.host'}}}])
container = pod.spec().containers()
container.name('nginx')
container.image('nginx:latest').volumeMounts([
	{'name': 'config-volume','mountPath': '/etc/config'},
	{'name': 'config','mountPath': '/usr/local/etc/redis/redis.conf','subPath': 'redis.conf'}])
container.command(['nginx -c /etc/nginx/nginx.conf'])
pod.spec().containers().ports([{'containerPort':'6379'}])
pod.debug()

print("=" * 40, "ServiceAccount", "=" * 40)
account = ServiceAccount()
account.metadata().name('search').namespace('search').labels({'app':'elasticsearch'})
account.debug()

print("=" * 40, "Service", "=" * 40)
service = Service()
service.metadata().name('web')
service.metadata().namespace('stage')
service.spec().selector({'app': 'nginx'})
service.spec().type('NodePort')
service.spec().ports([{'name':'http','protocol':'TCP','port':'80','targetPort':'80'}])
service.spec().externalIPs(['172.16.0.250'])
service.spec().clusterIP('172.168.0.254')
service.status().loadBalancer({
    'ingress': [{'ip': '127.18.10.12'}]
    })
service.debug()

print("=" * 40, "Service1", "=" * 40)
service1 = Service()
service1.metadata().name('mysql')
service1.metadata().namespace('testing')
service1.spec().selector({'app': 'mysql'})
service1.spec().type('NodePort')
service1.spec().ports([{'name':'mysql','protocol':'TCP','port':'3306','targetPort':'3306'}])
service1.spec().externalIPs(['172.16.0.25'])
service1.spec().clusterIP('172.168.0.25')
service1.status().loadBalancer({
    'ingress': [{'ip': '127.18.10.1'}]
    })
service1.debug()