from netkiller.docker import *
from compose.service.mosquitto import *
from compose.service.elasticsearch import *

homeassistant = Composes("homeassistant")
homeassistant.version("3.9")
homeassistant.services(mosquitto)
homeassistant.services(elasticsearch)
homeassistant.volumes(volumes)
