#!/bin/bash
##############################################
# Author: netkiller<netkiller@msn.com>
# Homepage: http://www.netkiller.cn
# $Author$
# $Id$
##############################################
NAME=deploy.gitlab
BASEDIR='/srv/deploy'
PROG=$BASEDIR/bin/$(basename $0)
LOGFILE=/var/tmp/$NAME.log
PIDFILE=/var/tmp/$NAME.pid
ACCESS_LOG=/var/tmp/$NAME.access.log
##############################################
PHP=/srv/php/bin/php
#HOST=0.0.0.0
HOST=127.0.0.1
PORT=8000
##############################################
#echo $$
#echo $BASHPID
function start(){
	if [ -f "$PIDFILE" ]; then
		echo $PIDFILE
		exit 2
	fi

	$PHP -d error_log=$LOGFILE -c /srv/php/etc/php-cli.ini -S $HOST:$PORT -t $BASEDIR &
	echo $! > $PIDFILE
}
function stop(){
  	[ -f $PIDFILE ] && kill `cat $PIDFILE` && rm -rf $PIDFILE
}
function status(){
        #ps ax | grep $NAME | grep -v grep | grep -v status
        ps ax | grep $BASEDIR | grep -v grep | grep -v status
}
case "$1" in
  start)
  	start
	;;
  stop)
  	stop
	;;
  status)
  	status
	;;
  restart)
  	stop
	start
	;;
  log)
	tail -f $LOGFILE
	;;
  *)
	echo $"Usage: $0 {start|stop|status|restart|log}"
	exit 2
esac

exit $?
