import os,sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

print("=" * 40, "ConfigMap", "=" * 40)
config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('default')
config.data({'host':'localhost','port':'3306','user':'root','pass':'123456'})
config.data({'redis.conf':pss(
    'pidfile /var/lib/redis/redis.pid\n'
    'dir /var/lib/redis\n'
    'port 6379\n'
    'bind 0.0.0.0\n'
    'appendonly yes\n'
    'protected-mode no\n'
    'requirepass 123456\n'
    )
    })
# config.data({'dbhost':'localhost','dbport':'3306','dbuser':'root','dbpass':'123456'}).data({'mysql.cnf':pss('''\
# mysql.db = devops
# mysql.host = 127.0.0.1
# mysql.user = root
# mysql.pwd  = root123
# mysql.port = 3306
# ''')}).from_file('passwd.conf', '/etc/passwd').from_file('group.conf','/etc/group')

# print(len(config.dump()))
# config.json()
# config.debug()

print("=" * 40, "Pod", "=" * 40)

# pod = Pod()
# pod.metadata().name('busybox')
# pod.spec().containers().name('test').image('busybox').command([ "/bin/sh","-c","cat /tmp/config/redis.conf" ]).volumeMounts([{'name':'config-volume','mountPath':'/tmp/config/redis.conf','subPath':'redis.conf'}])
# pod.spec().volumes().name('config-volume').configMap({'name':'test'}) # , 'items':[{'key':'redis.conf','path':'keys'}]

# pod = Pod()
# pod.metadata().name('busybox')
# pod.spec().containers().name('test').image('busybox').command([ "/bin/sh","-c","env" ]).env([{'name':'DBHOST','valueFrom':{'configMapKeyRef':{'name':'test','key':'host'}}}])

pod = Pod()
pod.metadata().name('busybox')
pod.spec().containers().name('test').image('busybox').command([ "/bin/sh","-c","echo Helloworld!!!" ])


# pod.debug()
# pod.json()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
compose.add(config)
compose.add(pod)
compose.debug()
# compose.json()
# compose.save('/tmp/test.yaml')
compose.delete()
compose.create()
# compose.replace()

print("=" * 40, "Busybox", "=" * 40)
os.system("sleep 10 && kubectl logs busybox")