Deploy a java project
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
	# mkdir /www/example.com


Create a configuration file for the project.
-----
	$ cat production/example.com.ini 
	[www]
	repository=git@192.168.0.1:example.com/www.example.com
	delete=Y
	mode=ssh
	backup=~/backup
	exclude=www.example.com.lst
	remote=www@223.25.22.72
	destination=example.com/www.example.com
	remote_before=Y
	remote_after=Y

Create an exclude list
-----

	$ touch exclude/www.cf88.com.lst

Create remove shell
-----

### Before shell.
	
	Before running 'libexec/www.example.com.before' during the deployment.
	Such as build, package, shutdown tomcat...

	$ cat libexec/www.example.com.before 
	/srv/apache-tomcat/bin/shutdown.sh
	sleep 5
	pkill -f apache-tomcat

### After shell

	After running 'libexec/www.example.com.after' during the deployment.

	$ cat libexec/www.example.com.after 
	/srv/apache-tomcat/bin/startup.sh

Use locally available keys to authorise logins on a remote machine
-----

	$ ssh-copy-id www@223.25.22.72
	/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
	/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
	www@223.25.22.72's password: 
	
	Number of key(s) added: 1
	
	Now try logging into the machine, with:   "ssh 'www@223.25.22.72'"
	and check to make sure that only the key(s) you wanted were added.

Deploy locally available project to remove server.
-----

	$ deployment production www.example.com
