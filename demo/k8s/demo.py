import os, sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('default')
config.data({'NICKNAME':'netkiller','NAME':'Neo'})

pod = Pod()
pod.metadata().name('busybox')
pod.spec().containers().name('test').image('busybox').command([
    "/bin/sh","-c","env | grep NICKNAME" 
]).env([{
    'name':'NICKNAME',
    'valueFrom':{'configMapKeyRef':{
        'name':'test',
        'key':'NICKNAME'}
    }
}])

print("=" * 20, "Compose", "=" * 20)
compose = Compose('development')
compose.add(config)
compose.add(pod)
compose.debug()
compose.delete()
compose.create()

print("=" * 20, "Busybox", "=" * 20)
os.system("sleep 8 && kubectl logs busybox")