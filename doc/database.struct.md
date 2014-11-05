Database
========

Backup struct of database

Help
------
    ./backup.mysql.struct.sh
	Usage: ./backup.mysql.struct.sh {init|start|stop|status|restart}

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
	$ ./backup.mysql.struct.sh init
	Initialized empty Git repository in /home/neo/backup/.git/
	
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