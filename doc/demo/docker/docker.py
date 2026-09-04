#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-09-05
##############################################
# try:
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *
# except ImportError as err:
# 	print("%s" %(err))

extra_hosts = [
    'mongo.netkiller.cn:172.17.195.17', 'eos.netkiller.cn:172.17.15.17',
    'cfca.netkiller.cn:172.17.15.17'
]

nginx = Services('nginx')
nginx.image('nginx:latest')
nginx.container_name('nginx')
# service.restart('always')
# service.hostname('www.netkiller.cn')
nginx.extra_hosts(extra_hosts)
# service.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
# service.environment(['TA=Asia/Shanghai'])
# service.ports(['8080:8080'])
nginx.depends_on('test')

sms = Services('sms')
sms.image('sms:latest')
sms.container_name('nginx')
# sms.restart('always')ing
sms.hostname("7899")
sms.depends_on(['aaa', 'bbb', 'ccc'])
# # sms.debug()

test = Services('test')
test.image('test:latest')
# # sms.container_name('nginx')ß
# # sms.restart('always')
# # sms.hostname('www.netkiller.cn')
test.depends_on(nginx)
test.logging('fluentd', {
    'fluentd-address': 'localhost:24224',
    'tag': 'dev.redis.sfzito.com'
})
# # test.depends_on_object([service,sms])
# # test.debug()

development = Composes('development')
development.version('3.9')
development.services(nginx)
development.services(sms)
development.services(test)
# compose.networks(network)
# compose.networks(mynet)
# compose.volumes(volume)
development.workdir('/tmp/compose')

testing = Composes('testing')
testing.version('3.9')
testing.services(nginx)
testing.services(sms)
testing.services(test)
testing.workdir('/tmp/compose')

staging = Composes('staging')
staging.version('3.9')
staging.services(sms)

if __name__ == '__main__':
    try:
        docker = Docker({
            'DOCKER_HOST': 'ssh://root@192.168.30.11',
            'SSS': 'sdfff'
        })
        docker.sysctl({'neo': '1'})
        docker.environment(development)
        docker.environment(testing)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
