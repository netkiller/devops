#!/bin/bash
##################################################
# AUTHOR: Neo <netkiller@msn.com>
# WEBSITE: http://www.netkiller.cn
# Description：zabbix 通过 status 模块监控 php-fpm
# Note：Zabbix 3.2
# DateTime: 2016-11-22
##################################################

HOST="localhost"
PORT="80"
status="status"

function query() {
	curl -s http://${HOST}:${PORT}/${status}?xml | grep "<$1>" | awk -F'>|<' '{ print $3}'
}

if [ $# == 0 ]; then
		echo $"Usage $0 {pool|process-manager|start-time|start-since|accepted-conn|listen-queue|max-listen-queue|listen-queue-len|idle-processes|active-processes|total-processes|max-active-processes|max-children-reached|slow-requests}"
		exit
else
	query "$1"
fi