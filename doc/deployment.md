Backup
======

Help
----
	$ deployment 
	Usage: deployment [options] stage project <other>

	Options:
	  -h, --help            show this help message and exit
	  -r, --revert          revert to revision
	  --backup=BACKUP       backup remote to local
	  --clean               

	  stage:
		development | testing | production

	  project:
		<host>.<domain>

	  Branch:
		branch management

		-c master|trunk, --checkout=master|trunk
							checkout branch
		-n branch, --new=branch
							Create new branch
		-d branch, --delete=branch
							delete branch
		--release=RELEASE   release version exampe:2014-01-23

	  Example: 
		deployment testing www.example.com
		deployment production www.example.com --clean
		deployment testing bbs.example.com --backup=/tmp/backup

	  Homepage: http://netkiller.github.com	Author: Neo <netkiller@msn.com>

Configure
---------
	$ cat etc/testing/example.com.ini 
	[www]
	;repository=git@192.168.2.1:example.com/www.example.com
	repository=https://github.com/oscm/shell.git
	source=/tmp/repo
	option=--delete --password-file=confure/production/example.com/passwd
	exclude=testing/www.example.com.lst
	logfile=/tmp/www.example.com
	remote=www@192.168.2.15
	destination=example.com/www.example.com

	[bbs]
	repository=https://github.com/example.com/bbs.example.com.git
	remote=www@192.168.2.15
	destination=example.com/bbs.example.com
	
	[images]
	repository=https://github.com/example.com/images.example.com.git
	remote=www@192.168.2.15
	destination=example.com/images.example.com
	branch=freebsd

### Config item 
	repository: git uri
	source: directory for checkout and rsync
	option: rsync argv
	exclude: exclude file for rsync
	remote: remote host
	destination: destination directory
	branch: git branch, defualt is master
	
### show me the projects
	$ deployment testing
	example.com.ini
	['www', 'images', 'api', 'bbs', 'news', 'blog', 'music', 'video']
	
Deploy Project
--------------
	$ deployment testing bbs.example.com
	receiving incremental file list

	sent 82 bytes  received 3228 bytes  601.82 bytes/sec
	total size is 243879  speedup is 73.68

Revert
------
	$ deployment testing www.example.com -r master	
	$ deployment testing www.example.com -r b1f13fade4c069ff077ce5f26fc3cb1e3c6df902	
	
	$ deployment testing www.example.com -r 838cba5
	HEAD is now at 838cba5... Merge branch 'master' of https://github.com/oscm/linux
	* (detached from 838cba5)
	  master
	sending incremental file list
	.git/
	.git/index
			7344 100%    6.34MB/s    0:00:00 (xfer#1, to-check=117/157)

	sent 3230 bytes  received 148 bytes  519.69 bytes/sec
	total size is 234676  speedup is 69.47
	
Branch management
-----------------
### Show current branch
	$ deployment branch testing bbs.example.com 
	* master
### Create branch
	$ deployment branch testing bbs.example.com -n development
	Switched to a new branch 'development'
	$ deployment branch testing bbs.example.com -n testing
	Switched to a new branch 'testing'
	$ deployment branch testing bbs.example.com -n production
	Switched to a new branch 'production'
	
	$ deployment branch testing bbs.example.com 
	  development
	  master
	* production
	  testing
### Checkout branch
	$ deployment branch testing bbs.example.com -c master
	HEAD is now at f9ed461 Update 5.5.8.sh
	Switched to branch 'master'
	
	$ deployment branch testing bbs.example.com 
	  development
	* master
	  production
	  testing	
###	Delete branch
	$ deployment branch testing bbs.example.com -d beat
	error: Cannot delete the branch 'beat' which you are currently on.
	
	$ deployment branch testing bbs.example.com --delete=beat
	error: Cannot delete the branch 'beat' which you are currently on.
	
	$ deployment branch testing bbs.example.com -c master
	HEAD is now at f9ed461 Update 5.5.8.sh
	Switched to branch 'master'
	
	$ deployment branch testing bbs.example.com --delete=beat
	Deleted branch beat (was f9ed461).
	
	$ deployment branch testing bbs.example.com 
	* master	  
### Release version
	$ deployment branch testing bbs.example.com --release=10.0-RELEASE
	$ git tag 
	10.0-RELEASE

Backup
------
	$ deployment testing bbs.example.com --backup=/tmp/backup
	
Reset 
----
	$ deployment testing bbs.example.com --clean

Merge
-----
	$ deployment merge www.example.com -t master -f testing
	
### merge to testing form development
	$ deployment merge testing www.example.com 
	
### Merge to development from project1
	$ deployment development www.example.com -f project1

- - -

Node
====
	yum install xinetd rsync -y

	vim /etc/xinetd.d/rsync <<VIM > /dev/null 2>&1
	:%s/yes/no/
	:wq
	VIM

	cat > /etc/rsyncd.conf <<EOD
	uid = www
	gid = www
	use chroot = no
	max connections = 8
	pid file = /var/run/rsyncd.pid
	lock file = /var/run/rsync.lock
	log file = /var/log/rsyncd.log

	hosts deny=*
	hosts allow=192.168.2.0/255.255.255.0

	[www]
		uid = www
		gid = www
		path = /www
		ignore errors
		read only = no
		list = no
		auth users = www
		secrets file = /etc/rsyncd.passwd
		
	[example.com]
		uid = www
		gid = www
		path = /www/example.com
		ignore errors
		read only = no
		list = no
	
	EOD

	cat >> /etc/rsyncd.passwd <<EOF
	www:your_password
	EOF

	chmod 600 /etc/rsyncd.*
	chmod 600 /etc/rsyncd.passwd

	service xinetd restart
