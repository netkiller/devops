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




[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/oscm/devops/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

