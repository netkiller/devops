Database
========

Backup database

Installion
------
    # cp shell/backup.mysql.sh /etc/cron.daily

Create backup user for your database.
------
    CREATE USER 'backup'@'localhost' IDENTIFIED BY 'SaJePoM6BAPOmOFOd7Xo3e1A52vEPE';
	GRANT SELECT, LOCK TABLES  ON *.* TO 'backup'@'localhost';
	FLUSH PRIVILEGES;
	SHOW GRANTS FOR 'backup'@'localhost';


Database connect infomation
------
	BACKUP_HOST="localhost"
	BACKUP_USER="backup"
	BACKUP_PASS="SaJePoM6BAPOmOFOd7Xo3e1A52vEPE"
	BACKUP_DIR=/backup/database
	BACKUP_DBNAME="dbname"

Initialize the working directory
------
	$ mkdir -p /backup/database
	
Running 
------
    # /etc/cron.daily/backup.mysql.sh