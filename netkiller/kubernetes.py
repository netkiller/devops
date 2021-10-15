#-*- coding: utf-8 -*-
import os
import yaml,json
import logging, logging.handlers
from optparse import OptionParser, OptionGroup

class Logging():
	def __init__(self): 
		
		self.logging = logging.getLogger()

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

class Kubernetes(Logging):
	def __init__(self): 
		super().__init__()
		usage = "usage: %prog [options] <command>"
		self.parser = OptionParser(usage)
		self.parser.add_option("-e", "--environment", dest="environment", help="environment", metavar="development|testing|production")
		self.parser.add_option('','--logfile', dest='logfile', help='logs file.', default='debug.log')
		self.parser.add_option('-l','--list', dest='list', action='store_true', help='print service of environment')

		group = OptionGroup(self.parser, "Cluster Management Commands")
		group.add_option('-g','--get', dest='get', action='store_true', help='Display one or many resources')
		group.add_option('-c','--create', dest='create', action='store_true', help='Create a resource from a file or from stdin')
		group.add_option('-d','--delete', dest='delete', action='store_true', help='Delete resources by filenames, stdin, resources and names, or by resources and label selector')   
		group.add_option('-r','--replace', dest='replace', action='store_true', help='Replace a resource by filename or stdin')
		self.parser.add_option_group(group)

		group = OptionGroup(self.parser, "Others")
		# group.add_option('-d','--daemon', dest='daemon', action='store_true', help='run as daemon')
		group.add_option("", "--debug", action="store_true", dest="debug", help="debug mode")
		group.add_option('-v','--version', dest='version', action='store_true', help='print version information')
		self.parser.add_option_group(group)

		(self.options, self.args) = self.parser.parse_args()
		if self.options.logfile :
			logging.basicConfig(level=logging.NOTSET,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename=self.options.logfile,filemode='a')

		if self.options.debug:
			print("===================================")
			print(self.options)
			print(self.args)
			print("===================================")
			self.logging.debug("="*50)
			self.logging.debug(self.options)
			self.logging.debug(self.args)
			self.logging.debug("="*50)
		
		if self.options.create :
			self.create()
		if self.options.delete :
			self.delete()
		if not self.args :
			self.usage()
	def usage(self):
		print("Python controls the Kubernetes cluster manager.\n")
		self.parser.print_help()
		print("\nHomepage: http://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>")
		exit()
	def execute(self,cmd):
		command = "kubectl {cmd}".format(cmd=cmd)
		self.logging.debug(command)
		# os.system(command)
		return(self)
	def version(self):
		self.execure(self,'version')
		self.execure(self,'api-resources')
		self.execure(self,'api-versions')
		exit()
	def create(self):
		cmd = "{command} -f {yamlfile}".format(command="create", yamlfile="sss.yaml")
		self.execute(cmd)
		self.logging.info(cmd)
		exit()
	def delete(self):
		cmd = "{command} -f {yamlfile}".format(command="delete", yamlfile="sss.yaml")
		self.execute(cmd)
		self.logging.info(cmd)
		exit()
	def describe(self):
		pass
	def edit(self):
		pass
	def replace(self):
		pass
	
# kubernetes = Kubernetes()