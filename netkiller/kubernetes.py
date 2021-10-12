#-*- coding: utf-8 -*-
import yaml,json

class Common():
	commons = {}
	def __init__(self): 
		# self.commons = {}
		self.commons['apiVersion'] = 'v1'
		self.commons['metadata'] = {}
	def apiVersion(self, version = 'v1'):
		self.commons['apiVersion'] = version
	class metadata:
		# metadatas = {}
		def __init__(self): 
			if not 'metadata' in Common.commons :
				Common.commons['metadata'] = {}
			pass
		def name(self, value):
			# self.metadatas['metadata']['name'] = value
			Common.commons['metadata']['name'] = value
			return self
		def namespace(self, value):
			# self.metadatas['metadata']['namespace'] = value
			Common.commons['metadata']['namespace'] = value
			return self
		def labels(self, value):
			# self.metadatas['metadata']['labels'] = value
			Common.commons['metadata']['labels'] = value
			return self
		def annotations(self, value):
			# self.metadatas['metadata']['annotations'] = value
			Common.commons['metadata']['annotations'] = value
			return self
		# def __del__(self):
			# Common.commons.update(self.metadatas)
	# def __del__(self):
		# Common.commons['metadata'] = {}
		# print(self.commons)
      
class Containers:
	container = {}
	def __init__(self): 
		# self.container = {}
		pass
	def name(self, value):
		self.container['name'] = value
		return self
	def image(self,value):
		self.container['images'] = value
		return self
	def command(self,value):
		self.container['command'] = []
		self.container['command'].append(value)
		return self
	def args(self, value):
		self.container['args'] = []
		self.container['args'].append(value)
		return self
	def volumeMounts(self,value):
		self.container['volumeMounts'] = value
		return self
	def imagePullPolicy(self, value):
		self.container['imagePullPolicy'] = value
		return self
	def ports(self, value):
		self.container['ports'] = value
		return self

class Namespace(Common):
	def __init__(self):
		# print(self.commons)
		super().__init__()
		# print(self.commons)
		self.commons['kind'] = 'Namespace'
		# print(self.commons)
	def dump(self):
		return yaml.dump(self.commons)
	def debug(self):
		print(self.dump()) 

class ServiceAccount(Common):
	def __init__(self): 
		super().__init__()
		self.commons['kind'] = 'ServiceAccount'
	def dump(self):
		return yaml.dump(self.commons)
	def debug(self):
		print(self.dump()) 

class Volume(Common):
	def __init__(self): 
		self.volumes = {}
		self.volumes['kind'] = 'PersistentVolume'

class Pod(Common):
	pods = {}
	def __init__(self): 
		super().__init__()
		self.pods['kind'] = 'Pod'
	class spec:
		def __init__(self): 
			if not 'spec' in Pod.pods :
				Pod.pods['spec'] = {}
		def __del__(self):
			Pod.pods['spec']['containers'] = self.containers.container
			# Pod.pods['spec']['restartPolicy'] = 'sdfsf'
			pass
		def restartPolicy(self, value):
			Pod.pods['spec']['restartPolicy'] = value
		def hostAliases(self, value):
			Pod.pods['spec']['hostAliases'] = value
		def env(self, value):
			Pod.pods['spec']['env'] = value
		def securityContext(self,value):
			Pod.pods['spec']['securityContext'] = value
		class containers(Containers):
			def __init__(self): 
				# Pod.pods['spec']['containers'] = {}
				pass
			# def __del__(self):
			# 	Pod.pods['spec']['containers'] = self.container
			# 	print('----')
	def dump(self):
		self.pods.update(self.commons)
		# self.pods['']=
		# self.pods.update()
		return yaml.dump(self.pods,default_style='')
	def debug(self):
		print(self.dump()) 

class Service(Common):
	services = {}
	def __init__(self): 
		super().__init__()
		self.services['kind'] = 'Service'
	class spec:
		def __init__(self): 
			if not 'spec' in Service.services :
				Service.services['spec'] = {}
		def selector(self, value):
			Service.services['spec']['selector'] = value
			return self
		def type(self, value):
			Service.services['spec']['type'] = value
			return self
		def ports(self, value):
			Service.services['spec']['ports'] = value
			return self
		def externalIPs(self, value):
			Service.services['spec']['externalIPs'] = value
			return self
		def clusterIP(self, value):
			Service.services['spec']['clusterIP'] = value
			return self
	class status:
		def __init__(self): 
			if not 'status' in Service.services :
				Service.services['status'] = {}
		def loadBalancer(self,value):
			Service.services['status']['loadBalancer'] = value
			return self
	def dump(self):
		self.services.update(self.commons)
		return yaml.dump(self.services)
	def debug(self):
		print(self.dump()) 

def Deployment():
	def __init__(self): 
		pass
def Test():
	def __init__(self): 
		pass
class ConfigMap(Common):
	def __init__(self): 
		self.config = {}
		self.config['kind'] = 'ConfigMap'
	def data(self, value):
		self.config['data'] = value
	def dump(self):
		self.config.update(self.commons)
		# self.config.update(self.metadata.metadatas)
		return yaml.dump(self.config,default_style='')
	def debug(self):
		print(self.dump())

class Kubernetes():
	def __init__(self): 
		pass 
