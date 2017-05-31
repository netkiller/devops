Software Deployment Utility Programs
======

Create a user for deploy
-----

	groupadd -g 80 www
	adduser -o --home /www --uid 80 --gid 80 -c "Web Application" www

Deploy public key
-----
	$ ssh-keygen 
	Generating public/private rsa key pair.
	Enter file in which to save the key (/www/.ssh/id_rsa): 
	Created directory '/www/.ssh'.
	Enter passphrase (empty for no passphrase): 
	Enter same passphrase again: 
	Your identification has been saved in /www/.ssh/id_rsa.
	Your public key has been saved in /www/.ssh/id_rsa.pub.
	The key fingerprint is:
	dd:bb:51:f6:4e:f7:33:49:c6:7c:4c:5c:a7:fb:05:00 www@iZ62yln3rjjZ
	The key's randomart image is:
	+--[ RSA 2048]----+
	|          E.     |
	|            .   o|
	|             . oo|
	|         . .  o o|
	|        S . . == |
	|             +.*+|
	|            o o.B|
	|             o *+|
	|            .   =|
	+-----------------+

	Copy key file to remote server.
	
	$ ssh-copy-id www@203.88.18.17
	The authenticity of host '203.88.18.17 (203.88.18.17)' can't be established.
	ECDSA key fingerprint is b8:58:b5:65:00:27:0b:a8:c6:d8:dc:71:58:f9:00:db.
	Are you sure you want to continue connecting (yes/no)? yes
	/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
	/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
	www@203.88.18.17's password: 

	Number of key(s) added: 1

	Now try logging into the machine, with:   "ssh 'www@203.88.18.17'"
	and check to make sure that only the key(s) you wanted were added.
	
	Add Deploy key for Git (Github/Gitlab)
	
	$ cat ~/.ssh/id_rsa.pub 
	ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfMbpXWGmnM2lCnfypjL3TzkKetzpMq1ijt0b2rb/
	RVV0Ajhndvz6no1OJ5FZRhXmTcuBKk0YQQCO65vySTGZzl2+Ui1pgBA++9ZCJZFv1A0DM65RXPjVNFb
	DP9omx+huuxB+1spJF3IxsIQWJ53lnetKHlJ80UNeAo3VF8MgYrS8LJikc53aa40wKlhcuPjI0oUXpb
	LTR6iXgOKgF5+aCxcIGWIr7+5i0pFBwCb9ObCmmK602kVnVkGoyziIxRwx37DhtTT4sx1orrQP+4RAQ
	ya/ZXbfh3P+JGyA0rfMuQ8UV8zOHWqfwknDmpZlQ+ZJ9x8OChu+rhY1L46H www@exampe.com

	
Help
----
	$ deployment backup production appmanager.example.com
	Usage: deployment [options] {branch|stage} project

	Options:
	  -h, --help            show this help message and exit

	  stage:
		{development | testing | production | stable | unstable | alpha |
		beta} <host>.<domain>

		-r REVERT, --revert=REVERT
							revert to revision
		--clean             
		-s, --silent        Silent mode. Don't output anything
		--backup=BACKUP     backup remote to local

	  branch:
		branch management

		-c master|trunk, --checkout=master|trunk
							checkout branch
		-n branch, --new=branch
							Create new branch
		-d branch, --delete=branch
							delete branch
		--release=RELEASE   release version exampe:2015-01-15

	  merge:
		merge {development | testing | production}

		-t master, --to=master
							such as master
		-f your, --from=your
							from branch

	  unittest:
		unittest {development | testing | production}

	  Example: 
		deployment testing www.example.com
		deployment production www.example.com --clean
		deployment testing bbs.example.com --backup=/tmp/backup

	  Homepage: http://netkiller.github.com	Author: Neo <netkiller@msn.com>

Configure
---------
	$ mkdir ~/{development,testing,production}
	$ mkdir ~/{exclude,log}
	$ mkdir ~/{stable,unstable,nightly}
	
	$ vim ~/testing/example.com.ini 
	[www]
	;repository=git@192.168.2.1:example.com/www.example.com
	repository=https://github.com/oscm/shell.git
	source=/tmp/repo
	option=--delete --password-file=confure/production/example.com/passwd
	exclude=testing/www.example.com.lst
	logfile=/tmp/www.example.com
	remote=www@192.168.2.15
	destination=example.com/www.example.com

	[inf]
	repository=git@192.168.6.1:example.com/inf.example.com
	delete=Y
	mode=ssh
	backup=~/backup
	exclude=inf.example.com.lst
	remote=www@220.82.21.3,www@220.82.21.13
	destination=example.com/inf.example.com	
	
	[bbs]
	repository=https://github.com/example.com/bbs.example.com.git
	remote=www@192.168.2.15
	destination=example.com/bbs.example.com
	
	[images]
	repository=https://github.com/example.com/images.example.com.git
	remote=www@192.168.2.15
	destination=example.com/images.example.com
	branch=freebsd
	
	[windows]
	repository=git@192.168.2.1:example.com/windows.example.com
	delete=Y
	mode=ssh
	backup=/cygdrive/d/backup
	remote=administrator@158.99.11.168
	destination=/cygdrive/d/windows.example.com

### yuicompressor

	yuicompressor=all|css|js
	
	[m]
	repository=git@localhost:netkiller.cn/m.netkiller.cn.git
	branch=development
	delete=Y
	mode=ssh
	backup=~/backup
	remote=www@www.netkiller.cn
	destination=netkiller.cn/m.netkiller.cn
	include=m.netkiller.cn.lst
	exclude=m.netkiller.cn.lst
	yuicompressor=css
	
	* You need to install yuicompressor. FYI:
	curl -s https://raw.githubusercontent.com/oscm/shell/master/lang/java/devel/YUICompressor.sh | bash

### gulp
	
	[m]
	repository=git@localhost:netkiller.cn/m.netkiller.cn.git
	branch=development
	delete=Y
	mode=ssh
	backup=~/backup
	remote=www@www.netkiller.cn
	destination=netkiller.cn/m.netkiller.cn
	include=m.netkiller.cn.lst
	exclude=m.netkiller.cn.lst
	gulp=all
	gulp.path=/www/gulp
	gulp.gulpfile=gulpfile.js
	
	* cd <gulp.path> && gulp <gulp.gulpfile> 
	
Parameter replaces
-----
	create config file under the stage folder.
	vim config/testing/www.example.com.ini
	[config/database.php]
	host=localhost
	port=3306
	user=root
	password=passw0rd
	[config/redis.php]
	host=localhost
	port=6379
	
### Format of config item
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
