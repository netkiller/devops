DevOps Tools
====

OS Software Configure Managment

Install
-------
	$ cd /usr/local/src/
	$ git clone https://github.com/oscm/devops.git
	$ cd devops
	$ python3 setup.py sdist
	$ python3 setup.py install

	or 
	
	$ sudo python3 setup.py install --prefix=/srv/devops
	
	$ sudo cp share/profile.d/devops.sh /etc/profile.d/
	
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

