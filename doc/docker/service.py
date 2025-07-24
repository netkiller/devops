#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-07-24
##############################################
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *

target = 'init'

dockerfile = Dockerfile("neo",'/srv/netkiller')
dockerfile.image('openjdk:latest').volume(['/opt/netkiller','/app']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
dockerfile.copy('index.html','/var/www')
# dockerfile.show()
# print('-'*60)

neo = Services('netkiller')
neo.build(dockerfile)
neo.image("netkiller:1.3.0")
# neo.show()
# print('-'*60)

development = Composes('development')
development.version('3.9')
development.services(neo)
development.show()
# development.workdir("/tmp/test")

# print('-'*60)
development.save('/tmp/neo.yaml')
development.debug()
