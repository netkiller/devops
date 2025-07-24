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
