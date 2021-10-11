#-*- coding: utf-8 -*-
import yaml,json

class Common():
	commons = {}
	def __init__(self): 
		self.commons['apiVersion'] = 'v1'
	def apiVersion(self, version = 'v1'):
		self.commons['apiVersion'] = version
	class metadata:
		metadatas = {}
		def __init__(self): 
			self.metadatas['metadata'] = {}
			pass
		def name(self, value):
			self.metadatas['metadata']['name'] = value
			return self
		def namespace(self, value):
			self.metadatas['metadata']['namespace'] = value
			return self
		def labels(self, key,value):
			self.metadatas['metadata'][key] = value
	# class spec:
	#     spec = {}
	#     def __init__(self): 
	#         pass            
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
	def volumeMounts(self,value):
		self.container['volumeMounts'] = value
		return self
	def imagePullPolicy(self, value):
		self.container['imagePullPolicy'] = value
		return self
	def ports(self, value):
		self.container['ports'] = value
		return self

class Volume(Common):
	def __init__(self): 
		self.volumes = {}
		self.volumes['kind'] = 'PersistentVolume'

class Pod(Common):
	pods = {}
	def __init__(self): 
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

class Service():
	def __init__(self): 
		pass    
def Deployment():
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
		self.config.update(self.metadata.metadatas)
		return yaml.dump(self.config,default_style='')
	def debug(self):
		print(self.dump())

class Kubernetes():
	def __init__(self): 
		pass 

pod = Pod()
pod.apiVersion()
spec = container = pod.spec()
spec.restartPolicy('Always')

container = pod.spec().containers()
container.name('nginx')
container.image('nginx:latest').volumeMounts(['name: config-volume','mountPath: /etc/config'])
container.command(['nginx -c /etc/nginx/nginx.conf'])



pod.debug()