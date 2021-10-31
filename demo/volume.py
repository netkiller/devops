import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,module)

from netkiller.docker import *

volume = Volumes('redis')
volume.create('mongo')

compose = Composes('development')
compose.version('3.9')
# compose.services(service)
# compose.services(sms)
# compose.networks(network)
# compose.networks(mynet)
compose.volumes(volume)
print(compose.dump())