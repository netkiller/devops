#-*- coding: utf-8 -*-
import os, sys
import yaml,json

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
	def __init__(self, name): 
		self.compose = {}
		self.name = name
		self.filename = self.name+'.yaml'
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
	def __to_string(self):
		pass
	def debug(self):
		jsonformat = json.dumps(self.compose, sort_keys=True, indent=4, separators=(',', ':'))
		return(jsonformat)
		# return(self.compose)
	def dump(self):
		# print(yaml.dump(self.compose))
		return(yaml.dump(self.compose))
	def save(self):
		file = open(self.filename,"w")
		yaml.safe_dump(self.compose,stream=file,default_flow_style=False)
	def save_as(self, filename):
		file = open(filename,"w")
		yaml.safe_dump(self.compose,stream=file,default_flow_style=False)
	def up(self, service="", daemon = False):
		self.save()
		d = ''
		if daemon :
			d = '-d'
		command = "docker-compose -f {compose} up {daemon} {service}".format(compose=self.filename, daemon=d, service=service)
		print(command)
		os.system(command)
	def rm(self,service):
		command = "docker-compose -f {compose} rm {service}".format(compose=self.filename, service=service)
		os.system(command)	
	def restart(self,service):
		command = "docker-compose -f {compose} restart {service}".format(compose=self.filename, service=service)
		os.system(self.__to_string())
	def start(self,service):
		command = "docker-compose -f {compose} start {service}".format(compose=self.filename, service=service)
		os.system(command)	
	def stop(self,service):
		command = "docker-compose -f {compose} stop {service}".format(compose=self.filename, service=service)
		os.system(command)	
	def stop(self,service):
		command = "docker-compose -f {compose} stop {service}".format(compose=self.filename, service=service)
		os.system(command)	
	def ps(self,service):
		command = "docker-compose -f {compose} ps {service}".format(compose=self.filename, service=service)
		os.system(command)
	def logs(self,service, follow = False):
		if follow :
			tail = '-f --tail=50'
		command = "docker-compose -f {compose} logs {tail} {service}".format(compose=self.filename, tail=tail,service=service)
		os.system(command)		

class Docker():

	def __init__(self): 
		# pass
		self.composes= {}
	def environment(self, env):
		self.composes[env.name] = env
		return(self)
	def up(self):
		for env,obj in self.composes.items():
			obj.up()
	def rm(self):
		for env,obj in self.composes.items():
			obj.rm()
		return(self)
	def start(self):
		for env,obj in self.composes.items():
			obj.start()
		return(self)
	def stop(self):
		for env,obj in self.composes.items():
			obj.stop()
		return(self)
	def restart(self):
		for env,obj in self.composes.items():
			obj.restart()
		return(self)
	def ps(self):
		for env,obj in self.composes.items():
			obj.ps()
		return(self)
	def dump(self):
		for env,value in self.composes.items():
			print(value.dump())
	def save_all(self):
		for filename,value in self.composes.items():
			file = open(filename,"w")
			yaml.safe_dump(value,stream=file,default_flow_style=False)


