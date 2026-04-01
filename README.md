DevOps Tools
====

OS Software Configure Managment

这是一个运维工具箱，里面包含了一系列工具集合。

## Install 安装

中国镜像安装

	$ pip install netkiller-devops -i https://pypi.tuna.tsinghua.edu.cn/simple

有时国内镜像同步速度慢，需要指定官方镜像才能安装最新版

	$ pip install netkiller-devops --upgrade -i https://pypi.org/project
	

## Docker 编排工具

传统 Docker compose 采用 YAML 技术，无法完成复杂的编排任务，于是我开发了一个工具，将 compose.yaml 脚本 python 化，用 python 语音编排 compose.yaml 脚本。

1. [Docker 编排工具](https://github.com/netkiller/devops/tree/master/doc/docker)
1. [参考例子](https://github.com/netkiller/devops/tree/master/container/docker)

## Kubernetes 编排工具

与前面 Docker 编排一样，使用 pyhton 完成 Kubernetes 的编排任务。

1. [Kubernetes 编排工具](https://github.com/netkiller/devops/tree/master/doc/kubernetes)
1. [参考例子](https://github.com/netkiller/devops/tree/master/container/kubernetes)


## 工具列表

1. [数据备份工具](https://github.com/netkiller/devops/blob/master/doc/backup.md).	
1. [数据库备份脚本](https://github.com/netkiller/devops/blob/master/doc/database.md).
1. [配置文件版本控制工具](https://github.com/netkiller/devops/blob/master/doc/osconf.md).	
1. [环境部署脚本 Shell](https://github.com/netkiller/devops/blob/master/doc/deployment.md).	

### Shell 工具箱


[Shell 工具](https://github.com/netkiller/devops/tree/master/shell)

 

	root@netkiller ~# docker run --rm -it --name=netkiller --entrypoint=sh netkiller-devops:latest

### Ubuntu 编译安装

	$ cd /usr/local/src/
	$ git clone https://github.com/netkiller/devops.git
	$ cd devops
	$ python3 setup.py sdist
	$ python3 setup.py install

### CentOS 编译安装

	$ cd /usr/local/src/
	$ git clone https://github.com/netkiller/devops.git
	$ cd devops
	$ python3 setup.py sdist
	$ python3 setup.py install --prefix=/srv/devops
	
	or
	
	python36 setup.py sdist
  	python36 setup.py install --prefix=/srv/devops

### Deploy Pypi

	$ pip install setuptools wheel twine
	$ python setup.py sdist bdist_wheel
	$ twine upload dist/netkiller-devops-x.x.x.tar.gz 

### PATH Variable

	$ cp share/profile.d/devops.sh /etc/profile.d/
	
	or 
	
	$ cat >> /etc/profile.d/devops.sh <<'EOF'
	export PATH=/srv/devops/bin:$PATH
	EOF






# Donations

We accept PayPal through:

https://www.paypal.me/netkiller

Wechat (微信) / Alipay (支付宝) 打赏:

https://www.netkiller.cn/home/donations.html

