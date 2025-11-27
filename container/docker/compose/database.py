from netkiller.docker import *
from compose.service.mysql import *
from compose.service.redis import *
from compose.volumes.redis import redis as data

database = Composes("database")
database.version("3.9")
database.services(mysql)
database.services(redis)
database.volumes(data)
