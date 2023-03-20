DevOps Tools
====

OS Software Configure Managment

Install
-------

	pip install netkiller-devops -i https://pypi.tuna.tsinghua.edu.cn/simple

### Docker 

	root@netkiller ~# docker run --rm -it --name=netkiller --entrypoint=sh netkiller-devops:latest

### PATH Variable

	$ cp share/profile.d/devops.sh /etc/profile.d/
	
	or 
	
	$ cat >> /etc/profile.d/devops.sh <<'EOF'
	export PATH=/srv/devops/bin:$PATH
	EOF
	
	
Deployment
----------
[Software deployment tools](https://github.com/netkiller/devops/blob/master/doc/deployment.md).	

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

Backup
------
[Data backup tools](https://github.com/netkiller/devops/blob/master/doc/backup.md).	
[Database backup](https://github.com/netkiller/devops/blob/master/doc/database.md).	

OS Configuration file versioning
-----
[osconf](https://github.com/netkiller/devops/blob/master/doc/osconf.md).	


# Donations

We accept PayPal through:

https://www.paypal.me/netkiller

Wechat (微信) / Alipay (支付宝) 打赏:

https://www.netkiller.cn/home/donations.html

