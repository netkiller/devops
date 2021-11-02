#-*- coding: utf-8 -*-
import os,sys
import yaml,json
from optparse import OptionParser, OptionGroup
import logging, logging.handlers
from logging import basicConfig

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
	__metadata = {}
	def __init__(self): 
		self.__metadata = {}
		pass
	def name(self, value):
		self.__metadata['name'] = value
		# Common.commons['metadata']['name'] = value
		return self
	def namespace(self, value):
		self.__metadata['namespace'] = value
		# Common.commons['metadata']['namespace'] = value
		return self
	def labels(self, value):
		self.__metadata['labels'] = value
		# Common.commons['metadata']['labels'] = value
		return self
	def annotations(self, value):
		self.__metadata['annotations'] = value
		# Common.commons['metadata']['annotations'] = value
		return self
	# def __del__(self):
			# Common.commons.update(self.metadatas)
	def metadata(self):
		return(self.__metadata)
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
		self.container['image'] = value
		return self
	def command(self,value):
		self.container['command'] = []
		self.container['command'].append(value)
		return self
	def args(self, value):
		self.container['args'] = value
		# self.container['args'].append(value)
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
		# if 'apiVersion' in self.namespace :
		self.apiVersion()
		self.kind('Namespace')
		# self.namespace = {}
		# self.namespace['apiVersion'] = 'v1'
		# self.namespace['kind'] = 'Namespace'
		self.namespace['metadata'] = {}
		# print('ns', self.namespace)
		self.metadata = Metadata()
	def __del__(self):
		self.namespace = {}
	# def test(self, value):
		# self.namespace['test'] = value
	# class metadata(Metadata):
	# 	def __init__(self): 
	# 		# super().__init__()
	# 		print('Meta:', Namespace.namespace)
	# 		# if not 'metadata' in Namespace.namespace :
	# 			# Namespace.namespace['metadata'] = {}
	# 	def __del__(self):
	# 		Namespace.namespace['metadata'].update(self.metadata())
	# 		# self.metadata = {}
	# 		print('del NS', Namespace.namespace)
	# def compose(self):
		# return(self.namespace)
	def dump(self):
		self.namespace.update(self.commons)
		self.namespace['metadata'].update(self.metadata.metadata())
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
			ConfigMap.config['metadata'].update(self.metadata())
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
		self.metadata = Metadata()
		self.account['metadata'] = {}
	# class metadata(Metadata):
	# 	def __init__(self): 
	# 		super().__init__()
	# 		ServiceAccount.account['metadata'] = {}
	# 	def __del__(self):
	# 		ServiceAccount.account['metadata'].update(self.metadata)
	def dump(self):
		self.account.update(self.commons)
		self.account['metadata'].update(self.metadata.metadata())
		return yaml.dump(self.account)
	def debug(self):
		print(self.dump()) 

class Spec:
	spec = {}
	def __init__(self): 
		if not 'containers' in self.spec :
			# self.spec = {}
			self.spec['containers'] = []
		self.containers = Containers()
	def restartPolicy(self, value):
		self.spec['restartPolicy'] = value
	def hostAliases(self, value):
		self.spec['hostAliases'] = value
	def env(self, value):
		self.spec['env'] = value
	def securityContext(self,value):
		self.spec['securityContext'] = value
	# def spec(self):
		# return self.spec
	# class containers(Containers):
		# def __init__(self): 
	# 		spec['containers'] = []
		# def __del__(self):
			# self.spec['containers'].append(self.containers.container)
		# print(self.containers.container)
		print(self.spec)
	class volumes(Volumes):
		def __init__(self): 
			self.spec['volumes'] = []
		def __del__(self):
			self.spec['volumes'].append(self.volumes)

class Pod(Common):
	pod = {}
	def __init__(self): 
		super().__init__()
		self.apiVersion()
		self.kind('Pod')
		self.metadata = Metadata()
		self.pod['metadata'] = {}
		self.pod['spec'] = {}
		self.pod['spec']['containers'] = []
		self.spec = Spec()
	# class metadata(Metadata):
	# 	def __init__(self): 
	# 		super().__init__()
	# 		Pod.pod['metadata'] = {}
	# 	def __del__(self):
	# 		Pod.pod['metadata'].update(self.metadata)
	# class spec:
	# 	containers = Containers()
	# 	def __init__(self): 
	# 		if not 'spec' in Pod.pod :
	# 			Pod.pod['spec'] = {}
	# 	def restartPolicy(self, value):
	# 		Pod.pod['spec']['restartPolicy'] = value
	# 	def hostAliases(self, value):
	# 		Pod.pod['spec']['hostAliases'] = value
	# 	def env(self, value):
	# 		Pod.pod['spec']['env'] = value
	# 	def securityContext(self,value):
	# 		Pod.pod['spec']['securityContext'] = value
	# 	# class containers(Containers):
	# 	# 	def __init__(self): 
	# 	# 		Pod.pod['spec']['containers'] = []
	# 	def __del__(self):
	# 		Pod.pod['spec']['containers'].append(self.containers.container)
	# 		print(self.containers.container)
	# 	class volumes(Volumes):
	# 		def __init__(self): 
	# 			Pod.pod['spec']['volumes'] = []
	# 		def __del__(self):
	# 			Pod.pod['spec']['volumes'].append(self.volumes)
	def dump(self):
		self.pod.update(self.commons)
		self.pod['metadata'].update(self.metadata.metadata())
		self.pod['spec'].update(self.spec.spec)
		self.pod['spec']['containers'].append(self.spec.containers.container)
		print(self.pod)
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
			Service.service['metadata'].update(self.metadata())
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
			Deployment.deployment['metadata'].update(self.metadata())
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
					Deployment.deployment['spec']['template']['metadata'].update(self.metadata())
			class spec:
				def __init__(self): 
					Deployment.deployment['spec']['template']['spec'] = {}		
				class containers(Containers):
					def __init__(self): 
						super().__init__()
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

class Compose(Logging):
	def __init__(self, environment): 
		super().__init__()
		self.compose = []
		self.environment = environment
	# def __del__(self):
		# Kubernetes.composes.update(self.metadata)	
		# print(self.compose)
	def add(self, object):
		self.compose.append(object.dump())
		return(self) 
	def dump(self):
		# yaml.safe_dump(self.compose,stream=file,default_flow_style=False)
		return(yaml.dump(self.compose))
	def debug(self):
		print(self.compose)	
	def yaml(self):
		print('---\n'.join(self.compose))
	def save(self, path):
		path = os.path.expanduser(path)
		# if os.path.exists(path):
			# os.remove(path)
		with open(path, 'w') as file:
			file.write('---\n'.join(self.compose))	

class Kubernetes(Logging):
	def __init__(self): 
		super().__init__()
		self.kubernetes = {}
		self.workspace = '/tmp'

		self.parser = OptionParser("usage: %prog [options] <command>")
		self.parser.add_option("-e", "--environment", dest="environment", help="environment", metavar="development|testing|production")
		self.parser.add_option('-l','--list', dest='list', action='store_true', help='print service of environment')

		group = OptionGroup(self.parser, "Cluster Management Commands")
		group.add_option('-g','--get', dest='get', action='store_true', help='Display one or many resources')
		group.add_option('-c','--create', dest='create', action='store_true', help='Create a resource from a file or from stdin')
		group.add_option('-d','--delete', dest='delete', action='store_true', help='Delete resources by filenames, stdin, resources and names, or by resources and label selector')   
		group.add_option('-r','--replace', dest='replace', action='store_true', help='Replace a resource by filename or stdin')
		self.parser.add_option_group(group)

		group = OptionGroup(self.parser, "Others")
		group.add_option('','--logfile', dest='logfile', help='logs file.', default='debug.log')
		group.add_option('-y','--yaml', dest='yaml', action='store_true', help='show yaml compose')
		group.add_option('','--export', dest='export', action='store_true', help='export docker compose')
		# group.add_option('-d','--daemon', dest='daemon', action='store_true', help='run as daemon')
		group.add_option("", "--debug", action="store_true", dest="debug", help="debug mode")
		group.add_option('-v','--version', dest='version', action='store_true', help='print version information')
		self.parser.add_option_group(group)

		(self.options, self.args) = self.parser.parse_args()
		if self.options.debug :
			logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
		elif self.options.logfile :
			logging.basicConfig(level=logging.NOTSET,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename=self.options.logfile,filemode='a')

		if self.options.debug:
			self.logging.debug("="*50)
			self.logging.debug(self.options)
			self.logging.debug(self.args)
			self.logging.debug("="*50)
		
	def usage(self):
		print("Python controls the Kubernetes cluster manager.\n")
		self.parser.print_help()
		print("\nHomepage: http://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>")
		exit()

	def compose(self, compose):
		self.kubernetes[compose.environment] = compose
		self.logging.info("kubernetes : %s" % (compose.environment))
	def save(self, env):
		if env in self.kubernetes.keys() :
			path = os.path.expanduser(self.workspace + '/' + env +'.yaml')
			self.kubernetes[env].save(path)
			if os.path.exists(path):
				# os.remove(path)
				self.logging.info('save as %s' % path)
				return path
			else:
				return None
	def yaml(self):
		print(self.composes)
		print('---\n'.join(self.composes))
	def debug(self):
		self.logging.debug(self.kubernetes)
	def execute(self,cmd):
		command = "kubectl {cmd}".format(cmd=cmd)
		self.logging.debug(command)
		os.system(command)
		return(self)
	def version(self):
		self.execute('version')
		self.execute('api-resources')
		self.execute('api-versions')
		exit()
	def create(self, env):
		path = self.save(env)
		if path :
			cmd = "{command} -f {yamlfile}".format(command="create", yamlfile=path)
			self.logging.info('create %s' % path)
			self.execute(cmd)
		exit()
	def delete(self, env):
		path = self.save(env)
		if path :
			cmd = "{command} -f {yamlfile}".format(command="delete", yamlfile=path)
			self.logging.info('delete %s ' % path)
			self.execute(cmd)
		exit()
	def replace(self,env):
		path = self.save(env)
		if path :
			cmd = "{command} -f {yamlfile}".format(command="replace", yamlfile=path)
			self.logging.info('replace %s ' % path)
			self.execute(cmd)
		exit()
	def describe(self):
		pass
	def edit(self):
		pass
	def get(self, args):
		cmd = "get {args}".format(args=args)
		self.logging.info('%s ' % cmd)
		self.execute(cmd)
	def list(self):
		for item in self.kubernetes :
			print(item)
	def main(self):
		
		if self.options.list :
			self.list()
		elif self.options.get :
			self.get(' '.join(self.args) )
		elif self.options.yaml :
			self.yaml()
		elif self.options.version :
			self.version()

		elif self.options.create :
			if self.options.environment :
				self.create(self.options.environment)
			else:
				for env in self.kubernetes.keys() :
					self.create(env)
		elif self.options.delete :
			if self.options.environment :
				self.delete(self.options.environment)
			else:
				for env in self.kubernetes.keys() :
					self.delete(env)
		elif self.options.replace :
			if self.options.environment :
				self.replace(self.options.environment)
			else:
				for env in self.kubernetes.keys() :
					self.replace(env)
		else:	
			if not self.args :
				self.usage()
	
