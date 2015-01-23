System Configuration Management
========
	Usage: osconf [options] node file

	System Configuration Management

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -d, --daemon          run as daemon
	  -g, --get             get config from remote
	  -p, --put             put config to remote

	  Configuration Management:
		--list              show module message
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

Init repo
-----
	$ osconf --init=/tmp/test

Clone repo
-----
	$ osconf --clone=/tmp/test
	$ osconf --clone=https://github.com/oscm/shell.git
	
get config from remote
-----
	# get directory
	$ osconf -g root@192.168.6.10 /etc/nginx/
	
	# get a file
	$ osconf -g root@192.168.6.10 /etc/passwd
	
put config to remote
-----
	$ osconf -g root@192.168.6.10 /etc/nginx/nginx.conf
	
