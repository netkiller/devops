import os,sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

print("=" * 40, "ConfigMap", "=" * 40)
config = ConfigMap()
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
config.data({'dbhost':'localhost','dbport':'3306','dbuser':'root','dbpass':'123456'}).data({'mysql.cnf':pss('''\
mysql.db = devops
mysql.host = 127.0.0.1
mysql.user = root
mysql.pwd  = root123
mysql.port = 3306
''')}).from_file('passwd.conf', '/etc/passwd').from_file('group.conf','/etc/group')

# print(len(config.dump()))
# config.json()
# config.debug()

print("=" * 40, "Pod", "=" * 40)

pod = Pod()
pod.metadata().name('busybox')
pod.spec().containers().name('test').image('busybox').command([ "/bin/sh","-c","cat /etc/config/keys" ]).volumeMounts([{'name':'config-volume','mountPath':'/tmp/config'}])
pod.spec().volumes().name('config-volume').configMap({'name':'test', 'items':[{'key':'redis.conf','path':'keys'}]})
pod.debug()
pod.json()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
# compose.add(config)
compose.add(pod)
# compose.add(service)
# compose.add(deployment)
# compose.debug()
# compose.json()
# compose.save('/tmp/test.yaml')
compose.create()
# compose.replace()


'''
apiVersion: v1
kind: ConfigMap
metadata:
  name: name-of-your-configmap
data:
  your-file.json: |
    {key1: value1, key2: value2, keyN: valueN}

apiVersion: v1
kind: ConfigMap
metadata:
  name: name-of-your-configmap-2
data:
  your-file.txt: |
    key1: value1
    key2: value2
    keyN: valueN


apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh","-c","cat /etc/config/keys" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: name-of-your-configmap
        items:
        - key: your-file.json
          path: keys
restartPolicy: Never    

'''