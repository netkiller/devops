#!/usr/bin/env python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-11-18
##############################################
try:
    import os, sys
    module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, module)
    from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

# extra_hosts = []

gitlab = Services('gitlab')
gitlab.image('gitlab/gitlab-ce:latest')
gitlab.container_name('gitlab')
gitlab.restart('always')
gitlab.hostname('gitlab.netkiller.cn')
# gitlab.extra_hosts(extra_hosts)
# gitlab.environment(['TA=Asia/Shanghai'])
gitlab.environment({'TA':'Asia/Shanghai','GITLAB_OMNIBUS_CONFIG':pss(
'''\
external_url 'http://gitlab.netkiller.cn'
registry_external_url 'http://registry.netkiller.cn'
gitlab_rails['time_zone'] = 'Asia/Shanghai'
''')
})
gitlab.ports(['80:80']) # ,'443:443'
gitlab.volumes([
    '/opt/gitlab/config:/etc/gitlab',
    '/opt/gitlab/logs:/var/log/gitlab',
    '/opt/gitlab/data:/var/opt/gitlab'
])

runner = Services('gitlab-runner')
runner.image('gitlab/gitlab-runner:alpine')
runner.container_name('gitlab-runner')
runner.restart('always')
runner.hostname('gitlabrunner.netkiller.cn')
# runner.extra_hosts(extra_hosts)
runner.environment(['TA=Asia/Shanghai'])
# runner.ports(['80:80','443:443']) 
runner.volumes(['./gitlab/config:/etc/gitlab-runner','/var/run/docker.sock:/var/run/docker.sock','/usr/bin/docker:/usr/bin/docker'])
runner.privileged(True)