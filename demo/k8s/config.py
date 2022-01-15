import os
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')

from netkiller.kubernetes import *

print("=" * 40, "ConfigMap", "=" * 40)
config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.data({'host': 'localhost', 'port': '3306',
            'user': 'root', 'pass': '123456'})
config.data({'logfile': '/var/log', 'tmp': '/tmp'})
config.debug()

config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.data({'redis.conf': pss(
    'pidfile /var/lib/redis/redis.pid\n'
    'dir /var/lib/redis\n'
    'port 6379\n'
    'bind 0.0.0.0\n'
    'appendonly yes\n'
    'protected-mode no\n'
    'requirepass 123456\n'
)
}).data({'db.ini': pss('''\
mysql.db = devops
mysql.host = 127.0.0.1
mysql.user = root
mysql.pwd  = root123
mysql.port = 3306
''')})
# config.json()
config.debug()

print("=" * 40, "ConfigMap", "=" * 40)

config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.from_file('resolv.conf', '/etc/resolv.conf')
config.debug()

config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.from_env_file('config.env')
config.debug()
