#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-09-05
##############################################
try:
	import os,  sys
	module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.insert(0,module)
	from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

def main():
    vhost =  {
        'www.netkiller.cn':['80','443'],
        'api.netkiller.cn':['8080'],
        'img.netkiller.cn':['81','82','83']
    }

    for host, port in vhost.items():
        nginx = Dockerfile()
        (nginx.image('nginx:latest').volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps')
         .expose(port).workdir(f'/var/www/{host}'))
        nginx.show()
        print('-' * 50)

if __name__ == '__main__':
	try:
	    main()
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")