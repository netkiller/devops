System Configuration Management
========
	Usage: osconf [options] node file

	System Configuration Management

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -d, --daemon          run as daemon

	  Configuration Management:
		-g, --get             get config from remote
		-p, --put             put config to remote	  
		--list              show nodes message
		-e                  default editor is vim
		--edit=nano         choose from vi, vim, nano

	  Repositories Management:
		--init=directory    init local repositories
		--clone=http://domain/project.git
							clone git repositories
		--pull              pull config from remote repositories
		--push              push config to remote repositories
		--add=/path/to/file
							add file to repositories
		--status            show status
		--commit=message    commit to local repositories
		--log               show log

	  Homepage: http://netkiller.github.io	Author: Neo <netkiller@msn.com>

Configure
-----

	$ cat /srv/devops/etc/os.ini
	[main]
	logfile=~/log/osconf.log
	logdir=~/log
	repositories=~/.osconf
	backup=~/.backup
	suffix=''

	[www.example.com]
	user=www
	file.iptable=/etc/sysconfig/iptables
	[news.example.com]
	host=www@news.example.com

Configuration Management
-----
	
### Init repo

	$ osconf --init=/path/to/system

### Clone repo

	$ osconf --clone=/path/to/system
	$ osconf --clone=https://github.com/oscm/shell.git
	$ osconf --clone=git@git.netkiller.cn:example.com/os.example.com.git
	
### Get config from remote
	# get directory
	$ osconf -g root@192.168.6.10 /etc/nginx/
	
	# get a file
	$ osconf -g root@192.168.6.10 /etc/passwd
	
### Put config to remote

	$ osconf -p root@192.168.6.10 /etc/nginx/nginx.conf

### Edit config

	$ osconf -e root@192.168.6.10 /etc/nginx/nginx/conf.d/default.conf

Repositories Management	
-----

### Add
	$ osconf --add=*

### Commmit 
	# osconf --commit=www.exampe.com
	
### Push
	# osconf --push

### Show log
	# osconf --log
	commit 60b45947f65195d3e8c9b99f53b24792ef361e21
	Author: netkiller <netkiller@msn.com>
	Date:   Fri Apr 15 11:40:55 2016 +0800

		www.exmaple.com
	-


Example
-----

### Initialization

	# install key file to remote host.
	
	# ssh-keygen
	Generating public/private rsa key pair.
	Enter file in which to save the key (/root/.ssh/id_rsa): 
	Enter passphrase (empty for no passphrase): 
	Enter same passphrase again: 
	Your identification has been saved in /root/.ssh/id_rsa.
	Your public key has been saved in /root/.ssh/id_rsa.pub.
	The key fingerprint is:
	f0:db:30:99:1e:72:5a:0f:9d:a7:2d:66:ad:01:ca:2a root@localhost.localdomain
	The key's randomart image is:
	+--[ RSA 2048]----+
	|                 |
	|                 |
	|      .          |
	|       o + .     |
	|      . S o .    |
	|     . B X =     |
	|      + o O o    |
	|  E  .   o +     |
	|   ..     .      |
	+-----------------+

	$ ssh-copy-id root@host

	$ osconf --init=system
	Initialized empty Git repository in /opt/www/system/.git/
	-

### Edit file os.ini
	
	[main]
	repositories=~/system
	
### Get some of config file.

	$ osconf -g root@192.168.6.10 /etc/nginx/
	
### Edit config file.
	$ osconf -e www@47.90.1.240 /etc/nginx/nginx/conf.d/default.conf
	
### Put file to remote host.

	$ osconf -p www@47.90.1.240 /etc/nginx/nginx/conf.d/default.conf
	
	
