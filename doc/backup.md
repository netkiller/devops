backup
======

Backup Software

Help
------
    $ ./backup --help
    Usage: backup [options] arg1 arg2 <task>
    
    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  write report to FILE
      -q, --quiet           don't print status messages to stdout
      --config=CONFIG       Read configuration options from file.
      --task=TASK           task config file.
      --schedule=SCHEDULE   schedule config file.
      -v, --version         print version number
      -d, --daemon          run as daemon
      --logfile=LOGFILE     logs file.
    
      arg1:
        arg1: task | schedule
    
      arg2:
        arg2: list | run
    
      Debug Options:
        --debug             Print debug information

New Task
------
    [www]
    policy=mirror
    from=/www/www.example.com/*
    to=/tmp/www
    exclude=.svn
    include=*
    
    [database]
    policy=mysql
    host=192.168.2.1
    port=3306
    user=www
    password=123456
    database=test
    compress=gzip
    to=/tmp

Run Task
------

    $ ./backup task list
    www
    htdocs
    database


New Schedule
------

    $ ./backup schedule show weekly
    www: True
    images: False
    
    $ ./backup schedule show monthly
    test: True
    test1: True
    test2: True


Run Schedule
------

    $ backup schedule list
    hourly
    daily
    weekly
    monthly


Crontab Schedule
------

    # m h  dom mon dow   command
    17 *    * * *   test -x /srv/sbin/backup || ( backup schedule run hourly )
    25 6    * * *   test -x /srv/sbin/backup || ( backup schedule run daily )
    47 6    * * 7   test -x /srv/sbin/backup || ( backup schedule run weekly )
    52 6    1 * *   test -x /srv/sbin/backup || ( backup schedule run monthly )
    
    
    */30 * * * * /srv/sbin/backup task run www

