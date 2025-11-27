#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Data. : 2023-07-21
##############################################
try:
    from netkiller.docker import *
except ImportError as err:
    print("%s" % (err))

# extra_hosts = []

redis = Services("redis")
redis.image("redis:latest")
redis.container_name("redis")
redis.restart("always")
# redis.hostname("redis.netkiller.cn")
# redis.extra_hosts(extra_hosts)
# redis.environment(['TZ=Asia/Shanghai'])
redis.environment(
    {
        "TZ": "Asia/Shanghai",
        "LANG": "en_US.UTF-8",
    }
)
redis.ports(["6379:6379"])
redis.volumes(["redis:/data"])
redis.sysctls({'net.core.somaxconn':'511'})
redis.command(
    [
              '--requirepass passw0rd',
      '--appendonly yes'
    ]
)
# .privileged(True)