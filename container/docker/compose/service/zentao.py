#!/usr/bin/env python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Data. : 2023-02-21
##############################################
try:
    from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

# extra_hosts = []

zentao = Services('zentao')
zentao.image('easysoft/zentao:latest')
zentao.container_name('zentao')
zentao.restart('always')
zentao.hostname('zentao.netkiller.cn')
# zentao.extra_hosts(extra_hosts)
# zentao.environment(['TA=Asia/Shanghai'])
zentao.environment({'TA':'Asia/Shanghai','MYSQL_ROOT_PASSWORD':'123456'})
zentao.ports(['80:80']) # ,'443:443'
zentao.volumes([
    '/opt/zentao/zentaopms:/www/zentaopms'
])
# .privileged(True)

# compose = Composes('zentao')
# compose.version('3.9')
# compose.services(zentao)