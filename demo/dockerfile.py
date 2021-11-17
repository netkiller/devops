#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-09-05
##############################################
# try:
import os,  sys
module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,module)
from netkiller.docker import *
# except ImportError as err:
# 	print("%s" %(err))

nginx = Dockerfile() 
nginx.image('nginx:latest').volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')

# dockerfile = Dockerfile() 
# dockerfile.label({'org.opencontainers.image.authors':'netkiller'})
# dockerfile.image('openjdk:8-jdk-alpine')
# dockerfile.copy('/tmp/test.txt','/tmp')
# dockerfile.run('ls /')
# dockerfile.run(['aa','bb','cc'])
# dockerfile.expose('9000')
# dockerfile.expose(['80','443'])
# dockerfile.volume([
# 	'/usr/local'
# ])
# dockerfile.volume([
# 	'/etc/nginx',
# 	'/var/www'
# ])
# dockerfile.env({'JAVA_HOME':'/lib/jvm'})
# dockerfile.cmd('startup.sh')
# dockerfile.cmd(['sh','/startup.sh','-e sss'])
# dockerfile.entrypoint('startup.sh')
# dockerfile.entrypoint(['sh','/startup.sh','-e sss'])
# dockerfile.user('nginx:nginx')
# dockerfile.workdir('/srv')
# dockerfile.render()
# dockerfile.save('/tmp/Dockerfile')

dockerfile = Dockerfile() 
dockerfile.label({'org.opencontainers.image.authors':'netkiller'})
dockerfile.image('openjdk:8-jdk-alpine')
# dockerfile.copy('/tmp/test.txt','/tmp')
# dockerfile.run('ls /')
# dockerfile.run(['aa','bb','cc'])
# dockerfile.expose('9000')
# dockerfile.expose(['80','443'])
# dockerfile.volume([
# 	'/usr/local'
# ])
# dockerfile.volume([
# 	'/etc/nginx',
# 	'/var/www'
# ])
# dockerfile.env({'JAVA_HOME':'/lib/jvm'})
# dockerfile.cmd('startup.sh')
# dockerfile.cmd(['sh','/startup.sh','-e sss'])
# dockerfile.entrypoint('startup.sh')
# dockerfile.entrypoint(['sh','/startup.sh','-e sss'])
# dockerfile.user('nginx:nginx')
# dockerfile.workdir('/srv')
# dockerfile.render()
# dockerfile.save('/tmp/Dockerfile')

nacos = Services('nacos')
# nacos.build(dockerfile)
nacos.build(nginx)

testing = Composes('testing')
# testing.workdir('/tmp')
testing.version('3.9')
testing.services(nacos)

if __name__ == '__main__':
	try:
	# {'DOCKER_HOST':'ssh://root@192.168.30.11','SSS':'sdfff'}
		docker = Docker() 
		# docker.sysctl({'neo':'1'})
		# docker.environment(development)
		docker.environment(testing)
		docker.main()
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")