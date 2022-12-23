#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2022-08-19
##############################################
# try:
import os, sys

#module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.insert(0, module)
from netkiller.docker import *
# except ImportError as err:
# 	print("%s" %(err))

#extra_hosts = [
#    'mongo.netkiller.cn:172.17.195.17', 'eos.netkiller.cn:172.17.15.17',
#    'cfca.netkiller.cn:172.17.15.17'
#]

dockerfile = Dockerfile()
dockerfile.image('openresty/openresty:alpine').run(
    'apk add -U tzdata'
)
openresty = Services('openresty')
# openresty.image('openresty/openresty:alpine')
openresty.build(dockerfile)
openresty.image('openresty:alpine')
openresty.container_name('openresty')
openresty.restart('always')
#openresty.hostname('www.netkiller.cn')
#openresty.extra_hosts(extra_hosts)
# service.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
openresty.environment(['TZ=Asia/Shanghai'])
openresty.ports(['80:80','443:443'])
#openresty.depends_on('test')
openresty.working_dir('/usr/local/openresty')
openresty.volumes(
	[
        '/var/log/openresty:/usr/local/openresty/nginx/logs',
        '/opt/grey.conf:/etc/nginx/conf.d/default.conf',
        '/opt/nginx-conf/location/weixin_business_host.location:/etc/nginx/weixin_business_host.location',
        '/opt/nginx-conf/certs/ejiayou.com:/etc/nginx/cert',
        '/opt/nginx-conf/lua:/usr/local/openresty/nginx/lua'
	]
)

development = Composes('development')
development.workdir('/var/tmp/development')
development.version('3.9')
development.services(openresty)


if __name__ == '__main__':
    try:
        docker = Docker(
        #        {'DOCKER_HOST': 'ssh://root@192.168.30.11'}
        )
        #docker.sysctl({'neo': '1'})
        docker.environment(development)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")