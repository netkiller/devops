#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2023-01-11
##############################################
import os
import sys
try:
    module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, module)
    from netkiller.docker import *
except ImportError as err:
    print("%s" % (err))

project = 'logstash'

# extra_hosts = [
#    'mongo.netkiller.cn:172.17.195.17', 'eos.netkiller.cn:172.17.15.17',
#    'cfca.netkiller.cn:172.17.15.17'
# ]

dockerfile = Dockerfile()
dockerfile.image('docker.elastic.co/logstash/logstash:8.6.0').run(
    ['apk add -U tzdata', 'rm -f /usr/share/logstash/pipeline/logstash.conf']
).copy('pipeline/', '/usr/share/logstash/pipeline/').copy('config/', '/usr/share/logstash/config/').workdir('/usr/share/logstash')

logstash = Services(project)
# openresty.image('openresty/openresty:alpine')
# openresty.build(dockerfile)
logstash.image('docker.elastic.co/logstash/logstash:8.6.0')
logstash.container_name(project)
logstash.restart('always')
# logstash.hostname('www.netkiller.cn')
# openrelogstashsty.extra_hosts(extra_hosts)
# logstash.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
logstash.environment(['TZ=Asia/Shanghai'])
logstash.ports(['80:80', '443:443'])
# openresty.depends_on('test')
logstash.working_dir('/usr/share/logstash')
logstash.volumes(
    [
        '/srv/logstash/pipeline/:/usr/share/logstash/pipeline/',
        '/srv/logstash/logs/:/usr/share/logstash/logs/',
        '/opt/log/:/opt/log/',
    ]
)

development = Composes('development')
development.workdir('/var/tmp/development')
development.version('3.9')
development.services(logstash)


if __name__ == '__main__':
    try:
        docker = Docker(
            # {'DOCKER_HOST': 'ssh://root@192.168.30.11'}
        )
        # docker.sysctl({'neo': '1'})
        docker.environment(development)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
