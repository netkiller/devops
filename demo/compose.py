#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-09-05
##############################################
try:
	import os,  sys
	# sys.path.append('/usr/local/lib/python3.9/site-packages')
	# module_path = '/'.join(os.path.abspath(__file__).split('/')[:-3])
	# print(module_path)
	# sys.path.append(module_path)
	module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.insert(0,module)
	
	# for module in sys.modules:
	# 	print(module)
	from netkiller.docker import *
	# from netkiller.docker import Services
	# from netkiller import *
	# from netkiller.docker import *
	# from netkiller.docker import volumes
	# import netkiller
	

except ImportError as err:
	print("%s" %(err))

nginx =  Services('nginx')
nginx.image('nginx:latest')
nginx.container_name('nginx')
# service.restart('always')
# service.hostname('www.netkiller.cn')
# service.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
# service.environment(['TA=Asia/Shanghai'])
# service.ports(['8080:8080'])
nginx.depends_on('test')

sms =  Services('sms')
sms.image('sms:latest')
sms.container_name('nginx')
# sms.restart('always')
# sms.hostname('www.netkiller.cn')
sms.depends_on(['aaa','bbb','ccc'])
# # sms.debug()

test =  Services('test')
test.image('test:latest')
# # sms.container_name('nginx')
# # sms.restart('always')
# # sms.hostname('www.netkiller.cn')
test.depends_on(nginx)
# # test.depends_on_object(service)
# # test.depends_on_object([service,sms])
# # test.debug()

compose = Composes('development')
compose.version('3.9')
compose.services(nginx)
compose.services(sms)
compose.services(test)
# compose.networks(network)
# compose.networks(mynet)
# compose.volumes(volume)
compose.workdir('/tmp/compose')

if __name__ == '__main__':
	try:
		docker = Docker()
		docker.environment(compose)
		docker.main()
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")