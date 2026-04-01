# Dockerfile 演示

## 安装 netkiller-devops 

```shell
(.venv) neo@netkiller devops % pip install netkiller-devops
```

## 生成一个 Dockerfile 文本

```python
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

nginx = Dockerfile() 
nginx.image('nginx:latest').volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
nginx.show()
```
输出结果
```text
FROM nginx:latest
VOLUME ["/etc/nginx","/var/log/nginx"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
```

## 另一种写法

```python
nginx = Dockerfile()
# 基于什么镜像
nginx.image('nginx:latest')
# 挂载卷
nginx.volume(['/etc/nginx','/var/log/nginx','/opt'])
# 运行脚本
nginx.run('apt update -y && apt install -y procps')
# 暴漏端口
nginx.expose(['80','443'])
# 工作目录
nginx.workdir('/opt')
# 打印 Dockerfile
nginx.show()
```
输出结果
```text
FROM nginx:latest
VOLUME ["/etc/nginx","/var/log/nginx","/opt"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
```

## 保存 Dockerfile 文件

```python
dockerfile = Dockerfile() 
dockerfile.label({'cn.netkiller.authors':'netkiller'})
dockerfile.image('openjdk:8-jdk-alpine')
dockerfile.copy('neo.txt','/tmp')
# dockerfile.run('ls /')
dockerfile.run(['aa','bb','cc'])
# dockerfile.expose('9000')
dockerfile.expose(['80','443'])
dockerfile.volume([
	'/usr/local'
])
dockerfile.volume([
	'/etc/nginx',
	'/var/www'
])
dockerfile.env({'JAVA_HOME':'/lib/jvm'})
# dockerfile.cmd('startup.sh')
dockerfile.cmd(['sh','/startup.sh','-e sss'])
# dockerfile.entrypoint('startup.sh')
dockerfile.entrypoint(['sh','/startup.sh','-e sss'])
dockerfile.user('nginx:nginx')
dockerfile.workdir('/srv')
dockerfile.show()
dockerfile.save('/tmp/Dockerfile')
```

查看文件

```shell
(.venv) neo@netkiller devops % cat /tmp/Dockerfile 
LABEL org.opencontainers.image.authors="netkiller"
FROM openjdk:8-jdk-alpine
COPY test.txt /tmp
RUN aa bb cc
EXPOSE 80 443
VOLUME ["/usr/local"]
VOLUME ["/etc/nginx","/var/www"]
ENV JAVA_HOME /lib/jvm
CMD sh /startup.sh -e sss
ENTRYPOINT sh /startup.sh -e sss
USER nginx:nginx
WORKDIR /srv
```
## 批量生成 Dockerfile

有时我门会在系统上运行多个实例，会生成一批 Dockerfile 

```python
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
```

## Example

```python

#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2022-08-19
##############################################
# try:
import os, sys
from netkiller.docker import *
# except ImportError as err:
# 	print("%s" %(err))

dockerfile = Dockerfile()
dockerfile.image('openresty/openresty:alpine').run(
    'apk add -U tzdata'
)
openresty = Services('openresty')
openresty.build(dockerfile)
openresty.image('openresty:alpine')
openresty.container_name('openresty')
openresty.restart('always')
openresty.environment(['TZ=Asia/Shanghai'])
openresty.ports(['80:80','443:443'])
openresty.working_dir('/usr/local/openresty')
openresty.volumes([
    '/var/log/openresty:/usr/local/openresty/nginx/logs',
    '/opt/grey.conf:/etc/nginx/conf.d/default.conf',
    '/opt/nginx-conf/location/weixin_business_host.location:/etc/nginx/weixin_business_host.location',
    '/opt/nginx-conf/certs/ejiayou.com:/etc/nginx/cert',
    '/opt/nginx-conf/lua:/usr/local/openresty/nginx/lua'
])

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

```

# Service 编排演示

```python
#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-07-24
##############################################
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *

dockerfile = Dockerfile("neo")
dockerfile.image('nginx:latest').volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
dockerfile.show()
print('-'*60)

neo = Services('netkiller')
neo.build(dockerfile)
neo.image("netkiller:1.3.0")
neo.show()
print('-'*60)

development = Composes('development')
development.version('3.9')
development.services(neo)
development.show()

print('-'*60)
development.debug()
development.save('/tmp/neo.yaml')
```

输出演示

```text
FROM nginx:latest
VOLUME ["/etc/nginx","/var/log/nginx"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
------------------------------------------------------------
container_name: netkiller
build:
  context: .
  dockerfile: Dockerfile
image: netkiller:1.3.0

------------------------------------------------------------
services:
  netkiller:
    container_name: netkiller
    build:
      context: /Users/neo/GitHub/devops/doc/docker
      dockerfile: ./development/netkiller/Dockerfile
    image: netkiller:1.3.0
version: '3.9'

------------------------------------------------------------
{'services': {'netkiller': {'container_name': 'netkiller', 'build': {'context': '/Users/neo/GitHub/devops/doc/docker', 'dockerfile': './development/netkiller/Dockerfile'}, 'image': 'netkiller:1.3.0'}}, 'version': '3.9'}
```

## target 演示

设置 target 名称 init

```text
FROM nginx:latest AS init
COPY --from=init index.html /var/www
```

代码

```python
#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-07-24
##############################################
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *

target = 'init'

dockerfile = Dockerfile("neo",None,target)
dockerfile.image('nginx:latest',target).volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
dockerfile.copy('index.html','/var/www',target)
dockerfile.show()
print('-'*60)

neo = Services('netkiller')
neo.build(dockerfile)
neo.image("netkiller:1.3.0")
neo.show()
print('-'*60)

development = Composes('development')
development.version('3.9')
development.services(neo)
development.show()

print('-'*60)
development.debug()
# development.save('/tmp/neo.yaml')
```

输出演示

```text
FROM nginx:latest AS init
VOLUME ["/etc/nginx","/var/log/nginx"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
COPY --from=init index.html /var/www
------------------------------------------------------------
container_name: netkiller
build:
  context: .
  dockerfile: Dockerfile
  target: init
image: netkiller:1.3.0

------------------------------------------------------------
services:
  netkiller:
    container_name: netkiller
    build:
      context: /Users/neo/GitHub/devops/doc/docker
      dockerfile: ./development/netkiller/Dockerfile
    image: netkiller:1.3.0
version: '3.9'

------------------------------------------------------------
{'services': {'netkiller': {'container_name': 'netkiller', 'build': {'context': '/Users/neo/GitHub/devops/doc/docker', 'dockerfile': './development/netkiller/Dockerfile'}, 'image': 'netkiller:1.3.0'}}, 'version': '3.9'}

```

## Context 上下文设置

context 设置为 /srv/netkiller

```python
#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-07-24
##############################################
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *

target = 'init'

dockerfile = Dockerfile("neo",'/srv/netkiller')
dockerfile.image('openjdk:latest').volume(['/opt/netkiller','/app']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
dockerfile.copy('index.html','/var/www')

neo = Services('netkiller')
neo.build(dockerfile)
neo.image("netkiller:1.3.0")

development = Composes('development')
development.version('3.9')
development.services(neo)
development.show()
```

输出结果 context: /srv/netkiller

```text
services:
  netkiller:
    container_name: netkiller
    build:
      context: /srv/netkiller
      dockerfile: ./development/netkiller/Dockerfile
    image: netkiller:1.3.0
version: '3.9'
```