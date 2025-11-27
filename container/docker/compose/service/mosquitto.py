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

# extra_hosts = []

mosquitto = Services("mosquitto")
mosquitto.image("eclipse-mosquitto:latest")
mosquitto.container_name("mosquitto")
mosquitto.restart("always")
# mosquitto.hostname("mosquitto.netkiller.cn")
# mosquitto.extra_hosts(extra_hosts)
# mosquitto.environment(['TZ=Asia/Shanghai'])
# mosquitto.environment({"TA": "Asia/Shanghai", "MYSQL_ROOT_PASSWORD": "123456"})
mosquitto.ports(["1883:1883", "9001:9001"])
mosquitto.volumes(["/srv/mosquitto/config/mosquitto.conf:/mosquitto/config/mosquitto.conf", "/srv/mosquitto/config/pwfile.conf:/mosquitto/config/pwfile.conf"])
mosquitto.privileged(True)

# mosquitto_passwd -b /mosquitto/config/pwfile.conf netkiller passw0rd

# compose = Composes('mosquitto')
# compose.version('3.9')
# compose.services(mosquitto)
