# Elasticsearch for Zabbix 3.2

## install python3

	# yum install -y python34
	
	# wget https://raw.githubusercontent.com/oscm/zabbix/master/elasticsearch/userparameter_elasticsearch.conf -P /etc/zabbix/zabbix_agentd.d/
	
	# wget https://raw.githubusercontent.com/oscm/zabbix/master/elasticsearch/elasticsearch -P /srv/zabbix/libexec
	
	# chmod +x /srv/zabbix/libexec/elasticsearch
	
	# /srv/zabbix/libexec/elasticsearch indices _all.total.flush.total_time_in_millis
	25557
	
	# systemctl restart zabbix-agent
	
## Test Agent

	# zabbix_get -s 10.47.33.124 -k 'elasticsearch.status[indices,_all.total.flush.total_time_in_millis]'
	25557

## Import template
	
	https://github.com/oscm/zabbix/blob/master/elasticsearch/zbx_export_templates.xml

