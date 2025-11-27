try:
    import os, sys
    module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, module)
    from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

rancher = Services('rancher')
rancher.container_name('rancher')
rancher.image('rancher/rancher:stable').restart('unless-stopped').volumes([
    '/var/lib/rancher/:/var/lib/rancher/',
    '/var/log/auditlog:/var/log/auditlog'
]).ports(['8080:80','443:443']).privileged()