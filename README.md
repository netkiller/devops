DevOps Tools
====

OS Software Configure Managment

Install
-------
### Ubuntu

	$ cd /usr/local/src/
	$ git clone https://github.com/oscm/devops.git
	$ cd devops
	$ python3 setup.py sdist
	$ python3 setup.py install

### CentOS

	$ cd /usr/local/src/
	$ git clone https://github.com/oscm/devops.git
	$ cd devops
	$ python3 setup.py sdist
	$ python3 setup.py install --prefix=/srv/devops
	
	or
	
	python36 setup.py sdist
  	python36 setup.py install --prefix=/srv/devops

### PATH Variable

	$ cp share/profile.d/devops.sh /etc/profile.d/
	
	or 
	
	$ cat >> /etc/profile.d/devops.sh <<'EOF'
	export PATH=/srv/devops/bin:$PATH
	EOF
	
	
Deployment
----------
[Software deployment tools](https://github.com/oscm/devops/blob/master/doc/deployment.md).	

Backup
------
[Data backup tools](https://github.com/oscm/devops/blob/master/doc/backup.md).	
[Database backup](https://github.com/oscm/devops/blob/master/doc/database.md).	

OS Configuration file versioning
-----
[osconf](https://github.com/oscm/devops/blob/master/doc/osconf.md).	


# Donations

We accept PayPal through:

https://www.paypal.me/netkiller

Wechat (微信) / Alipay (支付宝) 打赏:

http://www.netkiller.cn/home/donations.html

