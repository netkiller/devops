Database
========

Backup struct of database

Help
------
	cp /usr/local/libexec/devops/backup.mysql.struct.sh /usr/local/bin/
	chmod +x /usr/local/bin/backup.mysql.struct.sh
    backup.mysql.struct.sh
	Usage: ./backup.mysql.struct.sh {init|start|stop|status|restart}

## SSH Key

	使用 ssh-keygen 创建 SSH 密钥对
	[www@gitlab ~]$ ssh-keygen 
	Generating public/private rsa key pair.
	Enter file in which to save the key (/home/www/.ssh/id_rsa): 
	Enter passphrase (empty for no passphrase): 
	Enter same passphrase again: 
	Your identification has been saved in /home/www/.ssh/id_rsa.
	Your public key has been saved in /home/www/.ssh/id_rsa.pub.
	The key fingerprint is:
	SHA256:B/CxaTdcjobhj5KmamQ1TKmRhpveaniTArKsqM9SbT8 www@gitlab
	The key's randomart image is:
	+---[RSA 3072]----+
	| . . .. o   .    |
	|. + o  + B +     |
	| + =    O * .    |
	|o . +  o * .     |
	|. .o .+ S o      |
	|o.+.oo . .       |
	|==.o..           |
	|*==.  E          |
	|B*+.   .         |
	+----[SHA256]-----+

	复制公钥证书，并且配置到 Gitlab 中

	[www@gitlab ~]$ cat .ssh/id_rsa.pub 
	ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/IVVbu0XxDbaEbXiW8rw3ECJ1uduWCXO4Yh8gFNgF+fbKI8MZcrGQJnu3Y/TdvmDsv6ktWLx3ZgBoQQYrxm54ddinhIkzjxfGhRpYa1OzAj2FO82PoVHJtSAFj8eCu4EeQqNaERyRuIuHSlgQpazk+9d5hPywJHAwejoprf6m/1DeYbdGge6+GpV5FewxgoRs5knntH3GT0EL5BP3mI1Yje3tpw0jwi7fyFWC20mqLbfRGHh0/VjvzNE+izChyym9Nb4aYk3jrz+q0ehOD3H0KOv0ACP9aAFFv/QvNtx8O7KSABgBdwMca3HgKiT1XPEwf1eH1COPSbKqODEhtKXSJIYJgxVgvLBfGuj8L/TVUh0WIGPhcCK+DsFb8xnBMstAeS1TD5U2wyf+hIJy98xdTG2prhZm2ZzKLyqj11L8VjPXQqF7TQcJUVuoVYJBeJmkibCsKq5vRcJt5mDwG5bzfikRxmnvsT5Yfvw6hTENxVZ6EfuZDyyOsfqkWX2EhBc= www@gitlab

	设置GIT用户信息

	git config --global user.email "you@example.com"
  	git config --global user.name "Your Name"

Create backup user for your database.
------
    CREATE USER 'backup'@'localhost' IDENTIFIED BY 'SaJePoM6BAPOmOFOd7Xo3e1A52vEPE';
	GRANT SELECT, LOCK TABLES  ON *.* TO 'backup'@'localhost';
	FLUSH PRIVILEGES;
	SHOW GRANTS FOR 'backup'@'localhost';


Database connect infomation
------
	BACKUP_HOST="localhost"
	BACKUP_USER="netkiller"
	BACKUP_PASS="chen"
	BACKUP_DBNAME="test aabbcc"
	BACKUP_DIR=~/backup

Initialize the working directory
------
	[www@gitlab ~]$ backup.mysql.struct init
	Cloning into '/home/www/.backup'...
	The authenticity of host '192.168.30.5 (192.168.30.5)' can't be established.
	ECDSA key fingerprint is SHA256:iR4AqKofuqLFQ2o+aUWU0Iokl1EtQmHLKM8Wi/EE9D0.
	Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
	Warning: Permanently added '192.168.30.5' (ECDSA) to the list of known hosts.
	remote: Enumerating objects: 3, done.
	remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 3
	Receiving objects: 100% (3/3), done.
	
Start 
------
    $ ./backup.mysql.struct.sh start

Stop
------
	$ ./backup.mysql.struct.sh stop

Status
-----
	$ ./backup.mysql.struct.sh status
	19837 pts/0    S      0:00 /bin/bash ./backup.mysql.struct.sh start

Diff
-----
	$ cd ~/backup
	$ git diff HEAD^ test.sql
	diff --git a/localhost/test.sql b/localhost/test.sql
	index a749b5a..402d6d1 100644
	--- a/localhost/test.sql
	+++ b/localhost/test.sql
	@@ -53,6 +53,7 @@ DROP TABLE IF EXISTS `test`;
	 /*!40101 SET character_set_client = utf8 */;
	 CREATE TABLE `test` (
	   `id` int(11) DEFAULT NULL,
	+  `key` char(50) DEFAULT NULL,
	   `val` char(10) DEFAULT NULL
	 ) ENGINE=BLACKHOLE DEFAULT CHARSET=latin1;
	 /*!40101 SET character_set_client = @saved_cs_client */;

## DevOps CI/CD

	Gitlab 创建流水线 .gitlab-ci.yml 写入

	stages:
	- build

	build-job:
	stage: build
	script:
		- wechat -t 1 数据库结构变更通知 "http://192.168.30.5/netkiller.cn/db.netkiller.cn/-/commit/${CI_COMMIT_SHA}"
		- wechat -t 1 "$(git diff HEAD^)"