import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(module)
sys.path.insert(0,module)

from netkiller.kubernetes import *

config = ConfigMap()
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.data({'host':'localhost','port':3306,'user':'root','pass':'123456'})
# config.data({'redis.conf':'''
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

