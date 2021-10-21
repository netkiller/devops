# SQL Dump

## install 
    
    [root@netkiller ~]# pip3 install netkiller-devops --upgrade

## HELP

    [root@netkiller ~]# sqldump
    Netkiller database backup
    Usage: sqldump [options] <item item1 item2 ... item(n)>

    Options:
    -h, --help            show this help message and exit
    -c /usr/local/etc/dump.ini, --config=/usr/local/etc/dump.ini
                            config file
    -e, --edit            open the config file
    -a /opt/backup, --archive=/opt/backup
                            backup directory
    -l, --list            list items
    -H, --history         backup history
    --retain=30           The number of days retained
    --logfile=/var/log/dump.log
                            logs file.
    --debug               debug mode

    Compress or expand files:
        -z, --gzip          Gzip
        -u backup.sql.gz, --gunzip=backup.sql.gz
                            decompress files
        -s backup.sql.gz, --show=backup.sql.gz
                            print sql

    OpenGPG encrypt or decrypt files:
        -r netkiller@msn.com, --recipient=netkiller@msn.com
                            encrypt for USER-ID
        -g, --gpg           encrypt file
        -d backup.sql.gpg, --decrypt=backup.sql.gpg
                            decrypt file
        -S backup.sql.gpg, --stdout=backup.sql.gpg
                            print file

    Homepage: http://www.netkiller.cn	Author: Neo <netkiller@msn.com>

## 配置

    [root@netkiller ~]# sqldump -e
    [DEFAULT]
    ;directory=/opt/backup
    ;设置备份目录
    directory=/tmp/backup
    ;设置日志文件
    logfile=/tmp/dump.log

    [dev]
    host=192.168.30.11
    user=root
    pass=test
    dbname=test
    description=这是测试环境的数据库

    [test]
    host=192.168.10.10
    user=test
    pass=test
    dbname=test test1 test2 test3 test4

    [stage]
    user=root
    dbname=stage
    pass=
    dbname=test

    [prod]
    user=root
    dbname=prod
    pass=
    dbname=test

## 查看配置项

    [root@netkiller ~]# sqldump -l
    dev : 这是测试环境的数据库
    test
    stage
    prod

## 备份数据库

    常规备份，生产 SQL 文件

    [root@netkiller ~]# sqldump dev

    备份并压缩文件，使用 GZIP

    [root@netkiller ~]# sqldump dev -z

    备份，加密和压缩

    [root@netkiller ~]# sqldump dev -g
    The configuration item was not found: [dev] 'recipient'.

    需要在配置文件中加入 recipient=netkiller@msn.com 指定公钥证书，或者使用 -r 参数指定

    [root@netkiller ~]# sqldump dev -g -r netkiller@msn.com 

## 查看备份历史

    [root@netkiller ~]# sqldump dev -H
    dev :
        test.2021-10-21.16:10:03.sql
        test.2021-10-21.16:10:13.sql
        test.2021-10-21.16:11:14.sql
        test.2021-10-21.16:39:30.sql
        test.2021-10-21.16:40:04.sql.gz
        test.2021-10-21.16:37:32.sql
        test.2021-10-21.16:57:11.sql
        test.2021-10-21.16:57:18.sql
        test.2021-10-21.16:57:39.sql.gz
        test.2021-10-21.17:10:06.sql.gpg

