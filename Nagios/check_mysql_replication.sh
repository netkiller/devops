#!/bin/bash
##################################################
# Author: neo chan<netkiller@msn.com>
# Website: http://netkiller.github.io
##################################################
#~/.my.cnf
#[client]
#host= whatever
#port=whatever
#user=whatever
#password=whatever
##################################################
declare -a active

help="check_mysql_replication.sh (c) 2015 CC licence
Usage: check_mysql_replication.sh -H host -P port -u username -p password [-w integer] [-c integer]
\tcheck_mysql_replication.sh -f ~/.my.cnf [-w integer] [-c integer]
Attention: you must be create a user for monitor as CLIENT REPLICATION rights on the server. 
Example:\n\tGRANT REPLICATION CLIENT on *.* TO 'nagios'@'%' IDENTIFIED BY 'secret';"

if [ "${1}" = "--help" -o "${#}" = "0" ];
	then
	echo -e "${help}";
	exit 1;
fi

host=localhost
port=3306
#cnf=~/.my.cnf

while getopts "H:P:u:p:f:w:c:h" Input;
do
	case ${Input} in
	H)	host=${OPTARG};;
	P)	port=${OPTARG};;
	u)	user=${OPTARG};;
	p)	password=${OPTARG};;
	f)	cnf=${OPTARG};;
	w)      warn_delay=${OPTARG};;
	c)      crit_delay=${OPTARG};;
	h)      echo -e "${help}"; exit 1;;
	\?)	echo "Wrong option given. Please use options -H for host, -P for port, -u for user and -p for password"
		exit 1
		;;
	esac
done

if [ ! -z $cnf ]; then
	MYSQL_OPT="--defaults-extra-file=${cnf}"
else
	MYSQL_OPT="-h ${host} -P ${port} -u${user} -p${password}"
fi
#echo $MYSQL_OPT
status=($(mysql $MYSQL_OPT -e "show slave status\G"| grep -E "Slave_IO_Running:|Slave_SQL_Running:|Seconds_Behind_Master:" |awk '{print $2}'))

#for item in ${status[*]}
#do
#	echo $item
#done

slave_io_running=${status[0]}
slave_sql_running=${status[1]}
seconds_behind_master=${status[2]}

if [ "${slave_io_running}" = "Yes" -a "${slave_sql_running}" = "Yes" ]; then
    echo "Slave replication is running"
    exit 0
else
    echo "Slave replication is broken"
    echo "Critical - slave is error"
    exit 2
fi

if [ "${seconds_behind_master}" == "NULL"]; then
    echo "Critical - slave is error"
elif [ ${seconds_behind_master}" -gt ${warn_delay} ]; then
    echo "WARNING: Slave replication is delayed"
elif [ ${seconds_behind_master}" -gt ${crit_delay} ]; then
    echo "CRITICAL: Slave is ${seconds_behind_master} seconds behind Master"
fi
