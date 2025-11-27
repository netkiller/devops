#!/usr/bin/env python3
import sys

sys.path.insert(0, ".")
sys.path.insert(1, "/Users/neo/workspace/devops")
sys.path.insert(2, "/Users/neo/Github/devops")
sys.path.insert(3, "/srv/devops")

try:
    from netkiller.docker import *

    # from environment.experiment import experiment
    # from environment.development import development
    # from environment.production import production

    from compose.devops import devops
    from compose.demo import demo

    # from libexec.portainer import portainer
    from compose.database import database
    from compose.homeassistant import homeassistant

except ModuleNotFoundError as err:
    print("pip install netkiller-devops, %s" % (err))
    exit()

if __name__ == "__main__":
    try:
        docker = Docker()
        # docker.env({'DOCKER_HOST':'ssh://root@192.168.30.13','COMPOSE_PROJECT_NAME':'experiment'})
        # docker.sysctl({"vm.max_map_count": "262144"})
        docker.environment(database)
        # docker.environment(development)
        # docker.environment(logging)
        docker.environment(devops)
        docker.environment(homeassistant)
        # docker.environment(portainer)
        docker.environment(demo)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
