import os
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

config = ConfigMap('test')
config.apiVersion('v1')
config.metadata().name('test').namespace('test')
config.from_file('resolv.conf', '/etc/resolv.conf')
config.from_file('ntp.conf', '/etc/mnt.conf')
config.debug()