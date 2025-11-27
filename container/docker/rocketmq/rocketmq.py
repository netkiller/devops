#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-09-05
##############################################
try:
	import os,  sys
	module = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	print(module)
	sys.path.insert(0,module)
	from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

dockerfile = Dockerfile() 
# dockerfile.label({'org.opencontainers.image.authors':'netkiller'})
dockerfile.image('openjdk:8-alpine')
# dockerfile.image('openjdk:8')
dockerfile.env({'ROCKETMQ_VERSION':'4.9.2','ROCKETMQ_HOME':'/srv/rocketmq', 'PATH':'${ROCKETMQ_HOME}/bin:$PATH'}) # 'JAVA_OPT':'"${JAVA_OPT} -server -Xms512m -Xmx2048m -Xmn128m"'
dockerfile.arg({'user':'rocketmq', 'group':'nogroup'})
dockerfile.run('wget https://dlcdn.apache.org/rocketmq/4.9.2/rocketmq-all-4.9.2-bin-release.zip && unzip rocketmq-all-4.9.2-bin-release.zip')
dockerfile.run('mv rocketmq-4.9.2 /srv/rocketmq-4.9.2 && rm -rf rocketmq-all-4.9.2-bin-release.zip')
dockerfile.run('ln -s /srv/rocketmq-${ROCKETMQ_VERSION} /srv/rocketmq')
dockerfile.run('adduser -S -D ${user}')
dockerfile.run(['chown ${user}:${group} -R /srv/rocketmq-${ROCKETMQ_VERSION}'])
dockerfile.expose(['9876'])
dockerfile.expose(['10909','10911','10912'])
dockerfile.copy('docker-entrypoint.sh','/srv/docker-entrypoint.sh')
dockerfile.run('chmod a+x /srv/docker-entrypoint.sh')
dockerfile.entrypoint('["/srv/docker-entrypoint.sh"]') 
dockerfile.workdir('${ROCKETMQ_HOME}')
# dockerfile.render()
# dockerfile.save('/tmp/Dockerfile')

rocketmq = Services('rocketmq')
rocketmq.build(dockerfile).image('registry.netkiller.cn/rocketmq/rocketmq:4.9.2').container_name('rocketmq')
# rocketmq.entrypoint('/srv/rocketmq/bin/mqnamesrv')
# rocketmq.ports('9876:9876').command('/srv/rocketmq/bin/mqnamesrv')

dockerfile = Dockerfile() 
dockerfile.image('registry.netkiller.cn/rocketmq/rocketmq:4.9.2')
dockerfile.run('ln -s /srv/rocketmq-${ROCKETMQ_VERSION} /srv/mqnamesrv')
dockerfile.cmd('/srv/mqnamesrv/bin/mqnamesrv')
dockerfile.workdir('/srv/mqnamesrv')
dockerfile.user('rocketmq:nogroup')
dockerfile.volume([
 	'/home/rocketmq/logs/rocketmqlogs'
])

mqnamesrv = Services('mqnamesrv')
mqnamesrv.build(dockerfile).image('registry.netkiller.cn/rocketmq/mqnamesrv:4.9.2').container_name('mqnamesrv').ports('9876:9876')
mqnamesrv.command('mqnamesrv')

dockerfile = Dockerfile() 
dockerfile.image('registry.netkiller.cn/rocketmq/rocketmq:4.9.2')
dockerfile.run('ln -s /srv/rocketmq-${ROCKETMQ_VERSION} /srv/mqbroker')
dockerfile.cmd('/srv/rocketmq/bin/mqbroker')
dockerfile.workdir('/srv/mqbroker')
dockerfile.user('rocketmq:nogroup')
dockerfile.volume([
 	'/home/rocketmq/logs/rocketmqlogs'
])

mqbroker = Services('mqbroker')
mqbroker.build(dockerfile).image('registry.netkiller.cn/rocketmq/mqbroker:4.9.2').container_name('mqbroker').ports(['10909:10909','10911:10911','10912:10912'])
mqbroker.command('mqbroker -n mqnamesrv:9876 -c /srv/rocketmq/conf/broker.conf')
mqbroker.volumes(['/tmp/logs:/home/rocketmq/logs/rocketmqlogs'])

composes = Composes('rocketmq')
composes.version('3.9')
composes.services(rocketmq)
composes.services(mqnamesrv)
composes.services(mqbroker)


# cat >> /srv/docker-entrypoint.sh <<'EOF'
# EOF

entrypoint='''#!/bin/sh
if [ "$1" = 'mqnamesrv' ]; then
	exec /srv/rocketmq/bin/mqnamesrv
fi
exec "$@"
'''

if __name__ == '__main__':
	try:
		docker = Docker({'DOCKER_HOST':'ssh://root@192.168.30.11','NAMESRV_ADDR':'localhost:9876'}) 
		docker.createfile('rocketmq/rocketmq/docker-entrypoint.sh',entrypoint)
		docker.environment(composes)
		docker.main()
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")