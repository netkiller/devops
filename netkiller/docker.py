#-*- coding: utf-8 -*-
import os, sys
import yaml,json
import logging, logging.handlers
from optparse import OptionParser, OptionGroup

class Networks():
	networks = {}
	def __init__(self, name=None): 
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
	service = {}
	def __init__(self, name=None): 
		self.name = name
		self.service[name] = {}
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
	def environment(self, array=[]):
		self.service[self.name]['environment'] = array
		return(self)
	def env_file(self, array=[]):
		self.service[self.name]['env_file'] = array
		return(self)
	def ports(self, array):
		self.service[self.name]['ports'] = array
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
	def entrypoint(self, cmd):
		self.service[self.name]['entrypoint'] = cmd
		return(self)
	def command(self, array=[]):
		self.service[self.name]['command'] = array
		return(self)
	def dump(self):
		return(yaml.dump(self.service))
	def debug(self):
		print(self.service)
		
class Composes():
	compose = {}
	daemon = False
	def __init__(self, name): 
		self.compose = {}
		self.name = name
		self.filename = self.name+'.yaml'
		self.logging = logging.getLogger()

	def version(self, version):
		self.compose['version'] = str(version)
		return(self)
	def services(self,obj):
		self.compose['services'] = obj.service
		# print(obj.service)
		return(self)
	def networks(self, obj):
		# print(obj.networks)
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
	def save(self, filename=None):
		if filename :
			file = open(filename,"w")
		else:
			file = open(self.filename,"w")
		yaml.safe_dump(self.compose,stream=file,default_flow_style=False)
		return(self)
	def daemon(self,daemon = True):
		self.daemon = daemon
		return(self)
	def up(self, service=""):
		self.save()
		d = ''
		if self.daemon :
			d = '-d'
		command = "docker-compose -f {compose} up {daemon} {service}".format(compose=self.filename, daemon=d, service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def rm(self,service=''):
		command = "docker-compose -f {compose} rm {service}".format(compose=self.filename, service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def restart(self,service=''):
		command = "docker-compose -f {compose} restart {service}".format(compose=self.filename, service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def start(self,service=''):
		command = "docker-compose -f {compose} start {service}".format(compose=self.filename, service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def stop(self,service=''):
		command = "docker-compose -f {compose} stop {service}".format(compose=self.filename, service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def stop(self,service=''):
		command = "docker-compose -f {compose} stop {service}".format(compose=self.filename, service=service)
		self.logging.debug(command)
		os.system(command)	
		return(self)
	def ps(self,service=''):
		command = "docker-compose -f {compose} ps {service}".format(compose=self.filename, service=service)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def logs(self,service='', follow = False):
		tail = ''
		if follow :
			tail = '-f --tail=50'
		command = "docker-compose -f {compose} logs {follow} {service}".format(compose=self.filename, follow=tail,service=service)
		self.logging.debug(command)
		os.system(command)		
		return(self)
	def logfile(self, filename):
		logging.basicConfig(level=logging.NOTSET,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
			filename=filename,filemode='a')
		return(self)
	def workdir(self,path):
		os.makedirs( path,exist_ok=True);
		self.filename = path + '/' + self.filename
		self.logging.info('working dir is ' + self.filename)
		return(self)
class Docker():

	def __init__(self): 
		self.composes= {}
		self.daemon = False
		usage = "usage: %prog [options] up|rm|start|stop|restart <service>"
		self.parser = OptionParser(usage)
		# self.parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
		self.parser.add_option("", "--debug", action="store_true", dest="debug", help="debug mode")
		self.parser.add_option('-d','--daemon', dest='daemon', action='store_true', help='run as daemon')
		self.parser.add_option('-l','--logfile', dest='logfile', help='logs file.', default='debug.log')
		self.parser.add_option('-f','--follow', dest='follow', action='store_true', help='following logging')

		(options, args) = self.parser.parse_args()
		if options.daemon :
			self.daemon = True
		self.logfile = options.logfile
		if options.logfile :
			
			logging.basicConfig(level=logging.NOTSET,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
			filename=options.logfile,filemode='a')

		self.logging = logging.getLogger()

	def environment(self, env):
		env.logfile(self.logfile)
		# env.workdir('/tmp')
		self.composes[env.name] = env
		return(self)
	def up(self,service=''):
		for env,obj in self.composes.items():
			if self.daemon :
				obj.daemon().up(service)
			else:
				obj.up(service)
	def rm(self,service=''):
		for env,obj in self.composes.items():
			obj.rm(service)
		return(self)
	def start(self,service=''):
		for env,obj in self.composes.items():
			obj.start(service)
		return(self)
	def stop(self,service=''):
		for env,obj in self.composes.items():
			obj.stop(service)
		return(self)
	def restart(self,service=''):
		for env,obj in self.composes.items():
			obj.restart(service)
		return(self)
	def ps(self,service=''):
		for env,obj in self.composes.items():
			obj.ps(service)
		return(self)
	def logs(self,service='', follow=False):
		for env,obj in self.composes.items():
			obj.logs(service, follow)
		return(self)
	def dump(self):
		for env,value in self.composes.items():
			print(value.dump())
	def save_all(self):
		for filename,value in self.composes.items():
			file = open(filename,"w")
			yaml.safe_dump(value,stream=file,default_flow_style=False)

	def usage(self):
		self.parser.print_help()
		print("\nHomepage: http://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>")
		exit()
	def main(self):
		(options, args) = self.parser.parse_args()
		if options.debug:
			print("===================================")
			print(options, args)
			print("===================================")
		if not args:
			self.usage()

		if len(args) == 2 :
			self.service = args[1]
		else:
			self.service = ''

		if args[0] == 'up' :
			self.up(self.service)
			self.logging.info('up ' + self.service)
		elif args[0] == 'rm':
			self.rm(self.service)
			self.logging.info('rm ' + self.service)
		elif args[0] == 'start':
			self.start(self.service)
			self.logging.info('start ' + self.service)
		elif args[0] == 'stop':
			self.stop(self.service)
			self.logging.info('stop ' + self.service)
		elif args[0] == 'restart':
			self.restart(self.service)
			self.logging.info('restart' + self.service)
		elif args[0] == 'ps':
			self.ps(self.service)
		elif args[0] == 'logs':
			self.logs(self.service, options.follow)
			# self.logging.info('restart' + self.service)
		else:
			self.usage()
