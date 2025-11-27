#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Data. : 2023-06-28
##############################################
try:
    from netkiller.docker import *
except ImportError as err:
    print("%s" % (err))

volumes = Volumes()
volumes.create("elasticdata")
volumes.create("elasticplugins")

# extra_hosts = []

elasticsearch = Services("elasticsearch")
elasticsearch.image("docker.elastic.co/elasticsearch/elasticsearch:8.8.1")
elasticsearch.container_name("elasticsearch")
elasticsearch.restart("always")
# elasticsearch.hostname("elasticsearch.netkiller.cn")
# elasticsearch.extra_hosts(extra_hosts)
# elasticsearch.environment(['TZ=Asia/Shanghai'])
elasticsearch.environment({"TZ": "Asia/Shanghai", "ES_JAVA_OPTS": "-Xms1g -Xmx1g", "discovery.type": "single-node", "xpack.security.enabled": "false", "ELASTIC_PASSWORD": "passw0rd"})
elasticsearch.ports(["9200:9200", "9300:9300"])
elasticsearch.volumes(["elasticdata:/usr/share/elasticsearch/data", "elasticplugins:/usr/share/elasticsearch/plugins"])
elasticsearch.privileged(True)

# compose = Composes('elasticsearch')
# compose.version('3.9')
# compose.services(elasticsearch)
