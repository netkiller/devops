Deploy a Node.js project
=====
  
	First of all, create a user for runtime environment.
	login to remove server and then running following command.
	
	# groupadd -g 80 www
	# adduser -o --home /www --uid 80 --gid 80 -c "Web Application" www
	
	Assign a password to www user.

	# passwd www
	Changing password for user www.
	New UNIX password: 
	Retype new UNIX password: 
	passwd: all authentication tokens updated successfully.
	
	Create project directory.
	# su - www
	# mkdir /www/netkiller.cn


Create a configuration file for the project.
-----
	$ cat production/netkiller.cn.ini 
	[www]
	repository=git@192.168.0.1:netkiller.cn/www.netkiller.cn
	branch=development
	delete=Y
	mode=ssh
	backup=~/backup
	exclude=www.example.com.lst
	remote=www@www.netkiller.cn
	destination=netkiller.cn/www.netkiller.cn
	;dist=WebRoot
	'remote_before=Y
	remote_after=Y

Create an exclude list
-----

	$ touch production/exclude/www.netkiller.cn.lst

Create remove shell
-----

### Before shell.
	
	Before running 'production/libexec/www.netkiller.cn.before' during the deployment.
	Such as build, package, shutdown tomcat...

	$ cat production/libexec/www.netkiller.cn.before 
	/srv/apache-tomcat/bin/shutdown.sh
	sleep 5
	pkill -f apache-tomcat

### After shell

	After running 'production/libexec/www.netkiller.cn.after' during the deployment.

	$ cat production/libexec/www.netkiller.cn.after 
	/srv/apache-tomcat/bin/startup.sh

Use locally available keys to authorise logins on a remote machine
-----

	$ ssh-copy-id www@netkiller.cn
	/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
	/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
	www@netkiller.cn's password: 
	
	Number of key(s) added: 1
	
	Now try logging into the machine, with:   "ssh 'www@netkiller.cn'"
	and check to make sure that only the key(s) you wanted were added.

Deploy locally available project to remove server.
-----

	$ deployment production www.netkiller.cn
