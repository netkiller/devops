#!/bin/bash
##################################################
# AUTHOR: Neo <netkiller@msn.com>
# WEBSITE: http://www.netkiller.cn
# Description£ºzabbix mongodb monitor
# Note£ºZabbix 3.2
# DateTime: 2016-11-23
##################################################
HOST=localhost
PORT=27017
USER=monitor
PASS=chen

index=$(echo $@ | tr " " ".")

status=$(echo "db.serverStatus().${index}" |mongo -u ${USER} -p ${PASS} admin --port ${PORT}|sed -n '3p')
 
#check if the output contains "NumberLong"
if [[ "$status" =~ "NumberLong"   ]];then
	echo $status|sed -n 's/NumberLong(//p'|sed -n 's/)//p'
else 
	echo $status
fi