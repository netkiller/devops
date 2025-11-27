try:
    import os, sys
    module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, module)
    from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

gui = Services('portainer')
gui.container_name('portainer')
gui.image('portainer/portainer-ce').restart('always').volumes([
    '/var/run/docker.sock:/var/run/docker.sock',
    'portainter:/data'
]).ports(['8000:8000','9000:9000'])

agent = Services('portainer-agent')
agent.container_name('portainer-agent')
agent.image('portainer/agent').restart('always').volumes([
    '/var/run/docker.sock:/var/run/docker.sock',
    '/var/lib/docker/volumes:/var/lib/docker/volumes'
]).ports(['8000:8000','9000:9000'])

volumes = Volumes()
volumes.create('portainter')

portainer = Composes('portainer')
portainer.version('3.9')
portainer.volumes(volumes)
portainer.services(gui)
portainer.services(agent)
