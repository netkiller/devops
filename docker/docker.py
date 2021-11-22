#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/neo/workspace/devops')

from netkiller.docker import *
# from environment.experiment import experiment
# from environment.development import development
# from environment.production import production

from libexec.gitlab import devops
from libexec.logging import logging
from libexec.portainer import portainer

# print(test)
# exit()

if __name__ == "__main__":
    try:
        docker = Docker()
        # docker.env({'DOCKER_HOST':'ssh://www@192.168.30.11'}) 
        # docker.sysctl({"vm.max_map_count": "262144"})
        # docker.environment(experiment)
        # docker.environment(development)
        docker.environment(logging)
        docker.environment(devops)
        docker.environment(portainer)
        
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")