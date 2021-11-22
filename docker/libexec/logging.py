try:
    import os, sys
    module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, module)
    from netkiller.docker import *
except ImportError as err:
	print("%s" %(err))

fluentd = Services('fluentd')
fluentd.image('fluent/fluentd:latest').container_name('fluentd').hostname('fluentd.sfzito.com').restart('always')
fluentd.volumes(
	[
		'/opt/sfzito.com/ops.sfzito.com/fluentd/conf/fluentd.conf:/fluentd/etc/fluentd.conf',
		'/var/log/fluentd:/var/log/fluentd'
	]
).ports("24224:24224").environment(['FLUENTD_CONF=fluentd.conf'])

logging = Composes('logging')
logging.version('3.9')
# logging.env({'DOCKER_HOST': 'ssh://root@192.168.30.11'})
# logging.volumes(volumes)
logging.services(fluentd)