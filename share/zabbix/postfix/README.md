Zabbix for Postfix 3.2
=====

Install agent
-----

	yum install -y logcheck
	mkdir -p /srv/zabbix/libexec
	wget https://raw.githubusercontent.com/oscm/zabbix/master/postfix/postfix -P /srv/zabbix/libexec
	chmod +x /srv/zabbix/libexec/postfix
	
	wget https://raw.githubusercontent.com/oscm/zabbix/master/postfix/userparameter_postfix.conf -P /etc/zabbix/zabbix_agentd.d/
	systemctl restart zabbix-agent
	
	zabbix_get -s 13.24.22.53 -k 'agent.ping'