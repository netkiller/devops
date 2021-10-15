#-*- coding: utf-8 -*-
import os, sys
import yaml,json
import logging, logging.handlers
from optparse import OptionParser, OptionGroup

class Networks():
	def __init__(self, name=None): 
		self.networks = {}
		if name :
			self.name = name
		else:
			self.name = 'default'
		self.networks[self.name] = {}
	def driver(self, name="bridge"):
		self.networks[self.name]['driver'] = name
		return(self)
	def ipam(self):
		return(self.Ipam(self.networks[self.name]))
	class Ipam():
		def __init__(self,obj):
			self.networks = obj
			# print(self.networks)
			self.networks['ipam'] = {}
		def driver(self, name="default"):
			self.networks['ipam']['driver'] = name
			return(self)
		def config(self, array):
			self.networks['ipam']['config'] = array
			return(self)

class Volumes():
	def __init__(self, name="None"): 
		self.volumes = {}
		if name :
			self.volumes[name] = None
	def add(self, name):
		self.volumes[name] = None
		return(self)
		
class Services():	
	# service = {}
	def __init__(self, name): 
		self.service = {}
		self.name = name
		self.service[self.name]={}
	def image(self, name):
		self.service[self.name]['image']= name
		return(self)
	def container_name(self,name=None):
		if not name :
			name = self.name
		self.service[self.name]['container_name'] =name
		return(self)
	def restart(self,value='always'):
		self.service[self.name]['restart'] =value
		return(self)	
	def hostname(self,value='localhost.localdomain'):
		self.service[self.name]['hostname'] =value
		return(self)
	def extra_hosts(self,array=[]):
		self.service[self.name]['extra_hosts'] = array
		return(self)
	def environment(self, obj):
		if not 'environment' in self.service[self.name].keys() :
			self.service[self.name]['environment']=[]
		if type(obj) == str:
			self.service[self.name]['environment'].append(obj)
		elif type(obj) == list:
			self.service[self.name]['environment'].extend(obj)
		else:
			self.service[self.name]['environment'] = obj
		return(self)
	def env_file(self, array=[]):
		self.service[self.name]['env_file'] = array
		return(self)
	def ports(self, obj):
		if not 'ports' in self.service[self.name].keys() :
			self.service[self.name]['ports']=[]
		if type(obj) == str:
			self.service[self.name]['ports'].append(obj)
		elif type(obj) == list:
			self.service[self.name]['ports'].extend(obj)
		else:
			self.service[self.name]['ports'] = obj
		return(self)
	def expose(self, obj):
		if not 'expose' in self.service[self.name].keys() :
			self.service[self.name]['expose']=[]
		if type(obj) == str:
			self.service[self.name]['expose'].append(obj)
		elif type(obj) == list:
			self.service[self.name]['expose'].extend(obj)
		else:
			self.service[self.name]['expose'] = obj
		return(self)
	def working_dir(self, dir='/'):
		self.service[self.name]['working_dir'] = dir
		return(self)
	def volumes(self, array):
		self.service[self.name]['volumes'] = array
		return(self)
	def networks(self, array):
		self.service[self.name]['networks'] = array
		return(self)
	def sysctls(self,array):
		self.service[self.name]['sysctls'] = array
		return(self)
	def entrypoint(self, cmd):
		self.service[self.name]['entrypoint'] = cmd
		return(self)
	def command(self, array=[]):
		self.service[self.name]['command'] = array
		return(self)
	def depends_on(self, obj):
		if not 'depends_on' in self.service[self.name].keys() :
			self.service[self.name]['depends_on']=[]
		if isinstance(obj, Services):
			self.service[self.name]['depends_on'].append(obj.name)
		elif type(obj) == str:
			self.service[self.name]['depends_on'].append(obj)
		elif type(obj) == list:
			self.service[self.name]['depends_on'].extend(obj)	
		else:	
			self.service[self.name]['depends_on'] = obj
		return(self)
	def links(self, obj):
		if isinstance(obj, Services):
			self.service[self.name]['links'].append(obj.name)
		elif type(obj) == str:
			self.service[self.name]['links'].append(obj)
		elif type(obj) == list:
			self.service[self.name]['links'].extend(obj)
		else:	
			self.service[self.name]['links'] = obj
		return(self)
	def depends_on_object(self,obj):
		if isinstance(obj, Services):
			self.service[self.name]['depends_on'].append(obj.name)
		elif type(obj) == list:
			depends = []
			if isinstance(obj[0], Services):
				for o in obj:
					depends.append(o.name)
				self.service[self.name]['depends_on'] = depends
	def logging(self, driver="json-file", options=None):
		self.service[self.name]['logging'] = {'driver': driver}
		if options :
			self.service[self.name]['logging'].update({'options': options})
		return(self)
	def dump(self):
		return(yaml.dump(self.service))
	def debug(self):
		print(self.service)
		
class Composes():
	compose = {}
	daemon = False
	basedir = ''
	def __init__(self, name): 
		self.compose = {}
		self.name = name
		self.logging = logging.getLogger()
		self.compose['services'] = {}
		# self.compose['networks'] = []
	def version(self, version):
		self.compose['version'] = str(version)
		return(self)
	def services(self,obj):
		self.compose['services'].update(obj.service)
		return(self)
	def networks(self, obj):
		self.compose['networks'] = obj.networks
		return(self)
	def volumes(self, obj):
		self.compose['volumes'] = obj.volumes
		return(self)
	def debug(self):
		jsonformat = json.dumps(self.compose, sort_keys=True, indent=4, separators=(',', ':'))
		return(jsonformat)
	def dump(self):
		return(yaml.dump(self.compose))
	def filename(self):
		return self.basedir +'/'+ self.name+'.yaml'
	def save(self, filename=None):
		try:
			if filename :
				file = open(filename,"w")
			else:
				file = open(self.filename(),"w")
			yaml.safe_dump(self.compose,stream=file,default_flow_style=False)
			self.logging.info("save %s" % (self.filename()))
		except Exception as e:
			self.logging.error(e)
			print(e)
			exit()
		return(self)
	def daemon(self,daemon = True):
		self.daemon = daemon
		return(self)
	def up(self, service=""):
		self.save()
		d = ''
		if self.daemon :
			d = '-d'
		command = "docker-compose -f {compose} up {daemon} {service}".format(compose=self.filename(), daemon=d, service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def rm(self,service=''):
		command = "docker-compose -f {compose} rm {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def restart(self,service=''):
		command = "docker-compose -f {compose} restart {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def start(self,service=''):
		command = "docker-compose -f {compose} start {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def stop(self,service=''):
		command = "docker-compose -f {compose} stop {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def stop(self,service=''):
		command = "docker-compose -f {compose} stop {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def ps(self,service=''):
		command = "docker-compose -f {compose} ps {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def top(self,service=''):
		command = "docker-compose -f {compose} top {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def images(self,service=''):
		command = "docker-compose -f {compose} images {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)		
	def logs(self,service='', follow = False):
		tail = ''
		if follow :
			tail = '-f --tail=50'
		command = "docker-compose -f {compose} logs {follow} {service}".format(compose=self.filename(), follow=tail,service=service)
		self.logging.debug(command)
		os.system(command)		
		return(self)
	def exec(self,service, cmd):
		command = "docker-compose -f {compose} exec {service} {cmd}".format(compose=self.filename(), service=service, cmd=cmd)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def kill(self,service):
		command = "docker-compose -f {compose} kill {service}".format(compose=self.filename(), service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def logfile(self, filename):
		logging.basicConfig(level=logging.NOTSET,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
			filename=filename,filemode='a')
		return(self)
	def workdir(self,path):
		os.makedirs( path,exist_ok=True);
		self.basedir = path
		self.logging.info('working dir is ' + self.basedir)
		return(self)
class Docker():

	def __init__(self): 
		self.composes= {}
		self.daemon = False
		usage = "usage: %prog [options] up|rm|start|stop|restart|logs|top|images|exec <service>"
		self.parser = OptionParser(usage)
		self.parser.add_option("", "--debug", action="store_true", dest="debug", help="debug mode")
		self.parser.add_option("-e", "--environment", dest="environment", help="environment", metavar="development|testing|production")
		self.parser.add_option('-d','--daemon', dest='daemon', action='store_true', help='run as daemon')
		self.parser.add_option('','--logfile', dest='logfile', help='logs file.', default='debug.log')
		self.parser.add_option('-l','--list', dest='list', action='store_true', help='print service of environment')
		self.parser.add_option('-f','--follow', dest='follow', action='store_true', help='following logging')
		self.parser.add_option('-c','--compose', dest='compose', action='store_true', help='show docker compose')
		self.parser.add_option('','--export', dest='export', action='store_true', help='export docker compose')

		(self.options, self.args) = self.parser.parse_args()
		if self.options.daemon :
			self.daemon = True
		self.logfile = self.options.logfile
		if self.options.logfile :
			logging.basicConfig(level=logging.NOTSET,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
			filename=self.options.logfile,filemode='a')

		self.logging = logging.getLogger()

	def environment(self, env):
		env.logfile(self.logfile)
		workdir = '/var/tmp/devops'
		env.workdir(workdir)
		self.composes[env.name] = env
		self.logging.info("environment %s : %s" % (env.name, workdir))
		return(self)
	def up(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			if self.daemon :
				composes.daemon().up(service)
			else:
				composes.up(service)
		else:
			for env,obj in self.composes.items():
				if self.daemon :
					obj.daemon().up(service)
				else:
					obj.up(service)
		return(self)
	def rm(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.rm(service)
		else:
			for env,obj in self.composes.items():
				obj.rm(service)
		return(self)
	def start(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.start(service)
		else:
			for env,obj in self.composes.items():
				obj.start(service)
		return(self)
	def stop(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.stop(service)
		else:
			for env,obj in self.composes.items():
				obj.stop(service)
		return(self)
	def restart(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.restart(service)
		else:
			for env,obj in self.composes.items():
				obj.restart(service)
		return(self)
	def ps(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.ps(service)
		else:
			for env,obj in self.composes.items():
				obj.ps(service)
		return(self)
	def top(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.top(service)
		else:
			for env,obj in self.composes.items():
				obj.top(service)
		return(self)
	def images(self,service=''):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.images(service)
		else:
			for env,obj in self.composes.items():
				obj.images(service)
		return(self)
	def logs(self,service='', follow=False):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.logs(service, follow)
		else:
			for env,obj in self.composes.items():
				obj.logs(service, follow)
		return(self)
	def list(self):
		if self.options.environment and self.options.environment in self.composes :
			print(self.options.environment,':')
			services = self.composes[self.options.environment].compose['services']
			for service in services :
				print(' '*4, service)
		else:
			for env,obj in self.composes.items():
				print(env,':')
				for service in obj.compose['services'] :
					print(' '*4, service)
		return(self)
	def dump(self):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.dump()
		else:
			for env,value in self.composes.items():
				print(value.dump())
	def save_all(self):
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.save(self.options.environment+'.yaml')
		else:
			for filename,value in self.composes.items():
				value.save(filename+'.yaml')
	def exec(self,service, array):
		cmd = ' '.join(array)
		if self.options.environment and self.options.environment in self.composes :
			composes = self.composes[self.options.environment]
			composes.exec(service, cmd)
		else:
			for env,obj in self.composes.items():
				obj.exec(service, cmd)
		return(self)
	def usage(self):
		print("Python controls the docker manager.")
		self.parser.print_help()
		print("\nHomepage: http://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>")
		exit()
	def main(self):
		if self.options.debug:
			print("===================================")
			print(self.options, self.args)
			print("===================================")
			self.logging.debug("="*50)
			self.logging.debug(self.options)
			self.logging.debug(self.args)
			self.logging.debug("="*50)
		
		if self.options.export :
			self.save_all()
			exit()
		if self.options.compose :
			self.dump()
			exit()
		if self.options.list :
			self.list()
			exit()
		if not self.args:
			self.usage()

		if len(self.args) > 1 :
			self.service = ' '.join(self.args[1:])
		else:
			self.service = ''

		self.logging.debug('service ' + self.service)
	
		if self.args[0] == 'up' :
			self.up(self.service)
			self.logging.info('up ' + self.service)
		elif self.args[0] == 'rm':
			self.rm(self.service)
			self.logging.info('rm ' + self.service)
		elif self.args[0] == 'start':
			self.start(self.service)
			self.logging.info('start ' + self.service)
		elif self.args[0] == 'stop':
			self.stop(self.service)
			self.logging.info('stop ' + self.service)
		elif self.args[0] == 'restart':
			self.restart(self.service)
			self.logging.info('restart' + self.service)
		elif self.args[0] == 'ps':
			self.ps(self.service)
		elif self.args[0] == 'top':
			self.top(self.service)
		elif self.args[0] == 'images':
			self.images(self.service)
		elif self.args[0] == 'logs':
			self.logs(self.service, self.options.follow)
		elif self.args[0] == 'exec':
			self.exec(self.service, self.args[2:])
		else:
			self.usage()
