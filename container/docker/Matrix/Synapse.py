#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2022-07-06
##############################################
try:
	import os,  sys
	module = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	# print(module)
	sys.path.insert(0,module)
	from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

volumes = Volumes('matrix')
volumes.create('synapse')

generate = Services('generate')
generate.image('matrixdotorg/synapse:latest').container_name('synapse').ports(['8008:8008']).restart('always')
generate.environment([
    'TZ=Asia/Shanghai', 
    'SYNAPSE_SERVER_NAME=chat.netkiller.cn', 
    'SYNAPSE_REPORT_STATS=yes',
    'enable_registration'
])
generate.volumes(['synapse:/data'])
generate.command('generate')

synapse = Services('synapse')
synapse.image('matrixdotorg/synapse:latest').container_name('synapse').ports(['8008:8008']).restart('always')
synapse.environment([
    'TZ=Asia/Shanghai'
])
synapse.volumes(['synapse:/data'])

caddy = Services('caddy')
caddy.image('caddy:latest').container_name('caddy').ports(['80:80','443:443']).restart('unless-stopped')
caddy.environment([
    'TZ=Asia/Shanghai'
])
caddy.volumes(['/data/caddy/Caddyfile:/etc/caddy/Caddyfile'])

composes = Composes('matrix')
composes.version('3.9')
composes.volumes(volumes)
composes.services(generate)
composes.services(synapse)
composes.services(caddy)
composes.dump()
# cat >> /srv/docker-entrypoint.sh <<'EOF'
# EOF

Caddyfile='''
chat.netkiller.cn:80 {
	respond /.well-known/acme-challenge/h27fzgPCxW9Kmhcd9af3YPwuYFCizmZZ_JLvoCeNSQ4 "h27fzgPCxW9Kmhcd9af3YPwuYFCizmZZ_JLvoCeNSQ4.sD2SO-myCgf0JjzYqkA9LA3nN9Pau98bk_fmlBWmzII" 200
}
chat.netkiller.cn {
	reverse_proxy /_matrix/* http://localhost:8008
	reverse_proxy /_synapse/client/* http://localhost:8008
}
'''

if __name__ == '__main__':
	try:
        # {'DOCKER_HOST':'ssh://root@192.168.30.11','NAMESRV_ADDR':'localhost:9876'}
		docker = Docker() 
		docker.createfile('etc/Caddyfile',Caddyfile)
		docker.environment(composes)
		docker.main()
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")