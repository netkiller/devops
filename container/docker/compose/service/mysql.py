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

mysql = Services("mysql")
mysql.image("mysql:latest")
mysql.container_name("mysql")
mysql.restart("always")
# mysql.hostname("mysql.netkiller.cn")
# mysql.extra_hosts(extra_hosts)
# mysql.environment(['TZ=Asia/Shanghai'])
mysql.environment(
    {
        "TZ": "Asia/Shanghai",
        "MYSQL_ROOT_PASSWORD": "0E8AAA08-D7CB-403C-8761-0FA8F23DB326",
    }
)
mysql.ports(["3306:3306"])
mysql.volumes(["/var/lib/mysql:/var/lib/mysql"])
mysql.command(
    [
        "--character-set-server=utf8mb4",
        "--collation-server=utf8mb4_general_ci",
        "--explicit_defaults_for_timestamp=true",
        "--lower_case_table_names=1",
        "--max_allowed_packet=128M",
        '--sql-mode="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO"',
    ]
)
# .privileged(True)
