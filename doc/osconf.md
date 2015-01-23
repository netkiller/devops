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

	  editor:
		-e                  default editor is vim
		--edit=nano         choose from vi, vim, nano

	  repositories:
		--init=directory    init local repositories
		--clone=http://domain/project.git
							clone git repositories
		--pull              pull config from remote repositories
		--push              push config to remote repositories
		--commit            commit config to repositories

	  Homepage: http://netkiller.github.io	Author: Neo <netkiller@msn.com>

Init repo
-----
	$ osconf --init=/tmp/test

Clone repo
-----
	$ osconf --clone=/tmp/test
	$ osconf --clone=https://github.com/oscm/shell.git
	
get config file
-----
	# get directory
	$ osconf -g root@192.168.6.10 /etc/nginx/
	
	# get a file
	$ osconf -g root@192.168.6.10 /etc/passwd