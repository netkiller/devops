#-*- coding: utf-8 -*-
import yaml,json

class Common():
	commons = {}
	def __init__(self): 
		self.commons = {}
		pass
	def apiVersion(self, version = 'v1'):
		self.commons['apiVersion'] = version
	def kind(self,value):
		self.commons['kind'] = value

class Metadata:
	metadata = {}
	def __init__(self): 
		self.metadata = {}
		pass
	def name(self, value):
		self.metadata['name'] = value
		# Common.commons['metadata']['name'] = value
		return self
	def namespace(self, value):
		self.metadata['namespace'] = value
		# Common.commons['metadata']['namespace'] = value
		return self
	def labels(self, value):
		self.metadata['labels'] = value
		# Common.commons['metadata']['labels'] = value
		return self
	def annotations(self, value):
		self.metadata['annotations'] = value
		# Common.commons['metadata']['annotations'] = value
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

class Volumes(Common):
	volumes = {}
	def __init__(self): 
		self.volumes = {}
	def name(self,value):
		self.volumes['name'] = value
		return self
	def configMap(self, value):
		self.volumes['configMap'] = value
		return self

class Namespace(Common):
	namespace = {}
	def __init__(self):
		super().__init__()
		self.apiVersion()
		self.kind('Namespace')
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			Namespace.namespace['metadata'] = {}
		def __del__(self):
			Namespace.namespace['metadata'].update(self.metadata)
	def dump(self):
		self.namespace.update(self.commons)
		return yaml.dump(self.namespace)
	def debug(self):
		print(self.dump()) 

class ConfigMap(Common):
	config = {}
	def __init__(self): 
		super().__init__()
		self.apiVersion()
		self.kind('ConfigMap')
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			ConfigMap.config['metadata'] = {}
		def __del__(self):
			ConfigMap.config['metadata'].update(self.metadata)
	def data(self, value):
		self.config['data'] = value
	def dump(self):
		self.config.update(self.commons)
		return yaml.dump(self.config)
	def debug(self):
		print(self.dump())

class ServiceAccount(Common):
	account = {}
	def __init__(self): 
		super().__init__()
		self.apiVersion()
		self.kind('ServiceAccount')
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			ServiceAccount.account['metadata'] = {}
		def __del__(self):
			ServiceAccount.account['metadata'].update(self.metadata)
	def dump(self):
		self.account.update(self.commons)
		return yaml.dump(self.account)
	def debug(self):
		print(self.dump()) 

class Pod(Common):
	pod = {}
	def __init__(self): 
		super().__init__()
		self.apiVersion()
		self.kind('Pod')
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			Pod.pod['metadata'] = {}
		def __del__(self):
			Pod.pod['metadata'].update(self.metadata)
	class spec:
		def __init__(self): 
			if not 'spec' in Pod.pod :
				Pod.pod['spec'] = {}
		def restartPolicy(self, value):
			Pod.pod['spec']['restartPolicy'] = value
		def hostAliases(self, value):
			Pod.pod['spec']['hostAliases'] = value
		def env(self, value):
			Pod.pod['spec']['env'] = value
		def securityContext(self,value):
			Pod.pod['spec']['securityContext'] = value
		class containers(Containers):
			def __init__(self): 
				Pod.pod['spec']['containers'] = []
			def __del__(self):
				Pod.pod['spec']['containers'].append(self.container)
		class volumes(Volumes):
			def __init__(self): 
				Pod.pod['spec']['volumes'] = []
			def __del__(self):
				Pod.pod['spec']['volumes'].append(self.volumes)
	def dump(self):
		self.pod.update(self.commons)
		return yaml.dump(self.pod)
	def debug(self):
		print(self.dump()) 

class Service(Common):
	service = {}
	def __init__(self): 
		super().__init__()
		self.apiVersion()
		self.kind('Service')
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			Service.service['metadata'] = {}
		def __del__(self):
			Service.service['metadata'].update(self.metadata)
	class spec:
		def __init__(self): 
			if not 'spec' in Service.service :
				Service.service['spec'] = {}
		def selector(self, value):
			Service.service['spec']['selector'] = value
			return self
		def type(self, value):
			Service.service['spec']['type'] = value
			return self
		def ports(self, value):
			Service.service['spec']['ports'] = value
			return self
		def externalIPs(self, value):
			Service.service['spec']['externalIPs'] = value
			return self
		def clusterIP(self, value):
			Service.service['spec']['clusterIP'] = value
			return self
	class status:
		def __init__(self): 
			if not 'status' in Service.service :
				Service.service['status'] = {}
		def loadBalancer(self,value):
			Service.service['status']['loadBalancer'] = value
			return self
	def dump(self):
		self.service.update(self.commons)
		return yaml.dump(self.service)
	def debug(self):
		print(self.dump()) 

class Deployment(Common):
	deployment = {}
	def __init__(self): 
		super().__init__()
		# self.apiVersion('apps/v1')
		# self.kind('Deployment')
		self.deployment['apiVersion'] = 'apps/v1'
		self.deployment['kind'] = 'Deployment'
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			Deployment.deployment['metadata'] = {}
		def __del__(self):
			Deployment.deployment['metadata'].update(self.metadata)
			# print(Deployment.deployment)
	class spec:
		def __init__(self): 
			if not 'spec' in Deployment.deployment :
				Deployment.deployment['spec'] = {}
		def selector(self, value):
			Deployment.deployment['spec']['selector'] = value
			return self
		def replicas(self, value):
			Deployment.deployment['spec']['replicas'] = value
			return self
		class template():
			def __init__(self): 
				# super().__init__()
				if not 'template' in Deployment.deployment['spec'] :
					Deployment.deployment['spec']['template'] = {}
				pass
				# Deployment.deployment['spec']['template'].update(self.commons['metadata'])	
			class metadata(Metadata):
				def __init__(self): 
					super().__init__()
					Deployment.deployment['spec']['template']['metadata'] = {}
				def __del__(self):
					Deployment.deployment['spec']['template']['metadata'].update(self.metadata)
			class spec:
				def __init__(self): 
					Deployment.deployment['spec']['template']['spec'] = {}		
				class containers(Containers):
					def __init__(self): 
						Deployment.deployment['spec']['template']['spec']['containers'] = []
						pass
					def __del__(self):
						Deployment.deployment['spec']['template']['spec']['containers'].append(self.container)
	def dump(self):
		# self.deployment.update(self.commons)
		return yaml.dump(self.deployment)
	def debug(self):
		print(self.dump()) 
	def json(self):
		print(self.deployment)

class Ingress(Common):
	ingress = {}
	def __init__(self): 
		super().__init__()
		self.apiVersion('networking.k8s.io/v1beta1')
		self.kind('Ingress')
	class metadata(Metadata):
		def __init__(self): 
			super().__init__()
			Ingress.ingress['metadata'] = {}
		def __del__(self):
			Ingress.ingress['metadata'].update(self.metadata)
	class spec:
		def __init__(self): 
			if not 'spec' in Ingress.ingress :
				Ingress.ingress['spec'] = {}
		def rules(self, value):
			if not 'rules' in Ingress.ingress['spec'] :
				Ingress.ingress['spec']['rules'] = []
			Ingress.ingress['spec']['rules'].extend(value) 
	
	def dump(self):
		self.ingress.update(self.commons)
		return yaml.dump(self.ingress)
	def debug(self):
		print(self.dump()) 
	def json(self):
		print(self.ingress)

class Kubernetes():
	def __init__(self): 
		super().__init__()
		self.service['kind'] = 'Service'
	def describe(self):
		pass
	def edit(self):
		pass
	def replace(self):
		pass
	

deployment = Deployment()
deployment.metadata().name('redis').labels({'app':'redis'})
deployment.spec().replicas(2)
deployment.spec().selector({'matchLabels':{'app':'redis'}})
deployment.spec().template().metadata().labels({'app':'redis'})
deployment.spec().template().spec().containers().name('redis').image('redis:alpine').ports([{'containerPort':'6379'}])
deployment.debug()
deployment.json()