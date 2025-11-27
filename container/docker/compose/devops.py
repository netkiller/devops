from netkiller.docker import *
from compose.service.kubernetes import *
from compose.service.gitlab import *
from compose.service.zentao import *

devops = Composes('devops')
devops.version('3.9')
# devops.volumes(volumes)
devops.services(gitlab)
devops.services(runner)
# devops.services(portainer)
# devops.services(agent)
devops.services(rancher)
devops.services(zentao)